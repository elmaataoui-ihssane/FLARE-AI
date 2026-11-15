"""Evidence-aware template report, not an LLM research conclusion."""
from app.models import AnalysisResult, ComparisonResult, ExperimentGroup

def write_report(groups: list[ExperimentGroup],analyses: list[AnalysisResult],comparison: ComparisonResult | None)->str:
    lines=['FLARE AI | descriptive scientific report']
    for group,analysis in zip(groups,analyses):
        lines.append(f'{group.group_id} ({group.source_kind}):')
        if analysis.mean_extinction_time_s is None:
            lines.append('  extinction time: not available')
        else:
            lines.append(f'  extinction time mean={analysis.mean_extinction_time_s} s, '
                         f'median={analysis.median_extinction_time_s} s, '
                         f'n={analysis.n_trials}; sample SD={analysis.std_dev_extinction_time_s} s')
        for measure in analysis.measurements:
            if measure.status=='ok':
                lines.append(f'  {measure.metric}: mean={measure.mean} {measure.unit}, '
                             f'n={measure.n_trials}, missing={measure.n_missing}')
            else:
                lines.append(f'  {measure.metric}: {measure.status}: {measure.note}')
        if group.source_kind=='nasa':
            lines.append(f'  Source of measurements: {group.data_source_url}')
        else:
            lines.append('  DEMO ONLY: SYNTHETIC DATA — NO NASA MEASUREMENTS')
    if comparison is not None:
        lines.append(f'Comparison: {comparison.reason}')
        if comparison.comparable:
            lines.append('Ranking: '+' < '.join(comparison.ranking_by_mean_extinction_time))
            lines.append(comparison.ranking_meaning)
    lines.append('NASA investigation descriptions are contextual sources, not evidence for synthetic numbers.')
    lines.append('No operational spacecraft fire-safety advice or certified prediction.')
    return '\n'.join(lines)
