import json
from pathlib import Path


DATA_FILE = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "claims.json"
)


def validate_documents(claim):
    required_documents = set(claim["required_documents"])
    submitted_documents = set(claim["submitted_documents"])

    missing_documents = sorted(
        required_documents - submitted_documents
    )

    extra_documents = sorted(
        submitted_documents - required_documents
    )

    matched_documents = required_documents & submitted_documents

    total_required = len(required_documents)
    total_submitted = len(matched_documents)

    if total_required > 0:
        completeness_percentage = round(
            (total_submitted / total_required) * 100,
            2
        )
    else:
        completeness_percentage = 100.0

    return {
        "claim_id": claim["claim_id"],
        "complete": len(missing_documents) == 0,
        "total_required": total_required,
        "total_submitted": total_submitted,
        "completeness_percentage": completeness_percentage,
        "submitted_documents": sorted(matched_documents),
        "missing_documents": missing_documents,
        "extra_documents": extra_documents
    }


def add_submitted_document(claim_id: str, document_type: str):
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        claims = json.load(file)

    for claim in claims:

        if claim["claim_id"].upper() == claim_id.upper():

            if document_type not in claim["submitted_documents"]:
                claim["submitted_documents"].append(document_type)

            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    claims,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            return claim

    return None
