from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import settings
import uuid
import os
import json

def chunk_pages(pages: list[dict], source_file: str) -> list[dict]:
    """
    Takes a list of extracted pages and chunks them.
    Adds metadata: source_file, page, chunk_id.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    chunks = []
    for page in pages:
        page_chunks = text_splitter.split_text(page["text"])
        
        for i, chunk_text in enumerate(page_chunks):
            chunks.append({
                "chunk_id": str(uuid.uuid4()),
                "text": chunk_text,
                "metadata": {
                    "source_file": source_file,
                    "page": page["page_num"]
                }
            })
            
    return chunks

def save_chunks(chunks: list[dict]):
    """Saves chunks to a JSON file."""
    existing_chunks = load_chunks()
    existing_chunks.extend(chunks)
    
    with open(settings.CHUNKS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(existing_chunks, f, ensure_ascii=False, indent=2)
        
def load_chunks() -> list[dict]:
    """Loads chunks from the JSON file."""
    if not os.path.exists(settings.CHUNKS_JSON_PATH):
        return []
    with open(settings.CHUNKS_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
