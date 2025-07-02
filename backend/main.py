from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from llama_cpp import Llama
from datetime import datetime
import fitz  # PyMuPDF
import os
import traceback

from models import Document, Base, SessionLocal
from database import engine, create_tables

# Initialize FastAPI app
app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure DB tables are created on startup
@app.on_event("startup")
def on_startup():
    create_tables()

# Load LLaMA model once
model = Llama(
    model_path="models/mistral-7b-instruct-v0.1.Q3_K_M.gguf",
    n_ctx=3900,
    n_threads=8
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Utility to extract text from PDF
def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


# Route: Upload PDF and store in DB
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        print(f"🔄 Received file: {file.filename}")

        filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as f:
            f.write(await file.read())
        print(f"✅ File saved to: {filepath}")

        # Extract text
        pdf_text = extract_text_from_pdf(filepath)
        print(f"✅ Extracted {len(pdf_text)} characters from PDF")

        # Save to DB
        db = SessionLocal()
        doc = Document(filename=filename, upload_time=datetime.utcnow(), text=pdf_text)
        db.add(doc)
        db.commit()
        db.refresh(doc)
        db.close()
        print(f"✅ Document saved with ID {doc.id}")

        return {"message": "File uploaded", "document_id": doc.id}

    except Exception as e:
        print("❌ Upload failed:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Route: Ask question about uploaded PDF
@app.post("/ask")
async def ask_question(document_id: int = Form(...), question: str = Form(...)):
    db = SessionLocal()
    doc = db.query(Document).filter(Document.id == document_id).first()
    db.close()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        prompt = f"Answer the question based on the following PDF content:\n\n{doc.text}\n\nQuestion: {question}\nAnswer:"
        output = model(prompt, max_tokens=512, stop=["</s>", "Question:", "Answer:"], echo=False)
        answer = output["choices"][0]["text"].strip()
        return {"answer": answer}
    except Exception as e:
        print("❌ Model inference failed:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Failed to generate answer")


# Route: List uploaded documents
@app.get("/documents")
def list_documents():
    db = SessionLocal()
    docs = db.query(Document).all()
    db.close()

    return [
        {"id": d.id, "filename": d.filename, "upload_time": d.upload_time.isoformat()}
        for d in docs
    ]