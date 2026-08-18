#!/usr/bin/env python3
"""Extract text from PDFs using PyMuPDF and save to files"""
import fitz
import json
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using PyMuPDF"""
    doc = fitz.open(pdf_path)
    text = ''
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def main():
    pdf_dir = Path('public/data/session-pdfs')
    output_dir = Path('/tmp/pymupdf_texts')
    output_dir.mkdir(exist_ok=True)
    
    results = []
    
    for pdf_file in sorted(pdf_dir.glob('session_*.pdf')):
        text = extract_text_from_pdf(pdf_file)
        
        # Save text to file
        output_file = output_dir / f'{pdf_file.stem}.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        results.append({
            'session': pdf_file.stem.replace('session_', ''),
            'chars': len(text)
        })
        print(f'✅ {pdf_file.stem}: {len(text)} chars')
    
    # Save summary
    summary_file = output_dir / 'summary.json'
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total_sessions': len(results),
            'sessions': results
        }, f, ensure_ascii=False, indent=2)
    
    print(f'\n=== TOTAL: {len(results)} sessions ===')

if __name__ == '__main__':
    main()
