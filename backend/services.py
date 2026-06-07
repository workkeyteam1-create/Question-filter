import pdfplumber
import PyPDF2
import re
import os
from sqlalchemy.orm import Session
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import tempfile
from typing import List

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    text = ""
    
    # Check if file is actually a PDF by looking at extension and magic bytes
    if not file_path.lower().endswith('.pdf'):
        # For non-PDF files, try to read as plain text
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Failed to read file: {e}")
    
    try:
        # Try with pdfplumber first (better for text extraction)
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"pdfplumber failed: {e}, trying PyPDF2")
        # Fallback to PyPDF2
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e2:
            print(f"PyPDF2 also failed: {e2}")
            raise Exception(f"Failed to extract text from PDF: {e2}")
    
    return text

def extract_questions(text: str) -> List[str]:
    """Extract questions from text with improved handling of noisy PDF text"""
    questions = []
    
    # First, clean up the text - remove excessive noise but preserve question structure
    # Remove sequences of random special characters that aren't part of questions
    cleaned = re.sub(r'[^\w\s\.\?\!\,\:\;\(\)\[\]\d]+', ' ', text)
    # Normalize multiple spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # Pattern 1: Q followed by number (Q1., Q2:, Question 1, etc.) - most common for exam papers
    pattern_q = r'(?:Q\.?\s*\d+[\.:]?\s*|Question\s*\d+[\.:]?\s*)(.+?)(?=(?:Q\.?\s*\d+|Question\s*\d+|$))'
    
    # Pattern 2: Number followed by . or ) at start of line or after whitespace
    pattern_num = r'(?:^|\n)\s*(\d+[\.\)]\s*)(.+?)(?=(?:\n\s*\d+[\.\)]\s*|$))'
    
    # Pattern 3: Standalone questions with question words
    pattern_words = r'((?:What|How|Why|When|Where|Who|Explain|Describe|Define|Discuss|Calculate|Show|Prove)[\w\s,]+[\.\\?])'
    
    # Try pattern 1 first (most common for exam papers)
    matches = re.findall(pattern_q, cleaned, re.IGNORECASE | re.DOTALL)
    if matches:
        for match in matches:
            q = match.strip()
            if len(q) > 10:
                questions.append(q)
    
    # If no matches, try pattern 2
    if not questions:
        matches = re.findall(pattern_num, cleaned, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        if matches:
            for match in matches:
                q = match[1].strip()
                if len(q) > 10:
                    questions.append(q)
    
    # If still no matches, try pattern 3
    if not questions:
        matches = re.findall(pattern_words, cleaned, re.IGNORECASE)
        if matches:
            for match in matches:
                q = match.strip()
                if len(q) > 10:
                    questions.append(q)
    
    # If still no questions found, fall back to original heuristic approach
    if not questions:
        # Split by common delimiters
        delimiters = ['\n\n', '? ', '.\n']
        for delimiter in delimiters:
            if len(questions) > 0:
                break
            parts = text.split(delimiter)
            for part in parts:
                part = part.strip()
                if len(part) > 20 and any(keyword in part.lower() for keyword in ['what', 'how', 'why', 'explain', 'describe', 'calculate']):
                    questions.append(part)
    
    # Clean up extracted questions
    final_questions = []
    for q in questions:
        # Remove leading/trailing noise
        q = re.sub(r'^[^a-zA-Z\d]+', '', q)
        q = re.sub(r'[^a-zA-Z\d\?\.\!,\s]+$', '', q)
        # Normalize spaces
        q = re.sub(r'\s+', ' ', q).strip()
        # Ensure proper ending
        if not q.endswith(('?', '.', '!')):
            q = q + '?'
        if len(q) > 15:  # Minimum viable question length
            final_questions.append(q)
    
    return final_questions

def detect_unit(question_text: str) -> str:
    """Detect unit from question text"""
    question_lower = question_text.lower()
    
    # Unit detection based on keywords
    unit_keywords = {
        "unit 1": ["introduction", "overview", "basic", "fundamental"],
        "unit 2": ["perceptron", "neural network", "activation function", "forward propagation"],
        "unit 3": ["backpropagation", "gradient descent", "training", "learning rate"],
        "unit 4": ["cnn", "convolutional", "pooling", "image processing"],
        "unit 5": ["rnn", "recurrent", "lstm", "sequence"],
    }
    
    for unit, keywords in unit_keywords.items():
        for keyword in keywords:
            if keyword in question_lower:
                return unit
    
    return "Unknown"

def export_to_csv(db: Session) -> str:
    """Export questions to CSV file"""
    questions = db.query(models.Question).all()
    
    data = []
    for q in questions:
        data.append({
            "Question": q.text,
            "Unit": q.unit,
            "Source": q.source,
            "Repeated": q.repeat_count
        })
    
    df = pd.DataFrame(data)
    
    # Create temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
    df.to_csv(temp_file.name, index=False)
    
    return temp_file.name

def export_to_pdf(db: Session) -> str:
    """Export questions to PDF file"""
    questions = db.query(models.Question).all()
    
    # Create temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    
    # Create PDF document
    doc = SimpleDocTemplate(temp_file.name, pagesize=letter)
    elements = []
    
    # Add title
    styles = getSampleStyleSheet()
    title = Paragraph("Question Filter Report", styles['Title'])
    elements.append(title)
    
    # Prepare table data
    table_data = [["Question", "Unit", "Source", "Repeated"]]
    
    for q in questions:
        # Truncate long questions for table display
        question_text = q.text
        if len(question_text) > 100:
            question_text = question_text[:97] + "..."
        
        table_data.append([
            question_text,
            q.unit or "Unknown",
            q.source,
            str(q.repeat_count)
        ])
    
    # Create table
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    
    # Build PDF
    doc.build(elements)
    
    return temp_file.name

# Import models here to avoid circular import
import models