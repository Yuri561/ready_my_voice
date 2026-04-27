# Ready My Voice — Backend

FastAPI backend for the Tauri app.

## Setup

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```

## Run (dev)

```powershell
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Or:

```powershell
python -m backend.main
```

Then open:

- API root: http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/api/health

## Project layout

```
backend/
├── __init__.py
├── main.py           # FastAPI app + CORS for Tauri/Vite
├── config.py         # Env-driven settings
├── requirements.txt
└── routers/
    ├── __init__.py
    └── health.py
```

## Calling from the Tauri frontend

In `tauri_app/src`:

```ts
const res = await fetch("http://127.0.0.1:8000/api/health");
const data = await res.json();
```

For production, ensure the backend is started alongside the Tauri app
(e.g. via a Tauri sidecar) and that its origin is listed in
`allow_origins` in `backend/main.py`.
