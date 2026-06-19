from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
import chromadb
import shutil
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="documents")

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@app.get("/")
def home():
    return {"message": "RAG bot backend is running"}


def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    reader = PdfReader(file_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"

    os.remove(file_path)

    chunks = chunk_text(full_text)

    ids = [f"{file.filename}_{i}" for i in range(len(chunks))]
    collection.add(
        documents=chunks,
        ids=ids
    )

    return {
        "filename": file.filename,
        "pages": len(reader.pages),
        "num_chunks": len(chunks),
        "message": "Chunks stored in ChromaDB successfully"
    }


class QueryRequest(BaseModel):
    question: str


@app.post("/query")
async def query_documents(request: QueryRequest):
    results = collection.query(
        query_texts=[request.question],
        n_results=3
    )

    retrieved_chunks = results["documents"][0]
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""Answer the question based only on the context below. If the answer isn't in the context, say you don't know.

Context:
{context}

Question: {request.question}

Answer:"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content

    return {
        "question": request.question,
        "answer": answer,
        "sources": retrieved_chunks
    }