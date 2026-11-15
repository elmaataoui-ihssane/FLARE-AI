# FLARE AI — Frontend Specification for the Coding Agent

> **Purpose:** Build the frontend for FLARE AI, an agentic scientific research platform focused on NASA microgravity combustion and spacecraft-fire research.
>
> **Audience:** Frontend coding agent / Member 3  
> **Primary goal:** Deliver a polished, usable interface that connects to the existing backend and makes the research workflow, agents, datasets, evidence, and outputs understandable.

---

## 1. Product vision

FLARE AI is **not just a chatbot and not merely an analytics dashboard**.

It is an agentic research workspace where a user can ask a scientific question and follow how specialized agents help answer it:

1. The Research Agent finds relevant investigations and publications.
2. The Data Agent discovers and loads relevant datasets.
3. The analysis workflow compares or examines the available data.
4. The reporting workflow organizes findings and their supporting evidence.

The frontend should make this workflow visible without overwhelming the user. The main experience is the **Research Workspace**, supported by dedicated pages for datasets, investigations, knowledge sources, analysis, reports, and agent monitoring.

### Product principles

- Research-first: the user's question and the evidence should remain central.
- Agent transparency: show which agent is working, what it is doing, and whether it succeeded.
- Evidence-based: distinguish sourced facts, computed results, and missing information.
- Scientific integrity: never present missing values as zero or fabricate results.
- Simple MVP: build a reliable, coherent workflow before adding advanced features.
- Reuse the existing backend and project stack; do not rebuild backend logic in the frontend.

---

## 2. Main application navigation

Use a persistent left sidebar with these groups and pages.

### Workspace
- **Research Workspace** — primary AI research interface.
- **Agent Center** — agent status and execution details.

### Scientific Research
- **Investigations** — browse research programs and experiments.
- **Datasets Explorer** — inspect available datasets and records.
- **Scientific Analysis** — comparisons, charts, and analysis outputs.
- **Knowledge Base** — publications, source registry, and research documents.

### Outputs
- **Research Reports** — generated reports and export actions.
- **Research History** — previous research sessions and their results.

### System
- **System Monitoring** — service status, execution logs, and errors.
- **Settings** — frontend and user preferences, plus configuration exposed by the backend.

The sidebar should clearly indicate the active page. On smaller screens, it should collapse into a drawer or compact navigation.

---

## 3. Global application layout

Use a consistent application shell across all pages:

### A. Left sidebar
- FLARE AI logo and wordmark at the top.
- Grouped navigation listed above.
- Small, consistent line icons.
- Active navigation state with a subtle cyan/blue accent.
- Optional user/profile area at the bottom.

### B. Top bar
- Current page title or breadcrumb.
- Search field if supported by the backend.
- Backend/API connection indicator.
- Notifications or activity entry point if implemented.
- User avatar/profile menu if authentication exists.

### C. Main content
- Page-specific content with consistent spacing and alignment.
- Clear page title and one-line explanation.
- Loading, empty, success, and error states.
- Avoid overcrowded cards and unnecessary decorative elements.

### D. Optional contextual panel
On the Research Workspace, use a right-hand panel for agent workflow, selected sources, and evidence quality. It may collapse on smaller screens.

---

## 4. Page requirements

## 4.1 Research Workspace — highest priority

This is the main landing page and the heart of FLARE AI.

### Required elements
- Page heading: **Research Workspace**.
- Short description explaining that users can explore NASA combustion science with collaborative AI agents.
- Conversation area containing user questions and assistant responses.
- Message composer with:
  - Multiline question input.
  - Send action.
  - Attachment/source action only if supported.
  - Disabled/loading state while a request is running.
- Responses should support readable paragraphs, lists, tables, and citations.
- Display linked publications, investigations, and datasets used in the answer.
- Provide clear feedback when no relevant evidence is found.

### Agent workflow visibility
Show the stages of a research run, for example:
1. Research Agent — searching investigations and publications.
2. Data Agent — finding and loading relevant datasets.
3. Analysis Agent — comparing or analyzing available data.
4. Report Agent — preparing a structured result.

Use statuses such as:
- Waiting
- Running
- Completed
- Failed

Only show agents and stages that actually exist in the backend. If an agent is not implemented yet, mark it as unavailable or omit it; do not simulate successful execution.

### Example demonstration query
`Compare flame-spread behavior in SAFFIRE and BASS-II.`

Use this only as example UI content or a demo prompt. Do not hardcode a fabricated scientific answer.

---

## 4.2 Agent Center

A dedicated view for understanding the agentic system.

### Required elements
- Agent cards or a compact list for each available agent.
- Agent name, purpose, current status, and last execution if available.
- Execution history or recent task list.
- Expandable details for inputs, outputs, errors, and duration when supplied by the backend.
- Clear distinction between a real backend status and a frontend placeholder.

### Initial agents known in the project
- Research Agent
- Data Agent

Analysis and Report agents may be displayed only if the backend exposes them or the team implements them. Do not imply that they already work if they do not.

---

## 4.3 Investigations

A searchable catalogue of scientific investigations.

### Required elements
- Search by name, topic, or other supported metadata.
- List or grid of investigation records.
- Investigation detail view or expandable panel.
- Show available metadata such as name, identifier, topic, priority, and source URL.
- Link to associated publications and datasets when relationships are available.

### Known examples in the current project
- BASS-II
- SAFFIRE-I
- SAFFIRE-II
- SAFFIRE-III
- FLEX

The current investigation catalogue contains seven records. Load the actual records from the backend/data source rather than hardcoding this list as the complete catalogue.

---

## 4.4 Datasets Explorer

A scientific data browser for the project's processed and raw datasets.

### Required elements
- Dataset list with filename, record count, column count, and source/type where available.
- Dataset detail page or panel.
- Tabular data preview with pagination or virtualization for larger files.
- Search and filtering where supported.
- Column names and data types.
- Missing-value visibility.
- Dataset profile summary: rows, columns, missing values, duplicates, and available statistics.
- Clear distinction between raw and processed datasets.

### Known processed datasets
- `saffire_runs_cleaned.csv` — 20 rows, 23 columns.
- `bass2_tests_cleaned.csv` — 56 rows, 17 columns.
- `luci_runs_cleaned.csv` — 2 rows, 19 columns.

These are current project examples, not permanent hardcoded values. Fetch current metadata from the backend.

### Scientific data integrity rules
- Never silently convert missing values (`NaN` / null) to zero.
- Do not hide missing values in a way that changes interpretation.
- Preserve units and original recorded values when available.
- Show source and PDF-page references when present.
- Do not merge columns with different meanings just because their names look similar.

---

## 4.5 Scientific Analysis

A workspace for inspecting analysis results and comparing experiments or datasets.

### Required elements
- Select two or more datasets/experiments when supported.
- Show comparable columns and clearly identify non-comparable fields.
- Display analysis outputs returned by the backend.
- Charts with axis labels, units, legends, and readable tooltips.
- Tables for exact values behind charts.
- Explain which records and filters were used.
- Show limitations caused by missing or incompatible data.

### Important
Do not invent statistical conclusions or calculate comparisons from incompatible fields. The frontend should visualize backend results and only perform simple, clearly defined client-side transformations when appropriate.

---

## 4.6 Knowledge Base

A searchable catalogue of scientific references and source material.

### Required elements
- Search publications by title, abstract, author, or identifier when supported.
- Publication list and detail view.
- Show title, authors, date, abstract, source identifier, and URL when available.
- Link a publication to relevant investigations or datasets when those relationships exist.
- Source registry view showing source metadata and provenance.

The current project has collected 47 NASA publication records. Treat this as current data, not a fixed UI constant.

---

## 4.7 Research Reports

A place to review and export research outputs.

### Required elements
- List of reports or completed research runs.
- Report detail view with title, question, summary, methodology, findings, limitations, and references when available.
- Evidence/citation links.
- Export/download action only for formats supported by the backend.
- Clear report generation status.

Do not create fake report files or claim an export succeeded unless the backend confirms it.

---

## 4.8 Research History

A searchable history of previous research sessions.

### Required elements
- Previous questions/sessions.
- Date and status.
- Short result preview.
- Open a previous session and inspect its messages, agent runs, sources, and outputs if stored.
- Empty state for a new user or an empty history.

If the backend does not persist history yet, show a clear empty/not-yet-supported state rather than storing misleading mock history.

---

## 4.9 System Monitoring

A simple operational view for developers and users.

### Required elements
- Backend/API availability.
- Agent status when exposed by the backend.
- Recent execution events or logs if available.
- Error messages that help diagnose failed requests.
- Loading and retry states.

Do not expose secrets, API keys, environment variables, or sensitive stack traces in the UI.

---

## 4.10 Settings

Keep this page lightweight for the MVP.

Possible settings, only when supported:
- Theme preference.
- User profile.
- Display preferences.
- Backend or model configuration status (read-only unless authorized).
- Clear explanation of unavailable settings.

Never expose credentials or secret configuration values.

---

## 5. Visual design system

### Overall direction
Create a professional scientific SaaS product with a subtle mission-control character. It should feel trustworthy, calm, precise, and modern—not like a game interface or a flashy sci-fi dashboard.

### Suggested palette

| Purpose | Color |
|---|---|
| Main background | `#080D1B` |
| Panel background | `#111A2D` |
| Elevated panel | `#172238` |
| Primary blue | `#397BFF` |
| Cyan accent | `#22C7E8` |
| Flame accent | `#FF8B38` |
| Main text | `#F4F7FC` |
| Secondary text | `#9AAAC0` |
| Borders | `#26344B` |
| Success | `#35B887` |
| Warning | `#E7AD4B` |
| Error | `#E56B73` |

Use the flame-orange accent sparingly, mainly in the logo or small status details. Blue and cyan should carry most interactive emphasis.

### Logo direction
- Simple, recognizable abstract flame symbol.
- Cyan/blue outer flame with a small orange core.
- FLARE AI wordmark in a clean sans-serif font.
- Must remain legible at small sidebar sizes.
- Avoid complex illustrations or excessive gradients.

### Typography and components
- Use a clean modern sans-serif font.
- Establish clear heading/body/metadata hierarchy.
- Use consistent spacing, border radius, and icon sizes.
- Prefer subtle borders and restrained shadows.
- Use charts and tables with readable labels and units.
- Avoid excessive glow, glass effects, gradients, and decorative backgrounds.

### Light theme
Dark theme is the initial visual target. Structure the design tokens so a light theme can be added later without rewriting components.

---

## 6. Interaction and UX requirements

Every page must include appropriate states:

- **Loading:** skeletons or clear progress indicators.
- **Empty:** explain what is missing and what the user can do.
- **Success:** concise confirmation after a completed action.
- **Error:** human-readable message and retry action where appropriate.
- **Disabled:** explain why an action cannot currently be used.

Additional requirements:
- Keep navigation consistent across pages.
- Preserve the user's current research context when navigating where practical.
- Use confirmation for destructive actions.
- Make tables usable on smaller screens.
- Provide keyboard-accessible controls and visible focus states.
- Use accessible contrast and meaningful labels.
- Do not use decorative buttons that do nothing.

---

## 7. Backend integration requirements

The backend already exists as a separate team deliverable. The frontend coding agent must **inspect the actual backend code and API contract before implementing integrations**.

### Integration instructions
1. Inspect the backend repository and identify available endpoints, request/response schemas, authentication requirements, and error formats.
2. Create a centralized API client/service layer.
3. Keep API base URLs and public configuration in environment variables.
4. Do not hardcode backend URLs throughout UI components.
5. Add typed models/interfaces for API responses if the project uses TypeScript.
6. Handle network errors, timeouts, empty results, and loading states.
7. Connect the UI to real endpoints wherever available.
8. Document endpoints or features that are not yet implemented.
9. Never fabricate data to make a backend integration appear complete.

### Important integration rule
Do not assume endpoint names, payload structures, or agent capabilities from this specification. Discover them from the backend and adapt the frontend to the real contract. If an endpoint is missing, create a clearly documented integration placeholder and report it to the team.

---

## 8. Recommended implementation order

Build a coherent end-to-end MVP before implementing every page in depth.

### Phase 1 — Foundation
- Inspect existing frontend repository and preserve its framework/tooling.
- Set up the app shell, sidebar, top bar, routing, theme tokens, and reusable components.
- Establish API client and error/loading handling.

### Phase 2 — Core experience
- Research Workspace.
- Research Agent and Data Agent workflow visibility.
- Connect research question submission to the real backend.
- Display actual investigation/publication results and citations.

### Phase 3 — Data experience
- Datasets Explorer.
- Dataset preview and profile.
- Investigations catalogue.
- Knowledge Base.

### Phase 4 — Results
- Scientific Analysis.
- Research Reports.
- Research History, if persistence is available.

### Phase 5 — Operations and polish
- Agent Center details.
- System Monitoring.
- Settings.
- Responsive behavior, accessibility, testing, and visual refinement.

### MVP priority
If time is limited, prioritize in this order:

1. Research Workspace
2. Agent Center (at least Research Agent and Data Agent)
3. Datasets Explorer
4. Investigations
5. Knowledge Base
6. Scientific Analysis
7. Research Reports
8. Research History
9. System Monitoring
10. Settings

The first five should feel complete and work with real data before polishing lower-priority pages.

---

## 9. Suggested component structure

Adapt this to the existing codebase rather than forcing a new architecture.

```text
src/
  app/
    routes/
    layouts/
  components/
    layout/
      AppSidebar
      Topbar
      PageHeader
    ui/
      Button
      Card
      Badge
      DataTable
      SearchInput
      EmptyState
      LoadingState
      ErrorState
    agents/
      AgentStatus
      AgentWorkflow
      AgentRunDetails
    research/
      ChatPanel
      MessageBubble
      MessageComposer
      CitationList
      ResearchResult
    datasets/
      DatasetTable
      DatasetProfile
      ColumnMetadata
    charts/
  pages/
    ResearchWorkspace
    AgentCenter
    Investigations
    DatasetsExplorer
    ScientificAnalysis
    KnowledgeBase
    ResearchReports
    ResearchHistory
    SystemMonitoring
    Settings
  services/
    apiClient
    researchService
    agentService
    datasetService
    investigationService
    publicationService
    reportService
  types/
  hooks/
  styles/
```

This is a suggested organization, not a requirement to duplicate folders that already exist.

---

## 10. Acceptance checklist

The frontend is ready for team integration when:

### Application foundation
- [ ] App runs using the repository's existing setup.
- [ ] Sidebar navigation and routes work.
- [ ] Shared layout and design tokens are consistent.
- [ ] Responsive behavior is usable.

### Research workflow
- [ ] User can submit a research question to the real backend.
- [ ] Loading, success, empty, and error states work.
- [ ] Research results are rendered clearly.
- [ ] Citations and source links are visible when returned.
- [ ] Agent progress reflects actual backend responses.

### Data and knowledge
- [ ] Investigation catalogue loads from real data.
- [ ] Dataset list loads from real data.
- [ ] Dataset preview displays actual records.
- [ ] Missing values remain missing and are not represented as zero.
- [ ] Publication records and source links are displayed correctly.

### Results and reliability
- [ ] Analysis visualizations use actual returned results.
- [ ] Reports are displayed/exported only when supported.
- [ ] No fake successful actions or fabricated scientific results.
- [ ] Errors are understandable and do not reveal secrets.
- [ ] No major console errors or broken navigation.

---

## 11. Instructions to the coding agent

Before coding:

1. Inspect the current frontend repository, framework, package manager, and existing components.
2. Inspect the backend API and the data files/contracts provided by Member 1 and Member 2.
3. Summarize the existing architecture and identify integration gaps.
4. Propose a short implementation plan that fits the existing codebase.
5. Then implement the frontend incrementally, starting with the app shell and Research Workspace.

During implementation:

- Preserve working code and avoid unnecessary rewrites.
- Do not replace the existing stack without a clear technical reason.
- Do not build a static dashboard that only looks functional.
- Do not invent API endpoints, agent capabilities, scientific findings, or data.
- Use reusable components and keep business/API logic outside presentation components.
- Keep the UI focused and avoid adding features beyond the agreed scope.
- Record any missing backend capability as an integration gap.

### Final expected deliverable

A polished, responsive FLARE AI frontend with a working Research Workspace, transparent agent workflow, real dataset/investigation/publication browsing, and a clear path to scientific analysis and research reports—all integrated with the actual backend contract.
