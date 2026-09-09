# AI-Claims-Support-Assistant

An AI-powered insurance claims support solution that helps customers track claims, understand document requirements, receive AI-generated claim summaries, interact with a conversational claims assistant, and validate uploaded documents.

## 1. Problem Statement

Claims processing is one of the most critical customer touchpoints in the insurance industry. Customers frequently contact support teams to ask questions such as:

* What is the current status of my claim?
* What documents are still required?
* How long will my claim take to process?
* Are my submitted documents valid?

Support teams spend considerable time responding to repetitive queries and manually checking submitted documentation. These activities can increase processing time, operational effort, and customer dissatisfaction.

## 2. Solution

The **AI Claims Support Assistant** combines traditional backend processing with Generative AI to provide an intelligent self-service claims experience.

The solution provides:

* Claim lookup and tracking
* Visual claim progress tracking
* Document completeness verification
* Document upload
* AI-based document validation
* AI-generated claim summaries
* Conversational AI claims support
* Grounded responses using claim-specific information
* Hallucination-aware responses that avoid inventing unavailable claim information

For this prototype, synthetic insurance claim data is used instead of real customer information.

## 3. Key Features

### Claim Lookup

Customers can enter a claim ID and retrieve:

* Customer information
* Claim type
* Claim amount
* Current claim status
* Current processing stage
* Document completeness
* Missing documents
* Estimated processing time

### Claim Progress Tracker

The application provides a visual representation of the claim lifecycle:

```text
Claim Submitted
       ↓
Document Verification
       ↓
Assessment
       ↓
Settlement
```

The highlighted stage is dynamically determined from the claim information.

### Document Verification

The backend compares the required documents against submitted documents and identifies:

* Matched documents
* Missing documents
* Extra documents
* Document completeness percentage

For example:

```text
Required Documents = 5
Submitted Documents = 5

Completeness = 5 / 5 × 100 = 100%
```

This deterministic calculation is handled by backend logic rather than Generative AI.

### AI Claim Summary

The application uses Generative AI to convert structured claim information into a concise, customer-friendly summary.

Relevant information such as claim status, claim amount, processing stage, document completeness, missing documents, and estimated processing time is provided to the GenAI service as context.

The model is instructed to use the provided information and avoid inventing unavailable claim details.

### AI Claims Assistant

Customers can ask natural-language questions such as:

```text
What documents are still required for my claim?
```

```text
What is the current status of my claim?
```

```text
How long will my claim take to process?
```

The backend retrieves the relevant claim information and document status and provides that information as context to the GenAI model.

The response is then returned to the frontend.

### AI Document Validation

Customers can upload documents associated with their claims.

The validation flow is:

```text
Document Upload
       ↓
File Validation
       ↓
PDF Text Extraction
       ↓
Claim Context + Document Text
       ↓
GenAI Model
       ↓
Validation Result
       ↓
Frontend
```

For PDF documents, text is extracted using PyPDF. The extracted content, selected document type, and relevant claim information are provided to the GenAI service.

The validation result can include:

* Document validity
* Detected document type
* Confidence
* Document-type match
* Claim relevance
* Potential issues
* Explanation

The GenAI model is used for document interpretation and is **not used to make claim approval, rejection, or settlement decisions**.

## 4. System Architecture

```text
                    Customer
                       │
                       ▼
                Web Frontend
              HTML / CSS / JS
                       │
                       ▼
                 FastAPI API
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
   Claim Services             Document Services
          │                         │
          ▼                         ▼
   Synthetic Claim Data       Document Processing
          │                         │
          └────────────┬────────────┘
                       ▼
                  GenAI Service
                       │
                       ▼
                Azure GenAI Model
                       │
                       ▼
             Grounded AI Response
                       │
                       ▼
                   Frontend
```

The backend retrieves the relevant claim and document information before sending context to the GenAI service. The model does not have unrestricted access to the complete claims dataset.

## 5. End-to-End Flow

### Claim Information Flow

```text
Customer enters Claim ID
          ↓
Frontend sends API request
          ↓
FastAPI receives request
          ↓
Claim Service retrieves claim
          ↓
Document Service calculates document status
          ↓
Claim information returned
          ↓
Frontend displays claim information
```

### AI Summary Flow

```text
Customer requests AI Summary
          ↓
Frontend calls AI Summary API
          ↓
Claim information retrieved
          ↓
Document status calculated
          ↓
Relevant context sent to GenAI
          ↓
Azure GenAI generates summary
          ↓
Summary returned to frontend
```

### AI Chat Flow

```text
Customer Question
       ↓
Claim ID + Question
       ↓
FastAPI
       ↓
Claim Retrieval
       ↓
Document Status
       ↓
Claim Context + Question
       ↓
GenAI Model
       ↓
Grounded Response
       ↓
Frontend
```

## 6. Technology Stack

| Technology               | Purpose                                         |
| ------------------------ | ----------------------------------------------- |
| Python                   | Backend development                             |
| FastAPI                  | REST API development                            |
| HTML                     | Frontend structure                              |
| CSS                      | Frontend styling                                |
| JavaScript               | Frontend interaction and API communication      |
| JSON                     | Synthetic claim data                            |
| PyPDF                    | PDF text extraction                             |
| Generative AI            | Chat, summarization and document interpretation |
| Azure-hosted GenAI Model | AI inference                                    |
| Uvicorn                  | FastAPI application server                      |

## 7. Project Structure

```text
claims-support/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── claims.py
│   │   ├── chat.py
│   │   └── documents.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── models/
│   │   └── claim.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── claim_service.py
│       ├── document_service.py
│       ├── document_validation_service.py
│       └── genai_service.py
│
├── data/
│   └── claims.json
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── uploads/
│
├── .gitignore
├── README.md
└── requirements.txt
```

## 8. API Endpoints

### Get Claim

```http
GET /claims/{claim_id}
```

Retrieves claim information for the specified claim ID.

### Get Claim Summary

```http
GET /claims/{claim_id}/summary
```

Retrieves claim information together with document completeness information.

### Generate AI Summary

```http
GET /claims/{claim_id}/ai-summary
```

Generates a natural-language summary using Generative AI.

### Upload Document

```http
POST /claims/{claim_id}/documents
```

Uploads a document associated with a claim and performs document processing/validation.

### AI Claims Chat

```http
POST /chat/
```

Processes a customer question using claim-specific context.

Example request:

```json
{
  "claim_id": "CLM10003",
  "question": "What is the current status of my claim?"
}
```

## 9. GenAI and Grounding

The solution intentionally separates deterministic business logic from Generative AI functionality.

### Traditional Backend Logic

```text
Claim Lookup
Document Completeness
File Validation
Data Retrieval
PDF Text Extraction
```

### Generative AI

```text
Natural-Language Chat
Claim Summarization
Document Interpretation
```

The backend retrieves relevant claim information and provides it as context to the GenAI model.

The model is instructed to:

* Use only the provided claim context
* Avoid inventing claim information
* Avoid inventing approval or settlement dates
* Avoid inventing missing documents
* Avoid making unsupported claim decisions

This approach helps keep AI responses grounded in the available claim information.

## 10. Hallucination Protection

The application includes scenarios where the requested information is not available in the claim data.

For example:

```text
What exact date will my claim be approved?
```

If the claim data does not contain an exact approval date, the assistant should not invent one.

This demonstrates the use of contextual grounding and explicit AI instructions to reduce unsupported responses.

## 11. Why Generative AI?

Not every part of the application requires Generative AI.

Tasks such as claim retrieval and document completeness are deterministic and are therefore handled using traditional backend logic.

Generative AI is useful for tasks that require language understanding, including:

* Understanding customer questions
* Generating customer-friendly claim summaries
* Interpreting textual document content
* Providing natural-language explanations

Therefore, the architecture uses traditional programming where deterministic logic is appropriate and Generative AI where language understanding provides value.

## 12. Data and Privacy

The prototype uses **synthetic insurance claim data** for demonstration purposes.

No real customer information is required.

Sensitive configuration such as API credentials is stored using environment variables and is excluded from version control using `.gitignore`.

```text
.env
```

is intentionally not committed to the repository.

## 13. Error Handling

The application handles invalid claim IDs and other invalid requests with meaningful responses.

For example:

```text
Claim ID: CLM99999

Response:
Claim not found. Please check the Claim ID.
```

This prevents internal errors from being directly exposed to the customer.

## 14. Business Value

The solution can provide several potential business benefits:

* Reduces repetitive customer-support interactions
* Provides customers with self-service claim information
* Improves claim-status transparency
* Reduces manual document verification effort
* Provides AI-generated summaries of complex claim information
* Enables natural-language customer interaction
* Helps identify potential document issues earlier

Overall, the solution aims to improve customer experience while reducing repetitive operational effort.

## 15. Future Enhancements

Potential production enhancements include:

### Database Integration

Replace the JSON-based prototype data with a production database such as PostgreSQL or an enterprise claims-management system.

### Authentication and Authorization

Add secure customer authentication and role-based access control.

### Secure Document Storage

Move uploaded documents from local storage to secure cloud object storage.

### OCR Support

Add OCR capabilities for scanned PDFs and image-based documents.

### Enterprise Integration

Integrate with existing insurance policy, claims, and document-management systems.

### Human-in-the-Loop Validation

Route low-confidence document validation results to a human reviewer.

### Monitoring and Auditability

Add application logging, audit trails, AI monitoring, and observability.

### Retrieval-Augmented Generation

For a larger production knowledge base, introduce a RAG architecture to retrieve relevant policy documents, claim guidelines, and knowledge-base information before generating responses.

## 16. Limitations

The current implementation is a prototype and uses synthetic claim data.

Generative AI responses are probabilistic and should not be treated as authoritative insurance decisions.

The AI assistant does not make claim approval, rejection, or settlement decisions.

For production use, additional security, authentication, database integration, monitoring, validation, and human oversight would be required.

## 17. Demo Scenarios

The following synthetic claim IDs can be used to demonstrate different application scenarios:

```text
CLM10001 → Document upload and AI document validation
CLM10002 → Claim at Settlement stage
CLM10003 → Document verification and AI Claims Assistant
CLM10004 → Claim status and AI summary
CLM10005 → Claim status and AI summary
```

Example customer questions:

```text
What is the current status of my claim?
```

```text
What documents are still required for my claim?
```

```text
How long will my claim take to process?
```

```text
Can you summarize my claim?
```

```text
What exact date will my claim be approved?
```

The final question can be used to demonstrate that the assistant avoids inventing information that is not available in the claim context.

## 18. Conclusion

The **AI Claims Support Assistant** combines traditional backend processing with Generative AI to improve the insurance claims experience.

Traditional logic handles deterministic operations such as claim retrieval and document completeness, while Generative AI handles natural-language interaction, claim summarization, and document interpretation.

The solution provides customers with greater transparency and self-service while reducing repetitive manual effort for support teams.

## Screenshots

### 1. Claims Support Dashboard

The main dashboard provides users with an overview of the claims support system and allows them to interact with their insurance claims.

![Claims Support Dashboard](images/Screenshot%202026-09-09%20131949.png)

### 2. Claim Status

Users can enter a claim ID to view the current status and details of their insurance claim.

![Claim Status](images/Screenshot%202026-09-09%20132009.png)

### 3. Claim Progress Tracking

The system provides a visual representation of the claim processing journey across different stages.

![Claim Progress](images/Screenshot%202026-09-09%20132022.png)

### 4. Document Verification

The document verification feature checks the submitted documents and identifies whether any required documents are missing.

![Document Verification](images/Screenshot%202026-09-09%20132038.png)

### 5. AI Claim Summary

The AI-powered claim summarization feature generates a concise summary of the claim information to help users understand their claim quickly.

![AI Claim Summary](images/Screenshot%202026-09-09%20132056.png)

### 6. AI Claims Assistant

The conversational AI assistant allows users to ask questions about their claim, including status, required documents, processing time, and claim summaries.

![AI Claims Assistant](images/Screenshot%202026-09-09%20132022.png)

### 7. Document Upload and AI Validation

Users can upload claim-related documents, which are processed and validated using the AI-powered document validation service.

![AI Document Validation](images/Screenshot%202026-09-09%20132208.png)

### 8. Claim Information and Response

The system provides clear, user-friendly responses based on the claim information and available documents.

![Claim Information](images/Screenshot%202026-09-09%20132243.png)

### 9. AI Document Validation

The system uses AI to validate uploaded claim documents by checking the document type, claim ID, relevance to the claim, and potential mismatches.

![AI Document Validation](images/Screenshot%202026-09-09%20134138.png)
