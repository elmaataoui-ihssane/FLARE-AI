"""Runtime adapters for Member 1's local research and dataset assets.

Paths are rooted at the repository's data directory, never the process CWD.
MicroFire Atlas records remain third-party evidence unless independently verified.
"""
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

from app.models import ExperimentGroup

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_ROOT = PROJECT_ROOT / "data"
RAW_ROOT = DATA_ROOT / "raw"
EXPERIMENTS_ROOT = DATA_ROOT / "experiments"
MICROFIRE_ROOT = RAW_ROOT / "microfire_atlas"

DATASET_CONFIG = {
    "BASS2-TESTS": {
        "file": "bass2_tests_cleaned.csv", "family": "BASS-II",
        "title": "BASS-II extracted test records", "url": "https://microfire-atlas.vercel.app/downloads/bass2-tests.csv",
        "units": {"thickness_mm": "mm", "width_mm": "mm", "flow_initial_cm_s": "cm/s",
                  "flow_final_cm_s": "cm/s", "oxygen_vol_pct": "% vol", "pressure_kpa": "kPa"},
    },
    "LUCI-RUNS": {
        "file": "luci_runs_cleaned.csv", "family": "LUCI",
        "title": "Lunar Combustion Investigation runs", "url": "https://microfire-atlas.vercel.app/downloads/luci-runs.csv",
        "units": {"o2_start_pct": "%", "o2_end_pct": "%", "pressure_kpa": "kPa",
                  "spread_base_mm_s": "mm/s", "spread_tip_mm_s": "mm/s"},
    },
    "SAFFIRE-RUNS": {
        "file": "saffire_runs_cleaned.csv", "family": "SAFFIRE",
        "title": "SAFFIRE spacecraft fire experiment runs", "url": "https://microfire-atlas.vercel.app/downloads/saffire-runs.csv",
        "units": {"thickness_mm": "mm", "width_cm": "cm", "length_cm": "cm",
                  "flow_cm_s": "cm/s", "pressure_kpa": "kPa", "o2_pct": "%",
                  "burn_duration_s": "s", "spread_rate_mm_s": "mm/s",
                  "heat_release_avg_w": "W", "heat_release_peak_w": "W"},
    },
}

INVESTIGATIONS = [
    {"name": "BASS-II", "psi_id": "PSI-25", "topic": "Solid fuel combustion", "priority": 1,
     "url": "https://psi.nasa.gov/physci/repo/data/investigations/PSI-25"},
    {"name": "FLEX", "psi_id": "PSI-69", "topic": "Droplet combustion", "priority": 1,
     "url": "https://psi.nasa.gov/physci/repo/data/investigations/PSI-69"},
    *[{"name": f"SAFFIRE-{edition}", "psi_id": f"PSI-{number}",
       "topic": "Spacecraft fire safety", "priority": 1,
       "url": f"https://psi.nasa.gov/physci/repo/data/investigations/PSI-{number}"}
      for edition, number in [("I", 98), ("II", 99), ("III", 100)]],
    {"name": "SAME-R", "psi_id": "PSI-101", "topic": "Smoke and aerosols", "priority": 2,
     "url": "https://psi.nasa.gov/physci/repo/data/investigations/PSI-101"},
    {"name": "SAME", "psi_id": "PSI-102", "topic": "Smoke and aerosols", "priority": 2,
     "url": "https://psi.nasa.gov/physci/repo/data/investigations/PSI-102"},
]


def read_groups(ids: list[str] | None = None) -> list[ExperimentGroup]:
    """Load experiment groups directly from Member 1's cleaned CSV datasets."""
    groups = []
    for group_id, config in DATASET_CONFIG.items():
        path = EXPERIMENTS_ROOT / config["file"]
        if not path.is_file():
            raise FileNotFoundError(f"Required processed dataset is missing: {path.relative_to(PROJECT_ROOT)}")
        frame = pd.read_csv(path)
        metrics = config["units"]
        trials = []
        for row_index, row in frame.iterrows():
            values = {str(key): (None if pd.isna(value) else value.item() if hasattr(value, "item") else value)
                      for key, value in row.items()}
            measurements = {}
            for column, unit in metrics.items():
                value = row.get(column)
                if value is not None and not pd.isna(value):
                    numeric_value = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
                    if not pd.isna(numeric_value):
                        measurements[column] = {"value": float(numeric_value), "unit": unit}
            trial_id = str(values.get("id") or f"{group_id}-{row_index + 1}")
            trials.append({"trial_id": trial_id, "measurements": measurements, "metadata": values})
        groups.append(ExperimentGroup.model_validate({
            "group_id": group_id, "experiment_family": config["family"],
            "title": config["title"], "source_kind": "third_party",
            "data_source_url": config["url"],
            "conditions": {"gravity": "varies_or_not_recorded_per_row",
                           "fuel_type": "varies_by_row", "oxygen_percent": None,
                           "pressure_kpa": None, "suppression_case": "not_a_controlled_group"},
            "trials": trials,
            "provenance": {"provider": "MicroFire Atlas (third-party dataset)",
                           "processed_file": path.relative_to(PROJECT_ROOT).as_posix(),
                           "original_file": (MICROFIRE_ROOT / config["file"].replace("_cleaned", "")).relative_to(PROJECT_ROOT).as_posix(),
                           "source_references_in_row_fields": [key for key in ("source_id", "pdf_page", "conditions_source", "conditions_pdf_page", "results_source", "results_pdf_page", "outcome_pdf_page") if key in frame.columns],
                           "non_numeric_cells": "Range strings and other non-scalar cells remain unchanged in trial metadata and are excluded from numeric summaries.",
                           "summary_scope": "Descriptive summaries across dataset rows; rows may have different experimental conditions. No treatment effect or causal comparison is implied."},
        }))
    by_id = {g.group_id: g for g in groups}
    if len(by_id) != len(groups):
        raise ValueError("Duplicate group IDs in dataset")
    if ids is None:
        return groups
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate group IDs are not allowed")
    missing = [name for name in ids if name not in by_id]
    if missing:
        raise ValueError("Unknown group IDs: " + ", ".join(missing))
    return [by_id[name] for name in ids]


class ResearchAgent:
    """Notebook ResearchAgent backed by committed NASA/Atlas source records."""
    def __init__(self) -> None:
        self.investigations = INVESTIGATIONS
        manifest = MICROFIRE_ROOT / "source_manifest.json"
        records = json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else []
        # The manifest also lists datasets and investigations; only its NTRS
        # bibliographic records belong in the ResearchAgent publication search.
        self.publications = [item for item in records
                             if item.get("ntrs_id") or "NTRS" in str(item.get("source_type", "")).upper()]
        findings = MICROFIRE_ROOT / "findings.json"
        self.findings = json.loads(findings.read_text(encoding="utf-8")) if findings.exists() else []

    def research(self, query: str) -> dict:
        normalize = lambda value: re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()
        needle = normalize(query)
        terms = [term for term in needle.split() if len(term) >= 3]
        matches = lambda record: (
            needle in normalize(" ".join(map(str, record.values())))
            or any(term in normalize(" ".join(map(str, record.values()))) for term in terms)
        )
        return {
            "query": query,
            "investigations": [item for item in self.investigations if matches(item)],
            "publications": [item for item in self.publications if matches(item)],
            "findings": [item for item in self.findings if matches(item)],
            "limitations": "MicroFire Atlas is a third-party dataset; source records require NASA cross-check. Findings are contextual evidence, not a substitute for the underlying measurements.",
        }


class DataAgent:
    """Safe local-file implementation of the notebook's DataAgent operations."""
    def _paths(self) -> list[Path]:
        return [p for root in (RAW_ROOT, EXPERIMENTS_ROOT) if root.exists()
                for p in root.rglob("*") if p.is_file()]

    def list_datasets(self) -> list[dict]:
        items = []
        for path in sorted(self._paths()):
            items.append({"filename": path.name,
                          "path": path.relative_to(PROJECT_ROOT).as_posix(),
                          "extension": path.suffix.lower(), "size_bytes": path.stat().st_size,
                          "source_type": "MicroFire Atlas" if MICROFIRE_ROOT in path.parents else
                                        "processed dataset" if EXPERIMENTS_ROOT in path.parents else "raw source"})
        return items

    def _find_csv(self, filename: str) -> Path:
        # Match by basename only, preventing traversal and arbitrary local file reads.
        if Path(filename).name != filename or not filename.lower().endswith(".csv"):
            raise FileNotFoundError(f"CSV dataset not found: {filename}")
        matches = [p for p in self._paths() if p.name == filename and p.suffix.lower() == ".csv"]
        if not matches:
            raise FileNotFoundError(f"CSV dataset not found: {filename}")
        # Prefer explicitly cleaned data when requested by its distinct filename;
        # raw and cleaned files generally have different basenames.
        return sorted(matches, key=lambda p: (EXPERIMENTS_ROOT not in p.parents, str(p)))[0]

    def load_csv(self, filename: str) -> pd.DataFrame:
        return pd.read_csv(self._find_csv(filename))

    def profile_dataset(self, filename: str) -> dict:
        path = self._find_csv(filename)
        frame = pd.read_csv(path)
        stats = frame.describe(include="all").replace({np.nan: None}).to_dict()
        # pandas may leave non-finite numpy scalars in object-valued statistics.
        normalized = {column: {str(k): (None if pd.isna(v) else v.item() if hasattr(v, "item") else v)
                               for k, v in values.items()} for column, values in stats.items()}
        return {"filename": filename, "path": path.relative_to(PROJECT_ROOT).as_posix(),
                "rows": len(frame), "columns": list(frame.columns),
                "missing_values": {str(k): int(v) for k, v in frame.isna().sum().items()},
                "duplicate_rows": int(frame.duplicated().sum()), "statistics": normalized,
                "units": "Units are as recorded in the source columns; no conversions applied.",
                "limitations": "Profiling is descriptive and does not establish measurement validity."}

    def search_files(self, query: str) -> list[dict]:
        query = query.casefold()
        return [item for item in self.list_datasets() if query in item["filename"].casefold()]

    def compare_datasets(self, filename_a: str, filename_b: str) -> dict:
        a, b = self.load_csv(filename_a), self.load_csv(filename_b)
        return {"dataset_a": filename_a, "dataset_b": filename_b,
                "columns_a": list(a.columns), "columns_b": list(b.columns),
                "shared_columns": sorted(set(a.columns).intersection(b.columns)),
                "rows_a": len(a), "rows_b": len(b),
                "units": "Source units are not inferred or converted."}


research_agent = ResearchAgent()
data_agent = DataAgent()
