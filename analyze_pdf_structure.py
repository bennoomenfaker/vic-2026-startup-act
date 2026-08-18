#!/usr/bin/env python3
"""
Analyze the structure of a few PDFs to understand the table format.
"""
import subprocess

PDF_DIR = "public/data/session-pdfs"

def extract_pdf_text(pdf_path):
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", pdf_path, "-"],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        return result.stdout
    except:
        return ""

# Analyze a few representative PDFs
pdfs = [
    "session_2019_03.pdf",  # early format
    "session_2020_01.pdf",  # has "Label/Prélabel" column
    "session_2021_04.pdf",  # large session
    "session_2024_01.pdf",  # recent format
    "session_2026_01.pdf",  # latest
]

for pdf_name in pdfs:
    print(f"\n{'='*80}")
    print(f"PDF: {pdf_name}")
    print(f"{'='*80}")
    text = extract_pdf_text(f"{PDF_DIR}/{pdf_name}")
    print(text[:3000])
    print("...")
