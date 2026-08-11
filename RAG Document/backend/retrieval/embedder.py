import os
import faiss
import numpy as np
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import settings
from ingestion.chunker import load_chunks

# Initialize the embedder globally to avoid reloading the model
embeddings_model = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)

def get_embedder():
    return embeddings_model

def build_and_save_index(chunks: list[dict]):
    """
    Embeds new chunks and adds them to the FAISS index.
    Saves the updated index to disk.
    """
    if not chunks:
        return
        
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embeddings_model.embed_documents(texts)
    embedding_matrix = np.array(embeddings).astype('float32')
    
    # Check if index exists
    if os.path.exists(settings.FAISS_INDEX_PATH):
        index = faiss.read_index(settings.FAISS_INDEX_PATH)
    else:
        # Initialize a new index
        dimension = embedding_matrix.shape[1]
        index = faiss.IndexFlatL2(dimension)
        
    index.add(embedding_matrix)
    faiss.write_index(index, settings.FAISS_INDEX_PATH)
