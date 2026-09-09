from fastapi import APIRouter, HTTPException

from app.services.claim_service import get_claim_by_id
from app.services.document_service import validate_documents


router = APIRouter(
    prefix="/claims",
    tags=["Documents"]
)


@router.get("/{claim_id}/documents/validate")
def validate_claim_documents(claim_id: str):

    claim = get_claim_by_id(claim_id)

    if claim is None:
        raise HTTPException(
            status_code=404,
            detail="Claim not found"
        )

    return validate_documents(claim)