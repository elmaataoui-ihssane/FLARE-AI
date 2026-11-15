"""FLARE AI backend — honest synthetic demo + provenance-aware data contract."""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.adapters.member1 import read_groups
from app.catalog import INVESTIGATIONS
from app.models import CompareRequest,ResearchRequest,ResearchResponse,DatasetValidationRequest
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
    return {'status':'ok','workflow_engine':'langgraph' if LANGGRAPH_AVAILABLE else 'offline_fallback',
            'mode':'synthetic_demo' if all(g.source_kind=='synthetic' for g in groups) else 'mixed_or_nasa',
            'real_nasa_data_loaded':any(g.source_kind=='nasa' for g in groups)}

@app.get('/api/nasa-investigations')
def investigations():
    return {'catalog':INVESTIGATIONS,'note':'NASA descriptions only; no real numeric data imported by default.'}

@app.get('/api/experiments')
def experiments():
    groups=read_groups()
    return {'groups':[g.model_dump(mode='json') for g in groups],
            'notice':'Each group contains its own source_kind; demo groups are synthetic.'}

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
    return ResearchResponse(question=question,data_source=', '.join(sources),
        analyses=state['analyses'],comparison=state['comparison'],report=state['report'],
        workflow_trace=state['trace'],
        disclaimer='Numerical outputs are synthetic unless an independently verified NASA dataset is supplied; investigation links alone are context.')

@app.post('/api/research',response_model=ResearchResponse)
def research(payload:ResearchRequest):
    return _run(payload.question,payload.group_ids)

@app.post('/api/compare',response_model=ResearchResponse)
def compare(payload:CompareRequest):
    return _run(payload.question,payload.group_ids)
