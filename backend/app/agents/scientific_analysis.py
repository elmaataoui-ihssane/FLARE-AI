"""Scientific calculations are deterministic; LLM does not perform numerical math."""
from statistics import mean, median, stdev
from app.models import AnalysisResult, ExperimentGroup, MetricSummary


def summarize_measurement(group: ExperimentGroup, measurement_name: str) -> MetricSummary:
    """Summarize a numeric variable only when every recorded unit agrees.

    Missing values are excluded but counted. No automatic unit conversion or
    scientific inference is attempted.
    """
    readings = [t.measurements[measurement_name] for t in group.trials
                if measurement_name in t.measurements]
    recorded_non_numeric = sum(
        measurement_name in t.metadata and t.metadata[measurement_name] is not None
        and measurement_name not in t.measurements for t in group.trials
    )
    n_missing = len(group.trials) - len(readings) - recorded_non_numeric
    if not readings:
        return MetricSummary(metric=measurement_name,n_trials=0,n_missing=n_missing,
                             status='insufficient_data',note=f'No numeric observations; {recorded_non_numeric} non-scalar source values retained in row metadata')
    units = {r.unit for r in readings}
    if len(units) != 1:
        return MetricSummary(metric=measurement_name,n_trials=len(readings),n_missing=n_missing,
                             status='incompatible_units',note=f'Units differ: {", ".join(sorted(units))}')
    values = [r.value for r in readings]
    return MetricSummary(metric=measurement_name,unit=readings[0].unit,
        n_trials=len(values),n_missing=n_missing,
        mean=round(mean(values),3),median=round(median(values),3),
        std_dev=round(stdev(values),3) if len(values)>=2 else None,
        minimum=min(values),maximum=max(values),status='ok',
        note=f'{recorded_non_numeric} non-scalar source values retained in row metadata' if recorded_non_numeric else None)


def analyze_group(group: ExperimentGroup) -> AnalysisResult:
    values = [t.extinction_time_s for t in group.trials if t.extinction_time_s is not None]
    metrics = sorted({key for t in group.trials for key in t.measurements})
    summaries = [summarize_measurement(group, m) for m in metrics]
    has_data = bool(values) or any(s.status=='ok' for s in summaries)
    return AnalysisResult(
        group_id=group.group_id,n_trials=len(group.trials),
        mean_extinction_time_s=round(mean(values),3) if values else None,
        median_extinction_time_s=round(median(values),3) if values else None,
        std_dev_extinction_time_s=round(stdev(values),3) if len(values)>=2 else None,
        min_extinction_time_s=min(values) if values else None,
        max_extinction_time_s=max(values) if values else None,
        measurements=summaries,source_kind=group.source_kind,
        data_source_url=str(group.data_source_url) if group.data_source_url else None,
        status='ok' if has_data else 'insufficient_data')
