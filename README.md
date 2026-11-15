# FLARE AI — Dataset-backed NASA fire research backend

FastAPI + LangGraph workflow + deterministic analysis, conservative ranking and provenance-aware reporting for NASA Space Apps Challenge 2026: **Flame in Freefall**.

> **Scientific honesty:** The experiment and analysis endpoints now load the BASS-II, LUCI and SAFFIRE cleaned CSVs from `data/experiments/`. Those extracted datasets were provided by the third-party MicroFire Atlas; row-level NASA source IDs and page references are preserved but do not independently establish provenance. Dataset-wide statistics include measured conditions and outcomes, and do not imply matched controls or causal effects. When `OPENAI_API_KEY` is configured, the Responses API adds a synthesis grounded in those local summaries and source records. This project is not a certified fire-safety system.

## What works

- API with generated Swagger docs, restricted local CORS, health and error handling.
- LangGraph 5-node workflow when installed (Member 1 research and CSV data adapters -> analysis -> conservative comparison -> report). Offline sequential runner is test fallback only.
- Member 1 research catalog, source-manifest and finding search, plus raw/processed dataset listing, profiling and schema comparison endpoints.
- Mean, median, sample standard deviation, min/max, and missing/non-scalar counts for source-defined numeric fields with recorded units.
- General numeric metric summaries with unit check, missing counts and explicit insufficient-data behavior.
- Descriptive ranking restricted to matched controls and same source type.
- Machine-readable schemas for Member 1 integration and Frontend Member 3.
- Pytest + GitHub Actions CI.

## Run on Windows CMD

```cmd
cd backend
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pytest -q
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs then use the prefilled JSON examples in `POST /api/research` or `POST /api/compare`. Dataset group IDs are `BASS2-TESTS`, `LUCI-RUNS`, and `SAFFIRE-RUNS`.

The backend loads `backend/.env` at startup. Configure `OPENAI_API_KEY` there to enable the ResearchAgent's OpenAI synthesis; `OPENAI_MODEL` defaults to `gpt-4.1-mini`. `GET /api/health` reports whether the agent is configured. The research endpoint always returns local evidence matches even if the model request fails.

**Note:** Python 3.12 is used in GitHub CI. The local contributor has also tested their environment with Python 3.14.

## Run on Linux / WSL

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
python -m uvicorn app.main:app --reload
```

## Data + API contracts

See [docs/INTEGRATION_CONTRACT.md](docs/INTEGRATION_CONTRACT.md). Both the experiment workflow and dataset API read repository-relative files from `data/raw/` and `data/experiments/`. Original CSVs are not modified. Units come from source column names; range strings stay in row metadata and are excluded from numeric summaries. Comparison blocks cross-family or otherwise unmatched datasets.

## Official context / attribution

- NASA Space Apps challenge: https://www.spaceappschallenge.org/2026/challenges/flame-in-freefall/
- NASA PSI combustion catalog: https://www.nasa.gov/physical-sciences-informatics-psi/psi-investigations-by-research-area/
- NASA Combustion Science: https://www.nasa.gov/glenn/glenn-expertise-space-exploration/physical-sciences-program/combustion-science/
- NASA FLEX overview: https://gipoc.grc.nasa.gov/wp/fcf-cir/flex/

## Team responsibilities

- Member 1: NASA research, extraction, cleaning, Research Agent and Data Agent, integrated through `backend/app/adapters/member1.py`.
- **Member 2 (this package):** API, models, LangGraph workflow, scientific analysis, comparison and report, OpenAI synthesis, tests and integration boundary.
- Member 3: Next.js dashboard, visualizations, user chat and backend connectivity.

## Next priorities beyond this MVP

Independent verification of extracted measurements; full document retrieval and citation-grounded RAG; domain review of scientific interpretations; access controls and production deployment.

## Frontend (Member 3)

The Next.js research workspace is in [`frontend/`](frontend/README.md). Start the backend first, then run `npm install` and `npm run dev` in `frontend/`; open http://localhost:3000. See the frontend README for API configuration and current integration limitations.
