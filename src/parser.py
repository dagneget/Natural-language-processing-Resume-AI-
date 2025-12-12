import os
from pdfminer.high_level import extract_text
import docx

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file.
    """
    try:
        text = extract_text(file_path)
        return text
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        return ""

def extract_text_from_docx(file_path):
    """
    Extracts text from a DOCX file.
    """
    try:
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        print(f"Error reading DOCX {file_path}: {e}")
        return ""

def extract_text_from_file(file_path):
    """
    Dispatcher function to extract text based on file extension.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    else:
        # Fallback for text files or unsupported formats
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            print(f"Unsupported file format: {ext}")
            return ""
