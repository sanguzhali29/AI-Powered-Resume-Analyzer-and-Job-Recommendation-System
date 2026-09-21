"""
Resume File Parser Module (Phase 4)
===================================
Extracts raw plain-text content from uploaded PDF, DOCX, and TXT resumes.
Uses PyPDF2 / pdfplumber and python-docx with robust exception handling.
"""

import os
import re
import io
import PyPDF2
import docx

class ResumeParseError(Exception):
    """Custom exception raised when resume text extraction fails."""
    pass


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts plain text from a PDF file using PyPDF2.
    Iterates through all pages and concatenates extracted text blocks.
    """
    text_content = []
    try:
        with open(file_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            num_pages = len(pdf_reader.pages)
            if num_pages == 0:
                raise ResumeParseError("The uploaded PDF file has no pages.")
                
            for page_idx in range(num_pages):
                page = pdf_reader.pages[page_idx]
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
                    
        full_text = "\n".join(text_content).strip()
        if not full_text:
            raise ResumeParseError(
                "Could not extract readable text from PDF. It may be scanned or image-only."
            )
        return full_text
    except Exception as e:
        if isinstance(e, ResumeParseError):
            raise e
        raise ResumeParseError(f"Failed to parse PDF file: {str(e)}")


def extract_text_from_docx(file_path: str) -> str:
    """
    Extracts text from a Microsoft Word (.docx) document using python-docx.
    Extracts text from both paragraphs and table cells.
    """
    try:
        doc = docx.Document(file_path)
        text_content = []
        
        # 1. Paragraphs
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                text_content.append(text)
                
        # 2. Tables (resumes frequently format skills or education in tables)
        for table in doc.tables:
            for row in table.rows:
                row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_text:
                    text_content.append(" | ".join(row_text))
                    
        full_text = "\n".join(text_content).strip()
        if not full_text:
            raise ResumeParseError("The uploaded DOCX file is empty or unreadable.")
        return full_text
    except Exception as e:
        if isinstance(e, ResumeParseError):
            raise e
        raise ResumeParseError(f"Failed to parse DOCX file: {str(e)}")


def extract_text_from_txt(file_path: str) -> str:
    """Extracts text from a plain text (.txt) file with multi-encoding fallback."""
    encodings = ["utf-8", "latin-1", "cp1252"]
    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                text = f.read().strip()
                if text:
                    return text
        except UnicodeDecodeError:
            continue
    raise ResumeParseError("Failed to decode text file. Unsupported encoding.")


def parse_resume_file(file_path: str) -> str:
    """
    Dispatcher function to extract text based on file extension.
    Supported extensions: .pdf, .docx, .txt
    """
    if not os.path.exists(file_path):
        raise ResumeParseError(f"File not found: {file_path}")

    _, ext = os.path.splitext(file_path.lower())
    
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ResumeParseError(f"Unsupported file format '{ext}'. Please upload PDF, DOCX, or TXT.")
