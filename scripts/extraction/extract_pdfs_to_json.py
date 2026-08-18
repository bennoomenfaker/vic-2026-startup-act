#!/usr/bin/env python3
"""
Extraction du texte des 85 PDFs de sessions Startup Act vers 85 fichiers JSON.

Format de sortie (comparable à l'extraction opencode dans /tmp/pdf_texts) :
  /tmp/buffy_pdf_texts/session_YYYY_MM.json   (1 fichier par session)
  /tmp/buffy_pdf_texts/summary.json           (résumé : pages / text_length / has_text)

Chaque JSON contient :
  - session      : "MM/YYYY"
  - file         : nom du PDF source
  - pages        : nombre de pages du PDF
  - text_length  : longueur totale du texte extrait (concaténation des pages)
  - has_text     : text_length >= 100 (seuil identique à l'analyse opencode)
  - pages_text   : [{page, text}] texte brut par page (méthode PyMuPDF get_text)
"""
import json
import os
import sys

import fitz  # PyMuPDF

PDF_DIR = "public/data/session-pdfs"
OUT_DIR = "/tmp/buffy_pdf_texts"
TEXT_THRESHOLD = 100  # en dessous : has_text = false


def extract_pdf(pdf_path):
    """Extrait le texte de chaque page d'un PDF."""
    doc = fitz.open(pdf_path)
    pages_text = []
    total_len = 0
    for i, page in enumerate(doc):
        text = page.get_text()
        total_len += len(text)
        pages_text.append({"page": i + 1, "text": text})
    pages = doc.page_count
    doc.close()
    return pages, total_len, pages_text


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    pdfs = sorted(f for f in os.listdir(PDF_DIR) if f.endswith(".pdf"))
    print(f"{len(pdfs)} PDFs trouvés dans {PDF_DIR}")

    summary = {}
    for fname in pdfs:
        path = os.path.join(PDF_DIR, fname)
        pages, total_len, pages_text = extract_pdf(path)

        # session "MM/YYYY" depuis "session_YYYY_MM.pdf"
        base = fname.replace(".pdf", "")            # session_2019_04
        parts = base.split("_")                     # ["session", "2019", "04"]
        session = f"{parts[2]}/{parts[1]}"          # 04/2019

        has_text = total_len >= TEXT_THRESHOLD

        data = {
            "session": session,
            "file": fname,
            "pages": pages,
            "text_length": total_len,
            "has_text": has_text,
            "pages_text": pages_text,
        }
        out_file = os.path.join(OUT_DIR, f"{base}.json")
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        summary[session] = {
            "file": fname,
            "pages": pages,
            "text_length": total_len,
            "has_text": has_text,
        }
        status = "OK " if has_text else "VIDE"
        print(f"  [{status}] {fname}: {pages} pages, {total_len} chars")

    with open(os.path.join(OUT_DIR, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    n_ok = sum(1 for v in summary.values() if v["has_text"])
    print(f"\nTerminé : {len(summary)} JSON écrits dans {OUT_DIR}")
    print(f"  - {n_ok} sessions avec texte, {len(summary) - n_ok} sans texte extractible")
    return 0


if __name__ == "__main__":
    sys.exit(main())
