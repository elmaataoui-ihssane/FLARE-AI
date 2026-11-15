from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["real_nasa_data_loaded"] is False


def test_nasa_catalog_is_metadata_only():
    body = client.get("/api/nasa-investigations").json()
    assert {s["family"] for s in body["catalog"]} == {"FLEX", "BASS", "SAFFIRE"}
    assert all(not s["data_imported"] for s in body["catalog"])


def test_research_produces_trace_and_provenance():
    response = client.post("/api/research", json={
        "question": "What is the average extinction time in this demo?",
        "group_ids": ["FLEX-DEMO-A"]
    })
    assert response.status_code == 200
    result = response.json()
    assert result["analyses"][0]["mean_extinction_time_s"] == 10.0
    assert result["workflow_trace"] == [
        "research_adapter_demo", "data_adapter_demo", "scientific_analysis",
        "comparison_ranking", "report_insight"
    ]
    assert "synthetic" in result["disclaimer"]
    assert "DEMO ONLY" in result["report"]


def test_compare_two_synthetic_conditions():
    response = client.post("/api/compare", json={"group_ids": [
        "FLEX-DEMO-A", "FLEX-DEMO-B"
    ]})
    assert response.status_code == 200
    result = response.json()
    assert result["comparison"]["comparable"] is True
    assert result["comparison"]["ranking_by_mean_extinction_time"] == [
        "FLEX-DEMO-A", "FLEX-DEMO-B"
    ]


def test_unknown_group_is_404():
    response = client.post("/api/research", json={
        "question": "Analyze missing group", "group_ids": ["UNKNOWN"]
    })
    assert response.status_code == 404
