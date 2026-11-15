"""Member 2 LangGraph workflow.

The first two nodes are local substitutes for Member 1's agents.
Other nodes are deterministic processing components, not autonomous LLMs yet.
"""
from typing import TypedDict
try:
    from langgraph.graph import StateGraph, START, END
    LANGGRAPH_AVAILABLE = True
except ModuleNotFoundError:
    # Local offline test runner; production/normal installation uses LangGraph.
    StateGraph = None
    START = END = None
    LANGGRAPH_AVAILABLE = False
from app.adapters.member1 import read_groups
from app.agents.scientific_analysis import analyze_group
from app.agents.comparison import compare_groups
from app.agents.report import write_report
from app.models import ExperimentGroup, AnalysisResult, ComparisonResult


class FLAREState(TypedDict, total=False):
    question: str
    group_ids: list[str]
    groups: list[ExperimentGroup]
    analyses: list[AnalysisResult]
    comparison: ComparisonResult | None
    report: str
    trace: list[str]


def _trace(state: FLAREState, name: str) -> list[str]:
    return [*state.get("trace", []), name]


def research_adapter(state: FLAREState) -> dict:
    # Real Research Agent will select documents and experiments.
    return {"trace": _trace(state, "research_adapter_demo")}


def data_adapter(state: FLAREState) -> dict:
    groups = read_groups(state["group_ids"])
    return {"groups": groups, "trace": _trace(state, "data_adapter_demo")}


def scientific_agent(state: FLAREState) -> dict:
    analyses = [analyze_group(g) for g in state["groups"]]
    return {"analyses": analyses, "trace": _trace(state, "scientific_analysis")}


def comparison_agent(state: FLAREState) -> dict:
    result = compare_groups(state["groups"], state["analyses"])
    return {"comparison": result, "trace": _trace(state, "comparison_ranking")}


def report_agent(state: FLAREState) -> dict:
    report = write_report(state["groups"], state["analyses"], state["comparison"])
    return {"report": report, "trace": _trace(state, "report_insight")}


class _OfflineSequentialRunner:
    """Offline-only fallback for verifying agent functions without LangGraph."""
    def invoke(self, state: FLAREState) -> FLAREState:
        result = dict(state)
        for node in (
            research_adapter, data_adapter, scientific_agent, comparison_agent, report_agent
        ):
            result.update(node(result))
        return result


def build_graph():
    if not LANGGRAPH_AVAILABLE:
        return _OfflineSequentialRunner()
    builder = StateGraph(FLAREState)
    builder.add_node("research", research_adapter)
    builder.add_node("data", data_adapter)
    builder.add_node("science", scientific_agent)
    builder.add_node("comparison", comparison_agent)
    builder.add_node("report", report_agent)
    builder.add_edge(START, "research")
    builder.add_edge("research", "data")
    builder.add_edge("data", "science")
    builder.add_edge("science", "comparison")
    builder.add_edge("comparison", "report")
    builder.add_edge("report", END)
    return builder.compile()


flare_graph = build_graph()
