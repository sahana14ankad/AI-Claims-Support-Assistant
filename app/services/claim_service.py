import json
from pathlib import Path


DATA_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "claims.json"
)


def load_claims():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_claim_by_id(claim_id: str):
    claims = load_claims()

    for claim in claims:
        if claim["claim_id"].upper() == claim_id.upper():
            return claim

    return None