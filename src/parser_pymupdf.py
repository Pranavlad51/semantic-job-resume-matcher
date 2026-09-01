"""
src/parser.py (continued from previous - missing imports)
Adding PyMuPDF support
"""

import fitz  # PyMuPDF

def extract_text_from_pdf_pymupdf(file_path):
    """
    Alternative PDF extraction using PyMuPDF (faster for some PDFs).
    
    Args:
        file_path (str): Path to PDF file
    
    Returns:
        str: Extracted text
    """
    try:
        text = ""
        with fitz.open(file_path) as pdf:
            for page_num in range(len(pdf)):
                page = pdf[page_num]
                text += page.get_text()
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting PDF with PyMuPDF: {str(e)}")
