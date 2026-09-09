from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
    File,
    Form
)

from pathlib import Path

from app.services.claim_service import get_claim_by_id
from app.services.document_service import (
    validate_documents,
    add_submitted_document
)
from app.services.genai_service import generate_claim_summary
from app.services.document_validation_service import validate_document


router = APIRouter(
    prefix="/claims",
    tags=["Claims"]
)


@router.get("/{claim_id}")
def get_claim(claim_id: str):

    claim = get_claim_by_id(claim_id)

    if claim is None:
        raise HTTPException(
            status_code=404,
            detail="Claim not found"
        )

    return claim


@router.get("/{claim_id}/summary")
def get_claim_summary(claim_id: str):

    claim = get_claim_by_id(claim_id)

    if claim is None:
        raise HTTPException(
            status_code=404,
            detail="Claim not found"
        )

    document_status = validate_documents(claim)

    return {
        "claim_id": claim["claim_id"],
        "customer_name": claim["customer_name"],
        "claim_type": claim["claim_type"],
        "claim_amount": claim["claim_amount"],
        "status": claim["status"],
        "stage": claim["stage"],
        "document_completeness":
            document_status["completeness_percentage"],
        "submitted_documents":
            document_status["submitted_documents"],
        "missing_documents":
            document_status["missing_documents"],
        "estimated_processing_days":
            claim["estimated_processing_days"]
    }


@router.get("/{claim_id}/ai-summary")
def get_ai_claim_summary(claim_id: str):

    claim = get_claim_by_id(claim_id)

    if claim is None:
        raise HTTPException(
            status_code=404,
            detail="Claim not found"
        )

    document_status = validate_documents(claim)

    summary = generate_claim_summary(
        claim=claim,
        document_status=document_status
    )

    return {
        "claim_id": claim["claim_id"],
        "customer_name": claim["customer_name"],
        "ai_summary": summary
    }


@router.post("/{claim_id}/documents")
async def upload_document(
    claim_id: str,
    document_type: str = Form(...),
    file: UploadFile = File(...)
):

    claim = get_claim_by_id(claim_id)

    if claim is None:
        raise HTTPException(
            status_code=404,
            detail="Claim not found"
        )


    allowed_documents = {
        "Claim Form",
        "Hospital Bill",
        "Discharge Summary",
        "Prescription",
        "Diagnostic Reports",
        "ID Proof"
    }


    if document_type not in allowed_documents:

        raise HTTPException(
            status_code=400,
            detail="Invalid document type"
        )


    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file selected"
        )


    allowed_extensions = {
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png"
    }

    extension = Path(
        file.filename
    ).suffix.lower()


    if extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPG, JPEG and PNG files are allowed"
        )


    upload_directory = (
        Path("uploads") /
        claim_id.upper()
    )

    upload_directory.mkdir(
        parents=True,
        exist_ok=True
    )


    safe_filename = Path(
        file.filename
    ).name

    file_path = (
        upload_directory /
        safe_filename
    )


    contents = await file.read()


    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(contents)


    ai_validation = None


    if extension == ".pdf":

        ai_validation = validate_document(
            file_path=str(file_path),
            document_type=document_type,
            claim=claim
        )


    updated_claim = add_submitted_document(
        claim_id,
        document_type
    )


    document_status = validate_documents(
        updated_claim
    )


    return {
        "message":
            f"{document_type} uploaded successfully",

        "claim_id":
            claim_id.upper(),

        "document_type":
            document_type,

        "filename":
            safe_filename,

        "ai_validation":
            ai_validation,

        "document_completeness":
            document_status[
                "completeness_percentage"
            ],

        "submitted_documents":
            document_status[
                "submitted_documents"
            ],

        "missing_documents":
            document_status[
                "missing_documents"
            ]
    }
