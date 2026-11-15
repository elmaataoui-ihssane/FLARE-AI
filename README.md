# FLARE AI — Member 2 | Backend & Scientific Analysis MVP

FastAPI + LangGraph workflow + deterministic analysis, conservative ranking and provenance-aware reporting for NASA Space Apps Challenge 2026: **Flame in Freefall**.

> **Scientific honesty:** The included FLEX-DEMO-* measurements are **synthetic**, invented for software testing. NASA links support investigation *descriptions* only; they are NOT sources of demo numeric values. This project is an integration-ready MVP, not a certified fire-safety system. The current research/data nodes are mock adapters and the report generator is deterministic (no live LLM or full RAG yet).

## What works

- API with generated Swagger docs, restricted local CORS, health and error handling.
- LangGraph 5-node workflow when installed (`research mock -> data mock -> analysis -> comparison -> report`). Offline sequential runner is **test fallback only**.
- Mean, median, sample standard deviation, min/max for extinction time.
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

Open http://127.0.0.1:8000/docs then use the prefilled JSON examples in `POST /api/research` or `POST /api/compare`.

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

See [docs/INTEGRATION_CONTRACT.md](docs/INTEGRATION_CONTRACT.md). The default `backend/data/demo_experiments.json` is synthetic. To load approved real data, supply a validated JSON with same `{"groups": [...]}` structure, set environment variable `FLARE_DATA_FILE` and restart; verify its provenance before claiming NASA results.

## Official context / attribution

- NASA Space Apps challenge: https://www.spaceappschallenge.org/2026/challenges/flame-in-freefall/
- NASA PSI combustion catalog: https://www.nasa.gov/physical-sciences-informatics-psi/psi-investigations-by-research-area/
- NASA Combustion Science: https://www.nasa.gov/glenn/glenn-expertise-space-exploration/physical-sciences-program/combustion-science/
- NASA FLEX overview: https://gipoc.grc.nasa.gov/wp/fcf-cir/flex/

## Team responsibilities

- Member 1: NASA research, extraction, cleaning, Research Agent and Data Agent. Current mock nodes replaced after interface review.
- **Member 2 (this package):** API, models, LangGraph workflow, scientific analysis, comparison and report, tests and integration boundary.
- Member 3: Next.js dashboard, visualizations, user chat and backend connectivity.

## Next priorities beyond this MVP

Verified experimental datasets; Member 1's real agents; full document retrieval and citation-grounded LLM/RAG; evaluation of scientific interpretations with domain experts; access controls and production deployment.
