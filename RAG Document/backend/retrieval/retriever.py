import os
import faiss
import numpy as np
from config import settings
from retrieval.embedder import get_embedder
from ingestion.chunker import load_chunks

def retrieve(query: str, top_k: int = 5) -> list[dict]:
    """
    Embeds the query, searches the FAISS index, and returns the top_k chunks.
    """
    if not os.path.exists(settings.FAISS_INDEX_PATH):
        return []
        
    embedder = get_embedder()
    query_embedding = embedder.embed_query(query)
    query_vector = np.array([query_embedding]).astype('float32')
    
    index = faiss.read_index(settings.FAISS_INDEX_PATH)
    distances, indices = index.search(query_vector, top_k)
    
    all_chunks = load_chunks()
    
    results = []
    for idx in indices[0]:
        if idx != -1 and idx < len(all_chunks):
            results.append(all_chunks[idx])
            
    return results
