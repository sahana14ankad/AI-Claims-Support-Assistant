const API_BASE_URL = "http://127.0.0.1:8000";

async function loadClaim() {


const claimId =
    document.getElementById("claimId").value.trim();

const dashboard =
    document.getElementById("dashboard");

const error =
    document.getElementById("claimError");


if (!claimId) {

    error.innerHTML =
        '<p class="error">Please enter a Claim ID.</p>';

    dashboard.classList.add("hidden");

    return;
}


error.innerHTML =
    "<p>Loading claim details...</p>";


try {

    const response = await fetch(
        `${API_BASE_URL}/claims/${encodeURIComponent(claimId)}/summary`
    );


    if (!response.ok) {

        throw new Error("Claim not found");

    }


    const claim =
        await response.json();


    document.getElementById("customerName").textContent =
        claim.customer_name;


    document.getElementById("claimStatus").textContent =
        claim.status;


    document.getElementById("claimAmount").textContent =
        "\u20B9" +
        Number(
            claim.claim_amount
        ).toLocaleString("en-IN");


    document.getElementById("claimType").textContent =
        claim.claim_type;


    document.getElementById("claimStage").textContent =
        claim.stage;


    document.getElementById("documentCompleteness").textContent =
        `${claim.document_completeness}%`;


    document.getElementById("processingTime").textContent =
        claim.estimated_processing_days;


    displayDocuments(claim);


    // Update the visual claim progress tracker
    updateClaimProgress(claim.stage);


    error.innerHTML = "";

    dashboard.classList.remove("hidden");


} catch (errorObject) {

    dashboard.classList.add("hidden");

    error.innerHTML =
        '<p class="error">Claim not found. Please check the Claim ID.</p>';
}


}

function displayDocuments(claim) {


const container =
    document.getElementById("documentsList");


let html = "";


if (Array.isArray(claim.submitted_documents)) {

    claim.submitted_documents.forEach(
        documentName => {

            html += `
                <div class="document-item complete">
                    <span>&#10003;</span>
                    ${documentName}
                </div>
            `;
        }
    );
}


if (Array.isArray(claim.missing_documents)) {

    claim.missing_documents.forEach(
        documentName => {

            html += `
                <div class="document-item missing">
                    <span>&#10007;</span>
                    ${documentName}
                </div>
            `;
        }
    );
}


if (!html) {

    html =
        `<p>No document information available.</p>`;
}


container.innerHTML = html;


}

async function uploadDocument() {


const claimId =
    document.getElementById("claimId").value.trim();


const documentType =
    document.getElementById("documentType").value;


const fileInput =
    document.getElementById("documentFile");


const result =
    document.getElementById("uploadResult");


if (!claimId) {

    result.innerHTML =
        '<p class="error">Please enter a Claim ID first.</p>';

    return;
}


if (!documentType) {

    result.innerHTML =
        '<p class="error">Please select a document type.</p>';

    return;
}


if (
    !fileInput.files ||
    fileInput.files.length === 0
) {

    result.innerHTML =
        '<p class="error">Please select a document.</p>';

    return;
}


const formData =
    new FormData();


formData.append(
    "document_type",
    documentType
);


formData.append(
    "file",
    fileInput.files[0]
);


result.innerHTML =
    "<p>Uploading document and validating with AI...</p>";


try {

    const response = await fetch(
        `${API_BASE_URL}/claims/${encodeURIComponent(claimId)}/documents`,
        {
            method: "POST",
            body: formData
        }
    );


    const data =
        await response.json();


    if (!response.ok) {

        throw new Error(
            data.detail || "Upload failed"
        );
    }


    let validationHTML = "";


    if (data.ai_validation) {

        validationHTML = `
            <div class="ai-validation">
                <h3>AI Document Validation</h3>
                <p>${formatAIResponse(data.ai_validation)}</p>
            </div>
        `;
    }


    await loadClaim();


    result.innerHTML = `
        <p class="success">
            &#10003; ${data.message}
        </p>
        ${validationHTML}
    `;


    fileInput.value = "";


} catch (errorObject) {

    result.innerHTML = `
        <p class="error">
            ${errorObject.message}
        </p>
    `;
}


}

async function askAssistant() {


const claimId =
    document.getElementById("claimId").value.trim();


const question =
    document.getElementById("question").value.trim();


if (!claimId) {

    addMessage(
        "Please enter your Claim ID first.",
        "bot"
    );

    return;
}


if (!question) {
    return;
}


addMessage(
    question,
    "user"
);


document.getElementById("question").value = "";


addMessage(
    "Thinking...",
    "bot"
);


try {

    const response = await fetch(
        `${API_BASE_URL}/chat/`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                claim_id: claimId,
                question: question
            })
        }
    );


    if (!response.ok) {

        throw new Error(
            "Unable to contact AI assistant"
        );
    }


    const data =
        await response.json();


    removeThinkingMessage();


    addMessage(
        data.answer,
        "bot"
    );


} catch (errorObject) {

    removeThinkingMessage();


    addMessage(
        "Sorry, I was unable to process your request.",
        "bot"
    );
}


}

function addMessage(
message,
type
) {


const chatMessages =
    document.getElementById("chatMessages");


const messageDiv =
    document.createElement("div");


if (type === "user") {

    messageDiv.className =
        "user-message";


    messageDiv.textContent =
        message;

} else {

    messageDiv.className =
        "bot-message";


    messageDiv.innerHTML =
        formatAIResponse(message);
}


chatMessages.appendChild(
    messageDiv
);


chatMessages.scrollTop =
    chatMessages.scrollHeight;


}

function removeThinkingMessage() {


const messages =
    document.querySelectorAll(
        ".bot-message"
    );


messages.forEach(
    message => {

        if (
            message.textContent.trim() ===
            "Thinking..."
        ) {

            message.remove();
        }
    }
);


}

function handleEnter(event) {


if (event.key === "Enter") {

    askAssistant();
}


}

function formatAIResponse(message) {


const text =
    String(message);


const escaped =
    text
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );


return escaped
    .replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
    )
    .replace(
        /\n/g,
        "<br>"
    );


}

async function generateAISummary() {


const claimId =
    document.getElementById("claimId").value.trim();


const summaryContainer =
    document.getElementById("aiSummary");


if (!claimId) {

    summaryContainer.innerHTML =
        '<p class="error">Please enter a Claim ID first.</p>';

    return;
}


summaryContainer.innerHTML =
    "<p>Generating AI summary...</p>";


try {

    const response = await fetch(
        `${API_BASE_URL}/claims/${encodeURIComponent(claimId)}/ai-summary`,
        {
            method: "GET"
        }
    );


    const data =
        await response.json();


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Unable to generate AI summary"
        );
    }


    summaryContainer.innerHTML =
        `<p>${formatAIResponse(data.ai_summary)}</p>`;


} catch (errorObject) {

    summaryContainer.innerHTML =
        `<p class="error">
            ${errorObject.message}
        </p>`;
}


}

/* CLAIM PROGRESS TRACKER */

function updateClaimProgress(stage) {


const steps = [

    document.getElementById(
        "stepSubmitted"
    ),

    document.getElementById(
        "stepDocuments"
    ),

    document.getElementById(
        "stepAssessment"
    ),

    document.getElementById(
        "stepSettlement"
    )

];


// Reset all steps

steps.forEach(
    step => {

        if (step) {

            step.classList.remove(
                "completed"
            );

            step.classList.remove(
                "current"
            );
        }
    }
);


// Default stage:
// Claim Submitted

let currentStep = 0;

if (
    stage === "Document Collection" ||
    stage === "Document Verification"
) {
    currentStep = 1;
}
else if (stage === "Assessment") {
    currentStep = 2;
}
else if (stage === "Settlement") {
    currentStep = 3;
}

// Mark previous steps as completed

for (
    let i = 0;
    i < currentStep;
    i++
) {

    if (steps[i]) {

        steps[i].classList.add(
            "completed"
        );
    }
}


// Mark current step

if (steps[currentStep]) {

    steps[currentStep].classList.add(
        "current"
    );
}


}
