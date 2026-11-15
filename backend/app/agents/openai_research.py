"""Grounded, optional OpenAI synthesis over the local ResearchAgent results."""
import json
import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


@lru_cache(maxsize=1)
def _client() -> OpenAI | None:
    if not os.getenv("OPENAI_API_KEY"):
        return None
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"], timeout=30.0, max_retries=0)


def configured() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))


def model_name() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def synthesize_research(question: str, evidence: dict) -> str | None:
    """Answer from retrieved local evidence only; return None when not configured."""
    client = _client()
    if client is None:
        return None

    # Keep prompts focused and avoid sending the full source manifest or datasets.
    context = {
        "investigations": evidence.get("investigations", [])[:5],
        "publications": evidence.get("publications", [])[:5],
        "findings": evidence.get("findings", [])[:8],
        "dataset_analyses": evidence.get("dataset_analyses", []),
        "dataset_sources": evidence.get("dataset_sources", []),
        "limitations": evidence.get("limitations"),
    }
    response = client.responses.create(
        model=model_name(),
        instructions=(
            "You are FLARE AI's research assistant. Answer the question using only the supplied "
            "local evidence. Do not claim that third-party MicroFire Atlas data is NASA-verified. "
            "Distinguish publication records, investigation descriptions, reported findings, and "
            "dataset summary statistics. Cite available titles, identifiers, source IDs, URLs, and PDF pages. If evidence is "
            "insufficient, say so. Do not give operational spacecraft fire-safety instructions."
        ),
        input=(f"Question: {question}\n\nRetrieved evidence (JSON):\n"
               f"{json.dumps(context, ensure_ascii=False, default=str)}"),
        max_output_tokens=500,
    )
    return response.output_text.strip() or None
