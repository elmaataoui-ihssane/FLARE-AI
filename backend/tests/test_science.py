from app.adapters.member1 import read_groups
from app.agents.scientific_analysis import analyze_group
from app.agents.comparison import compare_groups
from app.models import ExperimentGroup


def test_analysis_uses_real_local_dataset_rows_and_keeps_missing_values():
    group = read_groups(["LUCI-RUNS"])[0]
    result = analyze_group(group)
    spread = next(item for item in result.measurements if item.metric == "spread_base_mm_s")
    assert result.mean_extinction_time_s is None
    assert result.n_trials == 2
    assert result.source_kind == "third_party"
    assert (spread.mean, spread.n_trials, spread.n_missing, spread.unit) == (0.92, 1, 1, "mm/s")


def test_comparison_blocks_incompatible_conditions():
    one, two = read_groups(["BASS2-TESTS", "SAFFIRE-RUNS"])
    modified = two.model_copy(deep=True)
    modified.conditions.gravity = "lunar_gravity"
    result = compare_groups([one, modified], [analyze_group(one), analyze_group(modified)])
    assert result.comparable is False
    assert result.ranking_by_mean_extinction_time == []


def test_real_nasa_records_need_a_measurement_source():
    group = read_groups(["BASS2-TESTS"])[0].model_dump()
    group["source_kind"] = "nasa"
    from pydantic import ValidationError
    import pytest
    with pytest.raises(ValidationError):
        ExperimentGroup.model_validate(group)
