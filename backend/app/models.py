"""Shared API contract for Members 1, 2 and 3.

The shapes are provisional until team approval. NASA source metadata is NOT a
substitute for an actual experimental data source.
"""
from typing import Literal
from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator
import math

class Conditions(BaseModel):
    gravity: str
    fuel_type: str
    oxygen_percent: float = Field(ge=0, le=100)
    pressure_kpa: float = Field(gt=0)
    suppression_case: str

class Measurement(BaseModel):
    value: float
    unit: str = Field(min_length=1)
    @field_validator('value')
    @classmethod
    def reject_nan_inf(cls, value: float) -> float:
        if not math.isfinite(value):
            raise ValueError('Measurement must be finite')
        return value

class Trial(BaseModel):
    trial_id: str
    extinction_time_s: float | None = Field(default=None, ge=0, description='Seconds; optional if not measured')
    measurements: dict[str, Measurement] = Field(default_factory=dict)

class ExperimentGroup(BaseModel):
    group_id: str
    experiment_family: str
    title: str
    source_kind: Literal['synthetic','nasa']
    nasa_background_url: HttpUrl | None = None
    data_source_url: HttpUrl | None = None
    conditions: Conditions
    trials: list[Trial] = Field(default_factory=list)
    @model_validator(mode='after')
    def require_evidence_for_real_data(self):
        if self.source_kind == 'nasa' and self.data_source_url is None:
            raise ValueError('Real NASA measurements need a data_source_url')
        return self

class ResearchRequest(BaseModel):
    question: str = Field(min_length=5)
    group_ids: list[str] = Field(min_length=1)
    model_config = {'json_schema_extra': {'example': {
        'question':'Analyze the extinction time of FLEX', 'group_ids':['FLEX-DEMO-A']
    }}}

class CompareRequest(BaseModel):
    group_ids: list[str] = Field(min_length=2)
    question: str = 'Compare extinction times between experimental groups'
    model_config = {'json_schema_extra': {'example': {
        'question':'Compare extinction times between experimental groups',
        'group_ids':['FLEX-DEMO-A','FLEX-DEMO-B']
    }}}

class MetricSummary(BaseModel):
    metric: str
    unit: str | None = None
    n_trials: int
    n_missing: int
    mean: float | None = None
    median: float | None = None
    std_dev: float | None = None
    minimum: float | None = None
    maximum: float | None = None
    status: Literal['ok','insufficient_data','incompatible_units']
    note: str | None = None

class AnalysisResult(BaseModel):
    group_id: str
    n_trials: int
    mean_extinction_time_s: float | None = None
    median_extinction_time_s: float | None = None
    std_dev_extinction_time_s: float | None = None
    min_extinction_time_s: float | None = None
    max_extinction_time_s: float | None = None
    measurements: list[MetricSummary] = Field(default_factory=list)
    source_kind: Literal['synthetic','nasa']
    data_source_url: str | None = None
    status: Literal['ok','insufficient_data']

class ComparisonResult(BaseModel):
    comparable: bool
    reason: str
    ranking_by_mean_extinction_time: list[str] = Field(default_factory=list)
    ranking_meaning: str = 'Descriptive ranking only; no safety conclusion.'

class ResearchResponse(BaseModel):
    question: str
    data_source: str
    analyses: list[AnalysisResult]
    comparison: ComparisonResult | None = None
    report: str
    workflow_trace: list[str]
    disclaimer: str

class DatasetValidationRequest(BaseModel):
    groups: list[ExperimentGroup] = Field(min_length=1)
