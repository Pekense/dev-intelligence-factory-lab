#!/usr/bin/env python3

"""
Local Qwen Agent Connector - DEV only.

Reads DEV change requests from FastAPI and sends the first pending request
to local Qwen through Ollama HTTP API.

This script:
- does not modify source code;
- does not apply Terraform;
- does not create commits;
- does not create branches;
- does not merge;
- only generates a proposal for human review.
"""

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from urllib import request, error


FASTAPI_CHANGE_REQUESTS_URL = "http://localhost:8000/ai/change-requests"
FASTAPI_CHANGE_PROPOSALS_URL = "http://localhost:8000/ai/change-proposals"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen-devsecops:latest"


@dataclass
class ChangeRequest:
    id: int
    title: str
    description: str
    requested_by: str
    status: str


def fetch_change_requests() -> list[ChangeRequest]:
    """
    Reads change requests from the local DEV FastAPI backend.
    """

    try:
        with request.urlopen(FASTAPI_CHANGE_REQUESTS_URL, timeout=30) as response:
            response_body = response.read().decode("utf-8")
            raw_items = json.loads(response_body)

    except error.URLError as exc:
        raise RuntimeError(
            f"Could not connect to FastAPI at {FASTAPI_CHANGE_REQUESTS_URL}. "
            "Check that the backend is running."
        ) from exc

    change_requests: list[ChangeRequest] = []

    for item in raw_items:
        change_requests.append(
            ChangeRequest(
                id=item["id"],
                title=item["title"],
                description=item["description"],
                requested_by=item.get("requested_by") or item.get("requester", "unknown"),
                status=item.get("status", "unknown"),
            )
        )

    return change_requests


def select_pending_request(change_requests: list[ChangeRequest]) -> ChangeRequest:
    """
    Selects the first actionable DEV change request.
    """

    actionable_statuses = {"pending", "created", "open", "new"}

    for change_request in change_requests:
        if change_request.status.lower() in actionable_statuses:
            return change_request

    available_statuses = sorted({cr.status for cr in change_requests})

    raise RuntimeError(
        "No actionable change requests found. "
        f"Accepted statuses: {sorted(actionable_statuses)}. "
        f"Available statuses: {available_statuses}"
    )


def select_request_by_id(
    change_requests: list[ChangeRequest],
    request_id: int,
) -> ChangeRequest:
    """
    Selects a specific DEV change request by ID.
    """

    for change_request in change_requests:
        if change_request.id == request_id:
            return change_request

    available_ids = sorted(cr.id for cr in change_requests)

    raise RuntimeError(
        f"Change request ID {request_id} not found. "
        f"Available IDs: {available_ids}"
    )


def build_repository_context() -> str:
    """
    Provides controlled repository context to reduce hallucinations.
    This is a manually curated DEV context for the current lab.
    """

    return """
REAL PROJECT CONTEXT - DEV Intelligence Factory Lab

Architecture:
- Backend: FastAPI
- Frontend: React + Vite
- Database: PostgreSQL
- Local cloud simulation: LocalStack with SQS
- Infrastructure as Code: Terraform
- Local AI runtime: Ollama with Qwen

Known real files:

Frontend:
- frontend/src/App.jsx
- frontend/src/App.css
- frontend/package.json
- frontend/vite.config.js

Backend:
- backend/app/main.py
- backend/app/models.py
- backend/app/schemas.py
- backend/tests/

Database:
- database/init.sql

Infrastructure:
- infrastructure/main.tf
- infrastructure/variables.tf
- infrastructure/outputs.tf

Scripts:
- scripts/local-pipeline.sh
- scripts/ai_agent/qwen_change_request_agent.py

Official validation command:
- ./scripts/local-pipeline.sh

Important project rules:
- Do not invent files.
- Only mention files listed in this repository context.
- If a new file is needed, explicitly mark it as "new file proposed".
- Do not suggest commands that are not listed as official validation commands.
- Do not suggest npm test, npm run lint, npm run sast, pytest, terraform apply, or docker compose commands unless explicitly present in the official validation command list.
- Do not suggest production actions.
- Do not suggest automatic commits.
- Do not suggest direct merges.
- Human review is mandatory.

Known endpoint behavior:
- /ai/change-requests exists.
- /shipments is assumed to already provide shipment data including location unless repository inspection proves otherwise.

For frontend-only visual changes, prefer:
- frontend/src/App.jsx
- frontend/src/App.css

For backend data model or API changes, inspect or mention:
- backend/app/main.py
- backend/app/models.py
- backend/app/schemas.py

For database schema changes, inspect or mention:
- database/init.sql
"""
    

def build_prompt(change_request: ChangeRequest) -> str:
    repository_context = build_repository_context()

    return f"""
You are a governed local AI software engineering and DevSecOps assistant.

Your job is NOT to implement changes automatically.
Your job is to produce a controlled technical proposal based only on the real repository context provided.

Project principle:
- The CIO requests.
- The developer governs.
- The AI agent proposes.
- The pipeline validates.
- DevOps/DevSecOps reviews.
- The team decides.

Strict restrictions:
- DEV only.
- No production changes.
- No real secrets.
- No terraform apply.
- No direct merge.
- No automatic code modification.
- No automatic commits.
- Human review is mandatory.

Repository context:
{repository_context}

Change request:

ID: {change_request.id}
Title: {change_request.title}
Requested by: {change_request.requested_by}
Status: {change_request.status}

Description:
{change_request.description}

You must generate a controlled technical proposal.

Hard anti-hallucination rules:
- Do not invent repository files.
- Only mention files included in the repository context.
- If a new file is required, label it clearly as: "new file proposed".
- If you are unsure, say: "pending repository inspection".
- Use only the official validation command: ./scripts/local-pipeline.sh
- Do not suggest npm test, npm run lint, npm run sast, pytest, terraform apply, or direct docker commands.
- Do not suggest production deployment.
- Do not suggest direct merge.
- If the requested change can be solved with existing frontend shipment data, do not invent backend services.
- For shipment location visibility, prefer frontend/src/App.jsx and frontend/src/App.css unless the request explicitly requires API changes.

Required output format in Markdown:

# Controlled AI Proposal

## 1. Request summary
Summarize the requested change.

## 2. Impact analysis
Explain whether this looks like frontend, backend, database, infrastructure, or mixed change.

## 3. Existing files likely affected
List only real files from the provided repository context.

## 4. New files proposed
List only if truly needed. Otherwise say: "None".

## 5. Technical approach
Describe the safest DEV-only implementation approach.

## 6. Risks
Include technical, security, UX, and DevSecOps risks.

## 7. Validation
Official validation command:
- ./scripts/local-pipeline.sh

## 8. Pull request summary
Write a concise PR summary.

## 9. Confidence level
Use one of: Low, Medium, High.
Explain briefly why.

Return only the proposal.
"""

def call_ollama(prompt: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    data = json.dumps(payload).encode("utf-8")

    req = request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=180) as response:
            response_body = response.read().decode("utf-8")
            result = json.loads(response_body)

            if "response" not in result:
                raise RuntimeError(f"Unexpected Ollama response: {result}")

            return result["response"].strip()

    except error.URLError as exc:
        raise RuntimeError(
            f"Could not connect to Ollama at {OLLAMA_URL}. "
            "Check that the Docker container 'ollama' is running."
        ) from exc



def extract_confidence_level(proposal_markdown: str) -> str:
    """
    Extracts a simple confidence level from the generated proposal.
    Defaults to Medium if the model output is ambiguous.
    """

    lower_proposal = proposal_markdown.lower()

    if "confidence level" in lower_proposal or "confidence" in lower_proposal:
        if "high" in lower_proposal or "alto" in lower_proposal:
            return "High"
        if "low" in lower_proposal or "bajo" in lower_proposal:
            return "Low"

    return "Medium"


def save_change_proposal(
    change_request: ChangeRequest,
    proposal_markdown: str,
) -> dict:
    """
    Persists the Qwen proposal in FastAPI/PostgreSQL for human review.
    """

    payload = {
        "change_request_id": change_request.id,
        "model_name": OLLAMA_MODEL,
        "proposal_markdown": proposal_markdown,
        "confidence_level": extract_confidence_level(proposal_markdown),
    }

    data = json.dumps(payload).encode("utf-8")

    req = request.Request(
        FASTAPI_CHANGE_PROPOSALS_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=30) as response:
            response_body = response.read().decode("utf-8")
            return json.loads(response_body)

    except error.URLError as exc:
        raise RuntimeError(
            f"Could not save proposal through FastAPI at {FASTAPI_CHANGE_PROPOSALS_URL}. "
            "Check that the backend is running and /ai/change-proposals is available."
        ) from exc


def read_allowed_patch_files() -> str:
    """
    Reads the current content of files allowed for patch generation.
    This reduces hallucinations by giving Qwen the real source code.
    """

    allowed_files = [
        "frontend/src/App.jsx",
        "frontend/src/App.css",
    ]

    sections = []

    for file_path in allowed_files:
        path = Path(file_path)

        if not path.exists():
            sections.append(f"FILE: {file_path}\nSTATUS: missing")
            continue

        content = path.read_text()
        sections.append(
            f"FILE: {file_path}\n"
            f"CURRENT CONTENT START\n"
            f"{content}\n"
            f"CURRENT CONTENT END"
        )

    return "\n\n".join(sections)



def build_patch_prompt(change_request: ChangeRequest) -> str:
    """
    Builds a controlled prompt asking Qwen for a suggested unified diff.
    The patch is not applied automatically.
    """

    repository_context = build_repository_context()
    allowed_file_contents = read_allowed_patch_files()

    return f"""
You are a governed local AI software engineering assistant.

Your task is to generate a MINIMAL suggested unified diff.
This patch will NOT be applied automatically.

Repository context:
{repository_context}

Allowed file contents:
{allowed_file_contents}

Change request:

ID: {change_request.id}
Title: {change_request.title}
Requested by: {change_request.requested_by}
Status: {change_request.status}

Description:
{change_request.description}

Allowed files for this patch:
- frontend/src/App.jsx
- frontend/src/App.css

Hard rules:
- Use only the real file contents provided above.
- Do not invent components.
- Do not invent imports.
- Do not invent files.
- Do not create new files.
- Do not modify backend files.
- Do not modify database files.
- Do not modify Terraform files.
- Do not suggest commands.
- Do not commit.
- Do not merge.
- Do not apply the patch.
- Keep the change minimal.
- The dashboard already displays the current shipment location using shipment.location.
- Do not add duplicate location columns.
- Do not create or use new fields such as shipment.location_updated, shipment.current_location, shipment.gps_location, or similar.
- Use only the existing field: shipment.location.
- The correct frontend change is to improve the existing <td>{{shipment.location}}</td> rendering.
- Prefer wrapping shipment.location in a visual badge/span.
- Improve the visual presentation of the existing location value.

Expected output:
- Return only a unified diff patch.
- The diff must only reference:
  frontend/src/App.jsx
  frontend/src/App.css
- Do not wrap the diff in Markdown fences.
- Do not add confidence text outside the diff.
"""

def save_suggested_patch(
    change_request: ChangeRequest,
    patch_content: str,
) -> Path:
    """
    Saves the Qwen-generated suggested patch for human review.
    """

    output_dir = Path("reports/agent-runs")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"change-request-{change_request.id}-suggested.patch"
    output_path.write_text(patch_content)

    return output_path

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Local governed Qwen connector for DEV AI change requests."
    )
    parser.add_argument(
        "--id",
        type=int,
        help="Specific ai_change_requests ID to analyze.",
    )
    parser.add_argument(
        "--mode",
        choices=["proposal", "patch"],
        default="proposal",
        help="Execution mode: proposal saves an AI proposal; patch saves a suggested patch file.",
    )

    args = parser.parse_args()

    print("=== Reading DEV change requests from FastAPI ===\n")

    change_requests = fetch_change_requests()

    if args.id is not None:
        change_request = select_request_by_id(change_requests, args.id)
    else:
        change_request = select_pending_request(change_requests)

    print(f"Selected change request ID: {change_request.id}")
    print(f"Title: {change_request.title}")
    print(f"Requested by: {change_request.requested_by}")
    print(f"Status: {change_request.status}")
    print(f"Mode: {args.mode}\n")

    if args.mode == "patch":
        prompt = build_patch_prompt(change_request)

        print("=== Sending governed PATCH prompt to local Qwen ===\n")
        patch_content = call_ollama(prompt)

        output_path = save_suggested_patch(change_request, patch_content)

        print("=== Suggested patch saved for human review ===")
        print(f"Patch file: {output_path}")
        print("\nReview it with:")
        print(f"cat {output_path}")
        print("\nThis script did not modify source code.")
        return

    prompt = build_prompt(change_request)

    print("=== Sending governed DEV prompt to local Qwen ===\n")
    proposal_markdown = call_ollama(prompt)

    print("=== Qwen governed proposal ===\n")
    print(proposal_markdown)

    print("\n=== Saving proposal for human review ===\n")
    saved_proposal = save_change_proposal(change_request, proposal_markdown)

    print("=== Proposal saved for review ===")
    print(f"Proposal ID: {saved_proposal['id']}")
    print(f"Change request ID: {saved_proposal['change_request_id']}")
    print(f"Review status: {saved_proposal['review_status']}")
    print(f"Confidence level: {saved_proposal['confidence_level']}")


if __name__ == "__main__":
    main()
