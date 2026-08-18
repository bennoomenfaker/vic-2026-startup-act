#!/usr/bin/env python3
"""
Convertit les 85 PDFs de sessions en markdown dans /tmp/freebuff/md/.
- 83 sessions textuelles: PyMuPDF extraction
- 2 sessions image (2020_12, 2021_01): texte CR fourni
"""
import fitz
import os
import json
import re

PDF_DIR = "public/data/session-pdfs"
OUT_DIR = "/tmp/freebuff/md"
IMAGE_SESSIONS = {"session_2020_12.pdf", "session_2021_01.pdf"}

def session_id_from_filename(fname):
    """Extract session id like 2020_07 from session_2020_07.pdf"""
    return fname.replace("session_", "").replace(".pdf", "")

def pdf_to_markdown(pdf_path, fname):
    """Extract text from PDF and format as markdown."""
    doc = fitz.open(pdf_path)
    session_id = session_id_from_filename(fname)
    
    lines = []
    lines.append(f"# Session {session_id}")
    lines.append("")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        if text.strip():
            lines.append(f"## Page {page_num + 1}")
            lines.append("")
            # Clean up the text
            for line in text.split("\n"):
                lines.append(line.rstrip())
            lines.append("")
    
    doc.close()
    return "\n".join(lines)

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    
    pdfs = sorted([f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")])
    print(f"Found {len(pdfs)} PDFs")
    
    stats = {"ok": 0, "image": 0, "empty": 0}
    image_sessions = []
    
    for fname in pdfs:
        pdf_path = os.path.join(PDF_DIR, fname)
        md_path = os.path.join(OUT_DIR, fname.replace(".pdf", ".md"))
        
        if fname in IMAGE_SESSIONS:
            # Mark as image - will be filled later
            session_id = session_id_from_filename(fname)
            image_sessions.append(session_id)
            with open(md_path, "w") as f:
                f.write(f"# Session {session_id}\n\n")
                f.write(f"*[Image PDF - texte OCR à compléter]*\n")
            stats["image"] += 1
            continue
        
        # Extract text from PDF
        md_content = pdf_to_markdown(pdf_path, fname)
        
        # Check if any real content
        text_only = re.sub(r'#.*\n', '', md_content).strip()
        if len(text_only) < 20:
            stats["empty"] += 1
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        stats["ok"] += 1
    
    print(f"OK: {stats['ok']}, Image: {stats['image']}, Empty: {stats['empty']}")
    print(f"Image sessions to fill: {image_sessions}")
    print(f"Output: {OUT_DIR}/")

if __name__ == "__main__":
    main()
