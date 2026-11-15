from app.adapters.member1 import read_groups
from app.agents.scientific_analysis import analyze_group
from app.agents.comparison import compare_groups
from app.models import ExperimentGroup


def test_mean_is_deterministic_and_synthetic():
    group = read_groups(["FLEX-DEMO-A"])[0]
    result = analyze_group(group)
    assert result.mean_extinction_time_s == 10.0
    assert result.n_trials == 3
    assert result.source_kind == "synthetic"


def test_comparison_blocks_incompatible_conditions():
    one, two = read_groups()
    modified = two.model_copy(deep=True)
    modified.conditions.gravity = "lunar_gravity"
    result = compare_groups([one, modified], [analyze_group(one), analyze_group(modified)])
    assert result.comparable is False
    assert result.ranking_by_mean_extinction_time == []


def test_real_nasa_records_need_a_measurement_source():
    group = read_groups()[0].model_dump()
    group["source_kind"] = "nasa"
    from pydantic import ValidationError
    import pytest
    with pytest.raises(ValidationError):
        ExperimentGroup.model_validate(group)
