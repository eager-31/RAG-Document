from langchain_groq import ChatGroq
from langchain_community.llms import Ollama
from config import settings
from generation.prompt_templates import qa_prompt

def get_llm():
    if settings.USE_LOCAL_LLM:
        return Ollama(base_url=settings.OLLAMA_BASE_URL, model=settings.MODEL_NAME)
    else:
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        return ChatGroq(temperature=0, model_name=settings.MODEL_NAME, groq_api_key=settings.GROQ_API_KEY)

def generate_answer(query: str, chunks: list[dict]) -> str:
    """
    Generates an answer using the provided chunks as context.
    """
    if not chunks:
        return "Not found in context."
        
    llm = get_llm()
    
    # Format context with citations
    context_parts = []
    for chunk in chunks:
        meta = chunk.get("metadata", {})
        filename = meta.get("source_file", "unknown")
        page = meta.get("page", "unknown")
        text = chunk.get("text", "")
        context_parts.append(f"[{filename}, page {page}]: {text}")
        
    context_str = "\n\n".join(context_parts)
    
    chain = qa_prompt | llm
    
    response = chain.invoke({"context": context_str, "question": query})
    
    if hasattr(response, 'content'):
        return response.content
    return str(response)
