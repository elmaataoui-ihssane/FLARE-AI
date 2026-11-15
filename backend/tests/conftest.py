import pytest

import app.main as main


@pytest.fixture(autouse=True)
def stub_openai_for_tests(monkeypatch):
    """Keep the suite offline and avoid making billable model calls in tests."""
    monkeypatch.setattr(main, "synthesize_research", lambda question, evidence: "Test synthesis from local evidence.")
