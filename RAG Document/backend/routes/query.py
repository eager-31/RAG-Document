from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from pydantic import BaseModel
import os
import shutil
from config import settings
from ingestion.parser import extract_text_from_pdf
from ingestion.chunker import chunk_pages, save_chunks
from retrieval.embedder import build_and_save_index
from retrieval.retriever import retrieve
from generation.llm_client import generate_answer
from storage.db import log_query, get_history
import re

router = APIRouter(prefix="/api", tags=["api"])

class QueryRequest(BaseModel):
    question: str

def process_pdf_background(file_path: str, filename: str):
    try:
        pages = extract_text_from_pdf(file_path)
        chunks = chunk_pages(pages, filename)
        save_chunks(chunks)
        build_and_save_index(chunks)
    except Exception as e:
        print(f"Error processing PDF: {e}")

@router.post("/upload")
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
    file_path = os.path.join(settings.RAW_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Process the PDF in the background
    background_tasks.add_task(process_pdf_background, file_path, file.filename)
    
    return {"message": "File uploaded and is being processed", "filename": file.filename}

@router.post("/query")
async def query_document(request: QueryRequest):
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
        
    chunks = retrieve(request.question, top_k=5)
    answer = generate_answer(request.question, chunks)
    
    # Extract citations
    # Look for [filename.pdf, page X] patterns
    citations = []
    matches = re.finditer(r'\[([^\]]+),\s*page\s*(\d+)\]', answer, re.IGNORECASE)
    for match in matches:
        citations.append({
            "file": match.group(1).strip(),
            "page": int(match.group(2))
        })
    
    # Deduplicate citations
    unique_citations = []
    seen = set()
    for c in citations:
        key = (c["file"], c["page"])
        if key not in seen:
            seen.add(key)
            unique_citations.append(c)
            
    # Log query
    log_query(request.question, answer, chunks)
    
    return {
        "answer": answer,
        "citations": unique_citations,
        "chunks": chunks
    }

@router.get("/history")
async def get_query_history():
    return get_history()
