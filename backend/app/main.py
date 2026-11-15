"""FLARE AI backend — dataset-backed analysis with source-aware reporting."""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.adapters.member1 import read_groups, research_agent, data_agent
from app.catalog import INVESTIGATIONS
from app.models import CompareRequest,ResearchRequest,ResearchResponse,DatasetValidationRequest
from app.agents.openai_research import configured as openai_configured, model_name, synthesize_research
from app.workflows.flare_graph import flare_graph, LANGGRAPH_AVAILABLE

app=FastAPI(title='FLARE AI — Scientific Backend (Member 2)',
    description='Scientific analysis and evidence-aware reports for NASA Space Apps Flame in Freefall',
    version='0.2.0')
origins=[x.strip() for x in os.getenv('CORS_ALLOWED_ORIGINS','http://localhost:3000,http://127.0.0.1:3000').split(',') if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=False,
                   allow_methods=['GET','POST'],allow_headers=['Content-Type'])

@app.get('/api/health')
def health():
    groups=read_groups()
    kinds={g.source_kind for g in groups}
    mode='synthetic_demo' if kinds=={'synthetic'} else 'third_party_datasets' if kinds=={'third_party'} else 'mixed_sources'
    return {'status':'ok','workflow_engine':'langgraph' if LANGGRAPH_AVAILABLE else 'offline_fallback',
            'mode':mode,
            'real_nasa_data_loaded':any(g.source_kind=='nasa' for g in groups),
            'datasets_loaded':[g.group_id for g in groups],
            'openai_agent_configured':openai_configured(),
            'openai_model':model_name() if openai_configured() else None}

@app.get('/api/nasa-investigations')
def investigations():
    return {'catalog':INVESTIGATIONS,'note':'NASA investigation metadata and third-party references provide context only; they are not measurement evidence.'}

@app.get('/api/datasets')
def datasets(q: str | None = None):
    """List available raw and processed files; optionally search by filename."""
    return {'datasets': data_agent.search_files(q) if q else data_agent.list_datasets(),
            'data_root': 'data/',
            'note': 'Raw source files are preserved. Processed CSVs are exposed separately.'}

@app.get('/api/datasets/compare')
def compare_datasets(dataset_a: str, dataset_b: str):
    try:
        return data_agent.compare_datasets(dataset_a, dataset_b)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@app.get('/api/datasets/{filename}/profile')
def profile_dataset(filename: str):
    try:
        return data_agent.profile_dataset(filename)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@app.get('/api/experiments')
def experiments():
    groups=read_groups()
    return {'groups':[g.model_dump(mode='json') for g in groups],
            'notice':'Groups load from cleaned project CSVs. MicroFire Atlas is third-party; row-level source IDs and PDF pages are retained in trial metadata.'}

@app.post('/api/validate-dataset')
def validate_dataset(payload:DatasetValidationRequest):
    ids=[g.group_id for g in payload.groups]
    if len(ids)!=len(set(ids)):
        raise HTTPException(status_code=422,detail='Duplicate group IDs')
    return {'valid':True,'groups':len(ids),'group_ids':ids,
            'note':'Schema validation only; scientific authenticity requires manual source review.'}

def _run(question:str,group_ids:list[str])->ResearchResponse:
    try:
        state=flare_graph.invoke({'question':question,'group_ids':group_ids,'trace':[]})
    except ValueError as exc:
        raise HTTPException(status_code=404,detail=str(exc)) from exc
    sources=sorted({g.source_kind for g in state['groups']})
    context = state.get('research_context') or research_agent.research(question)
    context['dataset_analyses'] = [analysis.model_dump(mode='json') for analysis in state['analyses']]
    context['dataset_sources'] = []
    for group in state['groups']:
        references = []
        seen = set()
        for trial in group.trials:
            record = {key: trial.metadata.get(key) for key in
                      ('id', 'source_id', 'pdf_page', 'conditions_source', 'conditions_pdf_page',
                       'results_source', 'results_pdf_page', 'outcome_pdf_page')
                      if trial.metadata.get(key) is not None}
            signature = tuple(sorted(record.items()))
            if record and signature not in seen:
                references.append(record)
                seen.add(signature)
            if len(references) >= 8:
                break
        context['dataset_sources'].append({
            'group_id': group.group_id, 'experiment_family': group.experiment_family,
            'data_source_url': str(group.data_source_url), 'provenance': group.provenance,
            'record_references': references,
        })
    try:
        answer = synthesize_research(question, context)
        context['agent_status'] = ('openai' if answer else
                                   'openai_empty_response' if openai_configured() else 'not_configured')
        context['agent_model'] = model_name() if openai_configured() else None
        context['answer'] = answer
    except Exception:
        # A model/API outage must not make the deterministic local workflow unavailable.
        context['agent_status'] = 'error_local_evidence_only'
        context['agent_model'] = model_name()
        context['answer'] = None
        context['agent_note'] = 'OpenAI synthesis failed; local search results are still available.'
    return ResearchResponse(question=question,data_source=', '.join(sources),
        analyses=state['analyses'],comparison=state['comparison'],report=state['report'],
        workflow_trace=state['trace'],
        disclaimer='Analyses summarize the selected local dataset rows. The datasets were provided through the third-party MicroFire Atlas; preserved NASA source IDs and page references are provenance leads, not independent verification. Dataset-wide statistics do not imply matched controls, causality, or safety conclusions.',
        research_context=context)

@app.post('/api/research',response_model=ResearchResponse)
def research(payload:ResearchRequest):
    return _run(payload.question,payload.group_ids)

@app.post('/api/compare',response_model=ResearchResponse)
def compare(payload:CompareRequest):
    return _run(payload.question,payload.group_ids)
