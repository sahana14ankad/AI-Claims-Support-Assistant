from pypdf import PdfReader

from app.services.genai_service import client, model


def extract_pdf_text(file_path: str) -> str:

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


def validate_document(
    file_path: str,
    document_type: str,
    claim: dict
) -> str:

    extracted_text = extract_pdf_text(file_path)

    if not extracted_text:

        return (
            "Validation: Unable to determine\n"
            "Document Type: Unknown\n"
            "Confidence: Low\n"
            "Match: No\n"
            "Claim Relevance: Unable to determine\n"
            "Issues: No readable text could be extracted from the PDF.\n"
            "Explanation: The uploaded PDF does not contain readable text."
        )


    prompt = f"""
You are an AI insurance document validation assistant.

Your task is to validate an uploaded insurance document.

CLAIM INFORMATION

Claim ID:
{claim["claim_id"]}

Customer Name:
{claim["customer_name"]}

Claim Type:
{claim["claim_type"]}


SELECTED DOCUMENT TYPE

{document_type}


UPLOADED DOCUMENT TEXT

{extracted_text}


Analyze the uploaded document carefully.

Determine:

1. Whether the document appears valid.
2. What type of document it appears to be.
3. Your confidence level.
4. Whether the detected document type matches
   the selected document type.
5. Whether the document appears relevant to this claim.
6. Any important issues or missing information.
7. A short explanation.


IMPORTANT RULES

- Use ONLY the claim information and uploaded document text.
- Do not invent information.
- Do not make claim approval or rejection decisions.
- Do not decide whether the claim should be paid.
- Do not assume information that is not present.
- If information is unavailable, say so clearly.
- Treat the uploaded document as synthetic/test data.


RESPOND EXACTLY IN THIS FORMAT:

Validation: Valid or Invalid
Document Type: <identified document type>
Confidence: High, Medium, or Low
Match: Yes or No
Claim Relevance: Relevant, Possibly Relevant, or Not Relevant
Issues: <brief explanation>
Explanation: <short explanation>
"""


    response = client.responses.create(

        model=model,

        instructions="""
You are an insurance document validation assistant.

Analyze uploaded insurance document text carefully.

Your responsibility is ONLY document validation.

Never make decisions about:
- claim approval
- claim rejection
- settlement
- payment

Use only the information provided.

Follow the requested response format exactly.
""",

        input=prompt
    )


    return response.output_text