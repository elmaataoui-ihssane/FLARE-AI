"""Conservative descriptive comparison; no certified safety inference."""
from app.models import AnalysisResult, ComparisonResult, ExperimentGroup


def compare_groups(groups: list[ExperimentGroup], analyses: list[AnalysisResult]) -> ComparisonResult | None:
    if len(groups)<2:
        return None
    first=groups[0]
    controls=('gravity','fuel_type','oxygen_percent','pressure_kpa')
    for other in groups[1:]:
        if (other.source_kind != first.source_kind or
            other.experiment_family != first.experiment_family or
            any(getattr(other.conditions,c)!=getattr(first.conditions,c) for c in controls)):
            return ComparisonResult(comparable=False,
                reason='Source category, family or control conditions differ; ranking blocked.')
    if len(analyses)!=len(groups) or any(a.mean_extinction_time_s is None for a in analyses):
        return ComparisonResult(comparable=False,
            reason='Extinction-time measurements missing for one or more groups.')
    ranked=sorted(analyses,key=lambda a:a.mean_extinction_time_s)
    return ComparisonResult(comparable=True,
        reason='Recorded controls match; descriptive extinction-time ranking only.',
        ranking_by_mean_extinction_time=[a.group_id for a in ranked],
        ranking_meaning='Ascending mean extinction time; not a fire-safety recommendation, causality, or statistical significance claim.')
