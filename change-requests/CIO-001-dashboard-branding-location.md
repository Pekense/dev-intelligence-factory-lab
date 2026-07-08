# CIO-001 — Dashboard branding and shipment location visibility

## Business request

The CIO requests a more corporate dashboard experience and clearer visibility of where each shipment currently is.

## Functional requirements

- Add a corporate identity placeholder to the dashboard.
- Highlight the current location of each shipment.
- Keep shipment status, ETA, temperature and alert state visible.
- Preserve the executive summary cards.
- Do not remove existing functionality.
- Do not use real company logos or real brand assets.

## Technical constraints

- DEV only.
- Frontend-first change unless backend changes are strictly required.
- No production changes.
- No secrets.
- No direct merge.
- No terraform apply.
- Pipeline must pass.
- Pull Request required.
- Human review required.

## Expected outcome

A developer can submit this request to a governed local AI agent.

The agent should analyze the repository, identify affected files, propose changes, and leave the project ready for pipeline validation and human review.

## Acceptance criteria

- Dashboard shows a DEV-safe corporate branding placeholder.
- Shipment current location is visually easier to identify.
- Existing dashboard metrics still work.
- Backend tests pass.
- Frontend build passes.
- Terraform validation and plan pass.
- Local pipeline completes successfully.
