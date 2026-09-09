import os

from dotenv import load_dotenv
from openai import OpenAI


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

api_key = os.getenv("AZURE_API_KEY")
base_url = os.getenv("AZURE_BASE_URL")
model = os.getenv("AZURE_MODEL")


# ==========================================
# VALIDATE ENVIRONMENT VARIABLES
# ==========================================

if not api_key:
    raise ValueError("AZURE_API_KEY is not set in .env")

if not base_url:
    raise ValueError("AZURE_BASE_URL is not set in .env")

if not model:
    raise ValueError("AZURE_MODEL is not set in .env")


# ==========================================
# CREATE OPENAI CLIENT
# ==========================================

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)


# ==========================================
# AI CLAIMS CHAT
# ==========================================


def generate_claim_response(
    question: str,
    claim: dict,
    document_status: dict
) -> str:

    context = f"""
Claim Information:

Claim ID: {claim["claim_id"]}
Customer Name: {claim["customer_name"]}
Claim Type: {claim["claim_type"]}
Claim Amount: ₹{claim["claim_amount"]}
Submitted Date: {claim["submitted_date"]}
Status: {claim["status"]}
Current Stage: {claim["stage"]}
Estimated Processing Time: {claim["estimated_processing_days"]}

Document Verification:

Documents Required: {document_status["total_required"]}
Documents Submitted: {document_status["total_submitted"]}
Completeness: {document_status["completeness_percentage"]}%
Missing Documents: {document_status["missing_documents"]}
Extra Documents: {document_status["extra_documents"]}
"""

    system_instruction = """
You are an AI insurance claims support assistant.

Answer customer questions using ONLY the claim information
provided in the context.

Rules:

1. Never invent claim information.
2. Never invent dates, documents, processing times, decisions,
   or reasons.
3. Do not say a claim is approved or rejected unless the claim
   status explicitly says so.
4. If information is unavailable, clearly say so.
5. If documents are missing, clearly mention the missing documents.
6. If no documents are missing and completeness is 100%, clearly
   tell the customer that all required documents have been
   submitted and that no additional documents are currently
   required.
7. If all documents are submitted but the claim is still in
   Document Collection or Document Verification, do not say that
   the documents have been verified unless the claim information
   explicitly says they are verified.
8. When the customer asks what documents are still required and
   there are no missing documents, respond concisely and naturally.
9. Give a helpful next step when appropriate.
10. Do not provide an exact approval date unless an exact approval
    date is explicitly available in the claim information.
11. If only an estimated processing time is available, clearly
    describe it as an estimate.
12. Keep responses professional, simple, and customer-friendly.

For a question such as:
"What documents are still required for my claim?"

If there are no missing documents, give a response similar to:

"All required documents for your claim have been submitted, so
there are no additional documents required at this time. Your claim
is currently in the Document Collection stage and will proceed to
document verification."

Do not add information that is not present in the claim context.
"""

    user_prompt = f"""
{context}

Customer Question:
{question}

Answer the customer's question using only the information above.
"""

    response = client.responses.create(
        model=model,
        instructions=system_instruction,
        input=user_prompt
    )

    return response.output_text



# ==========================================
# AI CLAIM SUMMARY
# ==========================================

def generate_claim_summary(
    claim: dict,
    document_status: dict
) -> str:

    prompt = f"""
You are an AI insurance claims support assistant.

Generate a concise and professional summary of the
following insurance claim.

Claim Information:

Claim ID: {claim["claim_id"]}
Customer Name: {claim["customer_name"]}
Claim Type: {claim["claim_type"]}
Claim Amount: ₹{claim["claim_amount"]}
Submitted Date: {claim["submitted_date"]}
Status: {claim["status"]}
Current Stage: {claim["stage"]}

Document Verification:

Required Documents:
{", ".join(claim["required_documents"])}

Submitted Documents:
{", ".join(document_status["submitted_documents"])}

Missing Documents:
{
    ", ".join(document_status["missing_documents"])
    if document_status["missing_documents"]
    else "None"
}

Document Completeness:
{document_status["completeness_percentage"]}%

Estimated Processing Time:
{claim["estimated_processing_days"]}


Instructions:

1. Write a concise summary in 3-5 sentences.
2. Mention the customer's claim status.
3. Mention the current processing stage.
4. Mention document completeness.
5. Mention missing documents if there are any.
6. Mention the estimated processing time.
7. Do not invent any information.
8. Use ONLY the information provided above.
9. Keep the language professional and customer-friendly.
10. Do not make assumptions about approval, rejection,
    delays, or settlement unless explicitly provided.
"""

    system_instruction = """
You are an AI insurance claims summarization assistant.

Your job is to summarize insurance claim information
accurately and clearly.

Use ONLY the information provided.

Never invent:
- claim decisions
- dates
- missing documents
- processing times
- reasons for delays
- settlement information
- policy information

If something is not available, do not make it up.

Keep the summary concise, professional,
and customer-friendly.
"""

    response = client.responses.create(
        model=model,
        instructions=system_instruction,
        input=prompt
    )

    return response.output_text

