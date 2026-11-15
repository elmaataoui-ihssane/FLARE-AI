from fastapi.testclient import TestClient
from app.main import app
from app.adapters.member1 import read_groups
from app.agents.scientific_analysis import analyze_group, summarize_measurement
from app.models import Measurement, Trial

client = TestClient(app)


def test_multivariate_analysis_uses_saffire_csv_metrics():
    group = read_groups(["SAFFIRE-RUNS"])[0]
    result = analyze_group(group)
    assert result.n_trials == 20
    assert result.source_kind == "third_party"
    assert "spread_rate_mm_s" in {item.metric for item in result.measurements}


def test_missing_values_and_units_are_retained():
    group = read_groups(["BASS2-TESTS"])[0].model_copy(deep=True)
    summary = summarize_measurement(group, "flow_final_cm_s")
    assert summary.n_trials + summary.n_missing == 56
    assert summary.n_missing > 0
    group.trials[0].measurements["diameter"] = Measurement(value=3, unit="mm")
    group.trials[1].measurements["diameter"] = Measurement(value=0.5, unit="cm")
    summary = summarize_measurement(group, "diameter")
    assert summary.status == "incompatible_units"
    assert summary.mean is None


def test_optional_extinction_time_and_original_row_metadata():
    group = read_groups(["LUCI-RUNS"])[0]
    assert group.trials[0].extinction_time_s is None
    assert group.trials[0].metadata["source_id"] == "luci"
    assert group.trials[0].metadata["outcome_quote"]


def test_validate_dataset_endpoint_accepts_third_party_provenance():
    group = read_groups(["BASS2-TESTS"])[0]
    response = client.post('/api/validate-dataset', json={'groups': [group.model_dump(mode='json')]})
    assert response.status_code == 200 and response.json()['valid'] is True


def test_openapi_and_research_examples_use_project_dataset_ids():
    schema = client.get('/openapi.json').json()
    assert schema['info']['version'] == '0.2.0'
    assert '/api/research' in schema['paths']
    assert 'SAFFIRE-RUNS' in str(schema['components']['schemas']['ResearchRequest'])


def test_research_response_analyzes_supplied_csv_group():
    body = client.post('/api/research', json={
        'question': 'Summarize measured spread rates in SAFFIRE',
        'group_ids': ['SAFFIRE-RUNS'],
    }).json()
    assert body['analyses'][0]['n_trials'] == 20
    assert {m['metric'] for m in body['analyses'][0]['measurements']} >= {'spread_rate_mm_s', 'burn_duration_s'}
    assert body['analyses'][0]['source_kind'] == 'third_party'
