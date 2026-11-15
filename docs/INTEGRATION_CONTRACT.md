# Backend data and API contract

## Dataset-backed experiment workflow

The numerical workflow reads cleaned CSVs in the repository's `data/experiments/` folder. It does not read a synthetic demo JSON file. Original records remain in `data/raw/microfire_atlas/`.

| Group ID | Dataset | Rows | Numeric fields summarized |
| --- | --- | ---: | --- |
| `BASS2-TESTS` | BASS-II | 56 | Thickness, width, flow, oxygen, pressure |
| `LUCI-RUNS` | LUCI | 2 | Oxygen, pressure, flame spread |
| `SAFFIRE-RUNS` | SAFFIRE | 20 | Sample dimensions, flow, oxygen, pressure, burn duration, flame spread, heat release |

Numeric units come from the source column names. Missing values are counted. Nonnumeric cells such as pressure ranges remain in each trial's metadata and are excluded from numeric summaries. Every row's original columns, outcomes, and source/page references are kept in `trial.metadata` and returned by `GET /api/experiments`.

The files came through the third-party MicroFire Atlas. They are labeled `third_party`, not NASA-verified. NASA source IDs and page references are provenance leads. Group-level summaries can include varying conditions; they are descriptive and do not establish causal effects or safety rankings. `/api/compare` blocks mismatched families and does not rank datasets without extinction-time measurements.

## Routes

- `GET /api/health` — loaded dataset groups, workflow engine and OpenAI configuration state.
- `GET /api/experiments` — parsed dataset groups with all per-row source metadata.
- `GET /api/nasa-investigations` — Member 1 NASA PSI catalog; context only.
- `GET /api/datasets` — raw and cleaned file inventory; `?q=saffire` filters filenames.
- `GET /api/datasets/{filename}/profile` — CSV shape, missing-value counts, duplicates and descriptive statistics.
- `GET /api/datasets/compare?dataset_a=...&dataset_b=...` — source column and row-count comparison.
- `POST /api/research` — local evidence retrieval, CSV-backed metric summaries and (when configured) OpenAI synthesis.
- `POST /api/compare` — conservative comparison of selected dataset groups; mismatched experimental families are blocked.
- `POST /api/validate-dataset` — validates an `ExperimentGroup` payload's schema only.
- `/docs` and `/openapi.json` — interactive Swagger UI and API schema.

Example research body:

```json
{
  "question": "Summarize the measured spread rates in SAFFIRE",
  "group_ids": ["SAFFIRE-RUNS"]
}
```

The response includes `research_context.answer`, `research_context.dataset_analyses`, per-metric `analyses`, source-aware `report`, and the workflow trace. The OpenAI answer is constrained to retrieved local evidence and numeric summaries; the local evidence remains available if the model call fails.

## OpenAI setup

Set `OPENAI_API_KEY` in `backend/.env`; optional `OPENAI_MODEL` defaults to `gpt-4.1-mini`. The app loads this file at startup. Do not commit `.env`; `.env.example` is a placeholder.
