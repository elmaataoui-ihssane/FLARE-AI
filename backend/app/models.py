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
    oxygen_percent: float | None = Field(default=None, ge=0, le=100)
    pressure_kpa: float | None = Field(default=None, gt=0)
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
    metadata: dict[str, object] = Field(default_factory=dict, description='Original row values, labels, and source references')

class ExperimentGroup(BaseModel):
    group_id: str
    experiment_family: str
    title: str
    source_kind: Literal['synthetic','nasa','third_party']
    nasa_background_url: HttpUrl | None = None
    data_source_url: HttpUrl | None = None
    conditions: Conditions
    trials: list[Trial] = Field(default_factory=list)
    provenance: dict[str, object] = Field(default_factory=dict)
    @model_validator(mode='after')
    def require_evidence_for_real_data(self):
        if self.source_kind in ('nasa', 'third_party') and self.data_source_url is None:
            raise ValueError('Non-synthetic measurements need a data_source_url')
        if self.source_kind == 'nasa' and self.data_source_url is not None:
            host = self.data_source_url.host.casefold()
            if host != 'nasa.gov' and not host.endswith('.nasa.gov'):
                raise ValueError('NASA measurements need a NASA-hosted data_source_url')
        return self

class ResearchRequest(BaseModel):
    question: str = Field(min_length=5)
    group_ids: list[str] = Field(min_length=1)
    model_config = {'json_schema_extra': {'example': {
        'question':'Summarize the measured spread rates in SAFFIRE', 'group_ids':['SAFFIRE-RUNS']
    }}}

class CompareRequest(BaseModel):
    group_ids: list[str] = Field(min_length=2)
    question: str = 'Compare extinction times between experimental groups'
    model_config = {'json_schema_extra': {'example': {
        'question':'Compare extinction times between experimental groups',
        'group_ids':['SAFFIRE-RUNS','LUCI-RUNS']
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
    source_kind: Literal['synthetic','nasa','third_party']
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
    research_context: dict = Field(default_factory=dict)

class DatasetValidationRequest(BaseModel):
    groups: list[ExperimentGroup] = Field(min_length=1)
