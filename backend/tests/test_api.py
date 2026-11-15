from fastapi.testclient import TestClient
from app.main import app
import app.main as main

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["real_nasa_data_loaded"] is False


def test_nasa_catalog_is_metadata_only():
    body = client.get("/api/nasa-investigations").json()
    assert {s["family"] for s in body["catalog"]} == {"FLEX", "BASS", "SAFFIRE", "SAME"}
    assert all(not s["data_imported"] for s in body["catalog"])


def test_member1_data_agent_lists_and_profiles_local_csv():
    listed = client.get("/api/datasets?q=bass2").json()["datasets"]
    assert any(item["filename"] == "bass2_tests.csv" for item in listed)
    profile = client.get("/api/datasets/bass2_tests_cleaned.csv/profile")
    assert profile.status_code == 200
    body = profile.json()
    assert body["rows"] == 56
    assert body["path"] == "data/experiments/bass2_tests_cleaned.csv"
    assert "missing_values" in body


def test_member1_research_results_are_attached_to_existing_research_api():
    response = client.post("/api/research", json={
        "question": "What is known about BASS-II?", "group_ids": ["BASS2-TESTS"]
    })
    assert response.status_code == 200
    context = response.json()["research_context"]
    assert context["investigations"]
    assert context["publications"]
    assert "third-party" in context["limitations"]


def test_dataset_profile_rejects_unknown_files():
    assert client.get("/api/datasets/../../README.md/profile").status_code in (404, 422)


def test_openai_answer_uses_local_evidence(monkeypatch):
    monkeypatch.setattr(main, "synthesize_research", lambda question, evidence: "Grounded answer")
    response = client.post("/api/research", json={
        "question": "What is known about BASS-II?", "group_ids": ["BASS2-TESTS"]
    })
    assert response.status_code == 200
    assert response.json()["research_context"]["answer"] == "Grounded answer"
    assert response.json()["research_context"]["agent_status"] == "openai"


def test_research_runs_on_local_csv_and_provenance():
    response = client.post("/api/research", json={
        "question": "Summarize the SAFFIRE dataset measurements",
        "group_ids": ["SAFFIRE-RUNS"]
    })
    assert response.status_code == 200
    result = response.json()
    assert result["analyses"][0]["n_trials"] == 20
    assert result["analyses"][0]["mean_extinction_time_s"] is None
    assert result["analyses"][0]["source_kind"] == "third_party"
    assert result["workflow_trace"] == [
        "member1_research_agent", "member1_csv_data_agent", "scientific_analysis",
        "comparison_ranking", "report_insight"
    ]
    assert "third-party" in result["disclaimer"]
    assert "source_id" in result["report"]


def test_compare_blocks_different_experiment_families():
    response = client.post("/api/compare", json={"group_ids": [
        "BASS2-TESTS", "SAFFIRE-RUNS"
    ]})
    assert response.status_code == 200
    result = response.json()
    assert result["comparison"]["comparable"] is False
    assert result["comparison"]["ranking_by_mean_extinction_time"] == []


def test_unknown_group_is_404():
    response = client.post("/api/research", json={
        "question": "Analyze missing group", "group_ids": ["UNKNOWN"]
    })
    assert response.status_code == 404
