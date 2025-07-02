# 🤖 AI PDF Q&A Web App

AI-powered web app to upload PDFs and ask questions based on their content using a locally hosted LLaMA (Mistral 7B) model.

---



## 🎬 Demo

📽️ [Watch the demo video](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

Below is a quick preview:

![Demo Preview](assets/demo-screenshot.gif)

---

## 🧠 Model Download

This app requires a local copy of the Mistral model in `.gguf` format.

📥 [Download `mistral-7b-instruct-v0.1.Q3_K_M.gguf`]([https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/blob/main/mistral-7b-instruct-v0.1.Q3_K_M.gguf))

🗂️ After downloading, place the model file here:

🧠 Make sure `main.py` has the correct path:

```python
model = Llama(
    model_path="backend/models/mistral-7b-instruct-v0.1.Q3_K_M.gguf",
    ...
)

---

## 📦 Project Structure
📁 AI_pdf_QnA_WebApp/ <br>
├── main.py # FastAPI backend logic<br>
├── models.py # SQLAlchemy document model<br>
├── database.py # DB setup and session<br>
├── index.html # TailwindCSS-based UI<br>
├── script.js # Handles PDF upload + Q&A<br>
├── uploads/ # Stores uploaded PDFs<br>
├── models/ # Store your .gguf LLaMA model<br>
└── README.md # Project documentation

---

## ✨ Features

- 📄 Upload PDF documents
- 🔍 Ask questions based on document content
- 🧠 Local inference using Mistral 7B model
- 💬 Chat-style Q&A interface
- 🛢️ SQLite for document storage
- 🎨 Responsive UI with TailwindCSS

---

## ⚙️ Setup Instructions

### 1. Clone this repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo

---

## ✅ Assignment Criteria Checklist

- ✅ **Functionality**  
  Upload PDF documents, extract content, and ask questions using an AI model — fully working end-to-end.

- ✅ **Code Quality**  
  Clean, well-organized codebase with modular structure and clear comments in both frontend and backend.

- ✅ **Design & UX**  
  Simple, intuitive user interface built with TailwindCSS — responsive layout and smooth interaction.

- ✅ **Innovation**  
  Uses a locally hosted LLaMA (Mistral 7B) model — no external API calls, ensuring privacy and performance.

---

## 🚀 Future Improvements

- 🔍 **Vector-based document search (FAISS)**  
  Implement semantic search using document embeddings for faster and more accurate answers, especially for large PDFs.

- ⏱️ **Stream answers instead of waiting for full response**  
  Improve user experience by streaming the AI's answer in real time instead of waiting for the complete response.

- 📌 **Highlight relevant parts of the PDF**  
  Visually mark or reference the portion of the PDF text that the AI answer is based on, for better transparency and context.
