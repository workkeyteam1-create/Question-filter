import pdfplumber
import PyPDF2
import re

# Test text that simulates the corrupted extraction you showed
test_text = """(-_-* ri.,B Gove rrr m en t Coll e ge o f trn gi f tl t u t g ab a d ol Golcrnn" r c" r" rt' .'o.1f M1aSh'a-r-a slttra) (An'+utonomouIhrstitrrte M;;...
ID: 1)

Q1. What is machine learning? Explain its applications.
Q2. Describe the perceptron model with diagram.
Q3. How does backpropagation work?
Q4. Explain CNN architecture.
Q5. What is LSTM? Why is it used?
"""

def extract_questions_improved(text: str):
    """Improved question extraction with better handling of noisy text"""
    questions = []
    
    # First, clean up the text - remove excessive noise but preserve structure
    # Remove sequences of random special characters that aren't part of questions
    cleaned = re.sub(r'[^\w\s\.\?\!\,\:\;\(\)\[\]\d]+', ' ', text)
    # Normalize multiple spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    print("=== Original Text ===")
    print(text[:200])
    print("\n=== Cleaned Text ===")
    print(cleaned[:200])
    
    # Pattern 1: Q followed by number (Q1., Q2:, Question 1, etc.)
    pattern_q = r'(?:Q\.?\s*\d+[\.:]?\s*|Question\s*\d+[\.:]?\s*)(.+?)(?=(?:Q\.?\s*\d+|Question\s*\d+|$))'
    
    # Pattern 2: Number followed by . or ) at start of line or after whitespace
    pattern_num = r'(?:^|\n)\s*(\d+[\.\)]\s*)(.+?)(?=(?:\n\s*\d+[\.\)]\s*|$))'
    
    # Pattern 3: Standalone questions with question words
    pattern_words = r'((?:What|How|Why|When|Where|Who|Explain|Describe|Define|Discuss|Calculate|Show|Prove)[\w\s,]+[\.\\?])'
    
    # Try pattern 1 first (most common for exam papers)
    matches = re.findall(pattern_q, cleaned, re.IGNORECASE | re.DOTALL)
    print(f"\nPattern 1 matches: {len(matches)}")
    for m in matches[:3]:
        print(f"  - {m.strip()[:50]}")
    
    if matches:
        for match in matches:
            q = match.strip()
            if len(q) > 10:
                questions.append(q)
    
    # If no matches, try pattern 2
    if not questions:
        matches = re.findall(pattern_num, cleaned, re.IGNORECASE | re.MULTILINE | re.DOTALL)
        print(f"\nPattern 2 matches: {len(matches)}")
        for m in matches[:3]:
            print(f"  - {m[1].strip()[:50]}")
        
        if matches:
            for match in matches:
                q = match[1].strip()
                if len(q) > 10:
                    questions.append(q)
    
    # If still no matches, try pattern 3
    if not questions:
        matches = re.findall(pattern_words, cleaned, re.IGNORECASE)
        print(f"\nPattern 3 matches: {len(matches)}")
        for m in matches[:3]:
            print(f"  - {m.strip()[:50]}")
        
        if matches:
            for match in matches:
                q = match.strip()
                if len(q) > 10:
                    questions.append(q)
    
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

# Test with the simulated corrupted text
result = extract_questions_improved(test_text)
print(f"\n=== Final Extracted Questions ({len(result)}) ===")
for i, q in enumerate(result, 1):
    print(f"{i}. {q}")
