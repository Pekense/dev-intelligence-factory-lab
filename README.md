# DEV Intelligence Factory Lab

Laboratorio de ingeniería asistida por IA: una solicitud de cambio pasa por una API, un modelo local propone una solución y el equipo revisa la propuesta y valida los cambios con un pipeline.

**La IA propone, el pipeline valida y el equipo técnico decide.**

## Dónde está la implementación

| Rama | Estado |
| --- | --- |
| `main` | Estructura inicial, Compose y documentación de arquitectura/gobernanza |
| [`develop`](https://github.com/Pekense/dev-intelligence-factory-lab/tree/develop) | Backend, frontend, PostgreSQL, conector Qwen, propuestas persistidas, patches sugeridos y pipeline local |

Para revisar el código funcional o ejecutar este README, utiliza **`develop`**. No confundas la estructura inicial de `main` con el estado completo del laboratorio.

## Capacidades implementadas en `develop`

- API REST con FastAPI, SQLAlchemy y Pydantic para mercancías, solicitudes de cambio y propuestas.
- PostgreSQL con datos de ejemplo y persistencia de propuestas pendientes de revisión.
- Dashboard React/Vite con configuración de refresco y visualización de solicitudes/propuestas.
- Conector Python a Ollama/Qwen que aporta contexto de archivos conocidos del repositorio.
- Modo de propuesta técnica y modo de generación de un diff sugerido para revisión humana.
- Terraform contra LocalStack para una cola SQS y un script de eventos de temperatura.
- Pipeline local: validación de entorno, pytest, build de frontend y comprobaciones Terraform.

El conector no aplica el patch, no modifica el código, no crea ramas ni commits y no abre o fusiona PR automáticamente. La revisión humana es parte del procedimiento; no constituye por sí sola un sistema de autorización de producción.

## Flujo

| Paso | Resultado |
| --- | --- |
| Solicitud en FastAPI | Cambio estructurado y persistido |
| Conector Python + Ollama | Propuesta técnica basada en contexto controlado |
| Persistencia | Propuesta con estado `PENDING_REVIEW` |
| Modo patch | Archivo de diff sugerido; sin aplicación automática |
| Revisión y pipeline | El desarrollador decide, realiza el cambio y valida |

Es un laboratorio DEV con datos ficticios, no un producto desplegado en una empresa ni una plataforma lista para producción.

## Puesta en marcha

Requisitos: Git, Python 3.12, Node.js compatible con Vite 8, Docker Compose y Terraform `>=1.6`. AWS CLI y Ollama son necesarios para las demostraciones opcionales de SQS e IA.

```bash
git clone --branch develop https://github.com/Pekense/dev-intelligence-factory-lab.git
cd dev-intelligence-factory-lab
docker compose config --quiet
docker compose up -d postgres localstack

# Preparar backend.
python3.12 -m venv backend/.venv
backend/.venv/bin/python -m pip install -r backend/requirements.txt

# Cargar el entorno de ejemplo y arrancar la API solo en loopback.
set -a
source config/backend.dev.env
set +a
cd backend
./.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

La base de datos se inicializa mediante `database/init.sql` al crear el contenedor. No reutilices la base de ejemplo para datos reales.

En otra terminal, desde la raíz:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/ai/change-requests

cp config/frontend.dev.env frontend/.env.local
cd frontend
npm ci
npm run dev -- --host 127.0.0.1
```

Dashboard: `http://127.0.0.1:5173`. Documentación de API: `http://127.0.0.1:8000/docs`.

## Modelo local y propuestas

El conector configura el modelo **`qwen-devsecops:latest`** en `scripts/ai_agent/qwen_change_request_agent.py`. Ese nombre corresponde a un modelo personalizado: prepáralo en tu Ollama o cambia la constante por un modelo que ya tengas instalado. No se incluye un Modelfile que permita reconstruirlo automáticamente.

Con Ollama en `http://localhost:11434` y la API/BD disponibles:

```bash
# Procesar la primera solicitud pendiente y guardar la propuesta.
backend/.venv/bin/python scripts/ai_agent/qwen_change_request_agent.py

# Generar un patch sugerido para una solicitud existente.
backend/.venv/bin/python scripts/ai_agent/qwen_change_request_agent.py --id 8 --mode patch
```

Sustituye `8` por un ID real. El diff se guarda en `reports/agent-runs/`; revísalo antes de aplicarlo. No envíes secretos o información confidencial en solicitudes ni en el contexto del modelo.

## Validación local

Los tests de backend requieren PostgreSQL inicializado y disponible; algunos crean registros. Utiliza únicamente la base del laboratorio.

```bash
cd backend
PYTHONPATH=. ./.venv/bin/python -m pytest
cd ../frontend
npm ci
npm run build
cd ..
bash scripts/validate-env.sh
```

Para utilizar el pipeline completo, inicializa primero Terraform contra el LocalStack del laboratorio:

```bash
cd infrastructure
terraform init
cd ..
bash scripts/local-pipeline.sh
```

El pipeline ejecuta `terraform plan`, no `terraform apply`. No equivale a CI alojada: `.github/workflows/` todavía contiene solo la estructura inicial.

## Seguridad y límites

- Las credenciales PostgreSQL son valores de ejemplo conocidos. Las credenciales AWS `test` apuntan a LocalStack y no son claves AWS reales.
- La API no implementa autenticación de usuarios. Arráncala únicamente en loopback.
- Compose publica PostgreSQL y LocalStack en todas las interfaces. Restringe `5432` y `4566` a `127.0.0.1` antes de utilizar un equipo compartido o accesible por red.
- LocalStack monta el socket Docker del host: ese acceso tiene gran alcance. Revisa su necesidad para esta demo SQS y utiliza un entorno dedicado.
- Los controles de prompt y la revisión manual reducen riesgos, pero no garantizan la corrección ni la seguridad de un patch generado.

Consulta la [revisión de seguridad para publicación](docs/publication-security-review.md).

## Organización y evolución

| Ruta en `develop` | Contenido |
| --- | --- |
| `backend/` | API, modelos y tests |
| `frontend/` | Dashboard React/Vite |
| `database/` | Inicialización y datos de ejemplo |
| `infrastructure/` | Terraform / LocalStack |
| `scripts/ai_agent/` | Conector Qwen y generación de propuestas |
| `scripts/` | Pipeline y validaciones DEV |
| `reports/` | Evidencias del laboratorio y patches sugeridos |

La documentación de diseño está en [arquitectura](https://github.com/Pekense/dev-intelligence-factory-lab/blob/main/docs/architecture.md), [gobernanza](https://github.com/Pekense/dev-intelligence-factory-lab/blob/main/docs/governance.md) y [modelo operativo de IA](https://github.com/Pekense/dev-intelligence-factory-lab/blob/main/docs/ai-operating-model.md).

Próximas mejoras: promover a `main` una versión validada de `develop`, reproducir el modelo personalizado, añadir CI y reforzar aislamiento/autenticación. Son tareas pendientes, no capacidades actuales.
