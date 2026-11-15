"""Member 1 contract: JSON ExperimentGroup records, loaded from a local file.

Set FLARE_DATA_FILE to a JSON file with a {"groups": [...]} object after the
team validates formats and provenance. Never label mock data as NASA data.
"""
import json
import os
from pathlib import Path
from app.models import ExperimentGroup
DEFAULT_DATA_FILE=Path(__file__).resolve().parents[2]/'data'/'demo_experiments.json'

def read_groups(ids: list[str] | None=None)->list[ExperimentGroup]:
    path=Path(os.getenv('FLARE_DATA_FILE',str(DEFAULT_DATA_FILE)))
    raw=json.loads(path.read_text(encoding='utf-8'))
    groups=[ExperimentGroup.model_validate(item) for item in raw['groups']]
    by_id={g.group_id:g for g in groups}
    if len(by_id)!=len(groups):
        raise ValueError('Duplicate group IDs in dataset')
    if ids is None:
        return groups
    if len(ids)!=len(set(ids)):
        raise ValueError('Duplicate group IDs are not allowed')
    missing=[name for name in ids if name not in by_id]
    if missing:
        raise ValueError('Unknown group IDs: '+', '.join(missing))
    return [by_id[name] for name in ids]
