# FLARE AI frontend

Next.js research workspace for the existing FastAPI service.

```powershell
cd frontend
npm install
Copy-Item .env.example .env.local
npm run dev
```

Start the backend separately on port 8000 as described in the root README, then open http://localhost:3000. The default API base is `http://127.0.0.1:8000`; set `NEXT_PUBLIC_API_BASE_URL` if it differs. Configure backend `CORS_ALLOWED_ORIGINS` when using a different frontend origin.

The workspace calls `/api/health`, `/api/experiments`, `/api/nasa-investigations`, `/api/datasets`, dataset profiles and `/api/research`. The backend does not currently provide streaming, live agent events, persisted chat history, a standalone publication catalogue, or report export. The interface labels these limitations and uses the completed workflow trace for agent status. Dataset records are third-party and source references are not independently verified. Missing values are never converted to zero.

PillNav, PromptBar and ElectricBorder are sourced from the React Bits registry (https://reactbits.dev); the workspace configures only supported research interactions.

## End-to-end tests

Start the backend on port 8000 and the frontend on port 3000, then run `npx playwright install chromium` and `npm run test:e2e`. To use an existing browser, set `FLARE_BROWSER_PATH` to its executable. Set `FLARE_FRONTEND_URL` if the frontend uses a different URL. The tests submit a real research request and check analysis, dataset profiles, investigations, reports, and mobile navigation.

The default Evidence Explorer supports a focused review of one dataset family at a time. Filters and counts apply only to the records currently shown. A record can be inspected with its extracted conditions and source IDs, and source links are resolved from `/api/sources` when present. PDF page references come from the third-party extraction and require checking against the original publication. Export creates a CSV of the visible extracted records; it is not a validated scientific report. Recorded gravity is displayed only when present in the row, including LUCI simulated lunar gravity.
