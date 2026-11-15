"""Member 1 NASA PSI research catalog; descriptions are not numeric evidence."""
from app.adapters.member1 import INVESTIGATIONS as _MEMBER1_INVESTIGATIONS

INVESTIGATIONS = [
    {"family": item["name"].split("-")[0], "title": item["name"],
     "focus": item["topic"], "official_url": item["url"],
     "psi_id": item["psi_id"], "data_imported": False}
    for item in _MEMBER1_INVESTIGATIONS
]
