#!/usr/bin/env python3
"""
Compare l'extraction Buffy (/tmp/buffy_pdf_texts) avec celle d'opencode (/tmp/pdf_texts).

Critères par session :
  1. pages          : identiques ?
  2. has_text       : identique ?
  3. text_length    : écart relatif (méthodes différentes : PyMuPDF vs pdftotext)
  4. contenu        : % de lignes normalisées de chaque page présentes dans les deux extractions
"""
import json
import os
import re

BUFFY_DIR = "/tmp/buffy_pdf_texts"
OPENCODE_DIR = "/tmp/pdf_texts"

def normalize_lines(text):
    lines = []
    for line in text.split("\n"):
        line = re.sub(r"\s+", " ", line).strip().lower()
        if line:
            lines.append(line)
    return lines

def read_opencode_session(name):
    """Lit le .txt opencode → {page: [lignes normalisées]}."""
    path = os.path.join(OPENCODE_DIR, f"{name}.txt")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    # découpage sur les marqueurs "--- PAGE N ---"
    parts = re.split(r"--- PAGE (\d+) ---", raw)
    # parts = ["", "1", text1, "2", text2, ...]
    pages = {}
    for i in range(1, len(parts), 2):
        pages[int(parts[i])] = normalize_lines(parts[i + 1])
    return pages

def main():
    with open(os.path.join(BUFFY_DIR, "summary.json"), encoding="utf-8") as f:
        buffy = json.load(f)
    with open(os.path.join(OPENCODE_DIR, "summary.json"), encoding="utf-8") as f:
        opencode = json.load(f)

    print(f"{'Session':<10} {'Pages B/O':<10} {'hasTxt':<8} {'lenB':>6} {'lenO':>6} {'écart%':>7}  Contenu par page")
    print("-" * 90)

    n_pages_diff = 0
    n_hastext_diff = 0
    total_lines_mine = 0
    total_lines_shared = 0

    for session in sorted(buffy.keys()):
        b, o = buffy[session], opencode.get(session)
        if o is None:
            print(f"{session:<10} MANQUANT chez opencode")
            continue

        pages_ok = b["pages"] == o["pages"]
        hastext_ok = b["has_text"] == o["has_text"]
        if not pages_ok: n_pages_diff += 1
        if not hastext_ok: n_hastext_diff += 1

        rel = abs(b["text_length"] - o["text_length"]) / max(o["text_length"], 1) * 100

        # contenu par page — nom fichier : session "04/2019" → session_2019_04
        mm, yyyy = session.split("/")
        name = f"session_{yyyy}_{mm}"
        op_pages = read_opencode_session(name)

        page_reports = []
        if op_pages is not None:
            bj = json.load(open(os.path.join(BUFFY_DIR, f"{name}.json"), encoding="utf-8"))
            for p in bj["pages_text"]:
                mine = normalize_lines(p["text"])
                theirs = op_pages.get(p["page"], [])
                shared = len(set(mine) & set(theirs))
                total_lines_mine += len(mine)
                total_lines_shared += shared
                pct = 100 * shared / max(len(mine), 1)
                page_reports.append(f"p{p['page']}:{pct:.0f}%")
        else:
            page_reports.append("txt absent")

        flag = ""
        if not pages_ok: flag += " ⚠️PAGES"
        if not hastext_ok: flag += " ⚠️HAS_TEXT"

        print(f"{session:<10} {b['pages']}/{o['pages']:<8} {'T' if b['has_text'] else 'F':<8} {b['text_length']:>6} {o['text_length']:>6} {rel:>6.1f}%  {' '.join(page_reports)}{flag}")

    print("-" * 90)
    print(f"\nRésumé :")
    print(f"  Sessions comparées : {len(buffy)}")
    print(f"  Écarts de pages    : {n_pages_diff}")
    print(f"  Écarts has_text    : {n_hastext_diff}")
    if total_lines_mine:
        print(f"  Lignes partagées   : {total_lines_shared}/{total_lines_mine} ({100*total_lines_shared/max(total_lines_mine,1):.1f}%)")

if __name__ == "__main__":
    main()
