import os
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path: str) -> list[dict]:
    """
    Extracts text from a PDF file page by page.
    Returns a list of dictionaries with page_num and text.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found at {pdf_path}")
        
    reader = PdfReader(pdf_path)
    pages = []
    
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            # Clean up the text slightly by replacing multiple spaces/newlines
            text = " ".join(text.split())
            pages.append({
                "page_num": i + 1,
                "text": text
            })
            
    return pages
