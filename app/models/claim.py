from pydantic import BaseModel
from typing import List


class Claim(BaseModel):
    claim_id: str
    customer_name: str
    claim_type: str
    claim_amount: float
    submitted_date: str
    status: str
    stage: str
    required_documents: List[str]
    submitted_documents: List[str]
    estimated_processing_days: str