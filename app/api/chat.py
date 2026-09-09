from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.claim_service import get_claim_by_id
from app.services.document_service import validate_documents
from app.services.genai_service import generate_claim_response


router = APIRouter(
    prefix="/chat",
    tags=["AI Claims Chat"]
)


class ChatRequest(BaseModel):
    claim_id: str
    question: str


@router.post("/")
def chat_with_claim_assistant(request: ChatRequest):

    claim = get_claim_by_id(request.claim_id)

    if claim is None:
        raise HTTPException(
            status_code=404,
            detail="Claim not found"
        )

    document_status = validate_documents(claim)

    answer = generate_claim_response(
        question=request.question,
        claim=claim,
        document_status=document_status
    )

    return {
        "claim_id": claim["claim_id"],
        "question": request.question,
        "answer": answer,
        "document_status": document_status
    }