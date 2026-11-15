# Interface between Member 1, Member 2 and Member 3

## Member 1 -> Member 2

- Provide a JSON document of the form `{"groups": [ExperimentGroup, ...]}`.
- Each `ExperimentGroup` has `group_id`, `experiment_family`, `title`, `source_kind`, `conditions`, and `trials`.
- Each `Trial` has `trial_id`, optional `extinction_time_s`, and optionally `measurements` (metric -> {value, unit}).
- All values claimed to be NASA must have an **actual source for the measurements**, not just a page about the experiment (`data_source_url`).
- These are provisional interface names. Member 1 should not be forced to adapt their real data blindly; confirm and version before merger.
- Numeric variables must have explicit units. The analysis rejects mixed units rather than silently converting.
- To test shape: POST `/api/validate-dataset`. This validates *schema*, not NASA provenance or scientific appropriateness.
- Once reviewed, set `FLARE_DATA_FILE` to the local JSON path and restart the server; synthetic demo remains the default.

## Member 2 -> Member 3

- `GET /api/health` for state and whether any real data is loaded.
- `GET /api/experiments` for groups (each has `source_kind`).
- `GET /api/nasa-investigations` for NASA context ONLY.
- `POST /api/research`: `{"question":"Analyze FLEX","group_ids":["FLEX-DEMO-A"]}`.
- `POST /api/compare`: `{"group_ids":["FLEX-DEMO-A","FLEX-DEMO-B"]}`.
- OpenAPI docs: `/docs` and `/openapi.json`.
- Response fields: `analyses`, `comparison`, `report`, `workflow_trace`, `disclaimer`.
- `analyses[].measurements` lists per-metric summaries (mean, median, sample SD, min/max, n_missing, unit, status).
- `CORS_ALLOWED_ORIGINS` accepts a comma-separated set of approved frontend origins (default: localhost:3000 and 127.0.0.1:3000).

## Limitations / required follow-up

- Research Agent and Data Agent are **mock adapters**; Member 1's actual agents are not integrated yet.
- The report agent is evidence-aware **template generation**, not an LLM.
- No production RAG, vector database, automatic NASA harvesting, certified fire-safety model or causal ranking.
- Ranking is descriptive and restricted to matched recorded control conditions.
- Test with actual NASA experimental datasets and subject-matter review before presenting scientific conclusions.
