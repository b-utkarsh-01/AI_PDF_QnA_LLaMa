const form = document.getElementById("ask-form");
const fileInput = document.getElementById("pdf-upload");
const fileNameDisplay = document.getElementById("file-name");
const chatHistory = document.getElementById("chat-history");
const errorBox = document.getElementById("error-box");

fileInput.addEventListener("change", () => {
  fileNameDisplay.textContent = fileInput.files[0]?.name || "No file chosen";
  errorBox.textContent = "";
  fileInput.dataset.documentId = ""; // Clear previous document ID if new file selected
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const file = fileInput.files[0];
  const question = document.getElementById("question").value.trim();

  if (!file || !question) {
    errorBox.textContent = "Please upload a PDF and type a question.";
    return;
  }

  if (!file.name.toLowerCase().endsWith(".pdf")) {
    errorBox.textContent = "Only PDF files are supported.";
    return;
  }

  errorBox.textContent = "";

  // 🟡 Chat UI: Create bubble immediately
  const bubble = document.createElement("div");
  bubble.className =
    "flex items-start space-x-3 bg-white p-4 rounded-lg shadow";
  bubble.innerHTML = `
    <div class="flex-shrink-0 w-10 h-10 rounded-full bg-purple-200 flex items-center justify-center text-white font-bold text-lg">Y</div>
    <div class="space-y-2">
      <div>
        <p class="text-gray-900 font-semibold">You</p>
        <p class="text-gray-700">${question}</p>
      </div>
      <div class="flex items-start space-x-2">
        <div class="flex-shrink-0 w-8 h-8 rounded-full bg-green-200 flex items-center justify-center text-white font-bold text-sm">AI</div>
        <div>
          <p class="text-gray-900 font-semibold">AI</p>
          <p class="text-blue-600" id="ai-answer">Loading...<br><span class="text-xs">Please wait</span></p>
        </div>
      </div>
    </div>
  `;
  chatHistory.appendChild(bubble);
  document.getElementById("question").value = "";

  try {
    // 🟢 STEP 1: Upload PDF once if not already
    let documentId = fileInput.dataset.documentId;

    if (!documentId) {
      const uploadForm = new FormData();
      uploadForm.append("file", file);

      const uploadRes = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: uploadForm,
      });

      if (!uploadRes.ok) {
        throw new Error("PDF upload failed");
      }

      const uploadData = await uploadRes.json();
      documentId = uploadData.document_id;
      fileInput.dataset.documentId = documentId; // Cache for next questions
    }

    // 🟢 STEP 2: Send question with document_id
    const askForm = new FormData();
    askForm.append("document_id", documentId);
    askForm.append("question", question);

    const askRes = await fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      body: askForm,
    });

    const data = await askRes.json();
    const aiAnswer = bubble.querySelector("#ai-answer");

    if (askRes.ok && data.answer) {
      aiAnswer.classList.remove("text-blue-600");
      aiAnswer.classList.add("text-gray-700");
      aiAnswer.textContent = data.answer;
    } else {
      throw new Error("Failed to get valid answer.");
    }
  } catch (err) {
    const aiAnswer = bubble.querySelector("#ai-answer");
    aiAnswer.classList.remove("text-blue-600");
    aiAnswer.classList.add("text-red-600");
    aiAnswer.textContent = "❌ Error: Failed to process your request.";
    console.error(err);
  }
});
