from fastapi.testclient import TestClient
from app.main import app
from app.adapters.member1 import read_groups
from app.agents.scientific_analysis import analyze_group, summarize_measurement
from app.models import Measurement, Trial

client=TestClient(app)

def test_multivariate_mean_and_sd():
    group=read_groups(['FLEX-DEMO-A'])[0].model_copy(deep=True)
    for trial,value in zip(group.trials,[800,900,1000]):
        trial.measurements['flame_temperature']=Measurement(value=value,unit='K')
    result=analyze_group(group)
    m=next(item for item in result.measurements if item.metric=='flame_temperature')
    assert (m.metric,m.mean,m.median,m.std_dev,m.unit)==('flame_temperature',900,900,100,'K')
    assert result.mean_extinction_time_s==10

def test_missing_values_and_units():
    group=read_groups(['FLEX-DEMO-A'])[0].model_copy(deep=True)
    group.trials[0].measurements['diameter']=Measurement(value=3,unit='mm')
    summary=summarize_measurement(group,'diameter')
    assert summary.n_missing==2 and summary.std_dev is None
    group.trials[1].measurements['diameter']=Measurement(value=0.5,unit='cm')
    summary=summarize_measurement(group,'diameter')
    assert summary.status=='incompatible_units'
    assert summary.mean is None

def test_optional_extinction_time():
    t=Trial(trial_id='X',measurements={'size':{'value':2,'unit':'mm'}})
    assert t.extinction_time_s is None

def test_validate_dataset_endpoint():
    g=read_groups(['FLEX-DEMO-A'])[0]
    r=client.post('/api/validate-dataset',json={'groups':[g.model_dump(mode='json')]})
    assert r.status_code==200 and r.json()['valid'] is True

def test_example_openapi_valid():
    s=client.get('/openapi.json').json()
    assert s['info']['version']=='0.2.0'
    assert '/api/research' in s['paths']

def test_research_multivariate_response():
    body=client.post('/api/research',json={'question':'Analyze measurements in FLEX demo','group_ids':['FLEX-DEMO-A']}).json()
    assert {m['metric'] for m in body['analyses'][0]['measurements']}=={'flame_temperature','flame_diameter'}
    assert body['analyses'][0]['status']=='ok'
