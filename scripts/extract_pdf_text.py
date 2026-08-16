#!/usr/bin/env python3
"""Ré-extraction du texte brut des 85 PDF de sessions — pour relecture/croisement.

Les données JSON actuelles (public/data/session-pdfs-json/) proviennent d'un
parse PDF imparfait. Ce script régénère le texte brut de chaque compte-rendu
(pdftotext -layout si disponible, sinon pymupdf) afin de permettre :
  - une relecture humaine directe ;
  - une re-extraction indépendante par un agent IA (voir docs/relecture_pdf_agent_prompt.md) ;
  - un croisement avec les données manuelles (public/data/manual_sessions/).

Sortie :
  --out/pdf-text-recheck/YYYY_MM.txt   (texte brut, mise en page conservée)
  --out/pdf-text-recheck/manifest.json (session → fichier, pages, lignes)

Usage :
  python3 scripts/extract_pdf_text.py
  python3 scripts/extract_pdf_text.py --out /tmp/opencode/pdf_text_recheck
  python3 scripts/extract_pdf_text.py --session 2025_12
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_DIR = os.path.join(ROOT, 'public', 'data', 'session-pdfs')
DEFAULT_OUT = os.path.join(ROOT, 'public', 'data', 'pdf-text-recheck')


def extract_pdftotext(pdf_path):
    """pdftotext -layout : meilleure fidélité pour les tableaux de comptes-rendus."""
    r = subprocess.run(
        ['pdftotext', '-layout', pdf_path, '-'],
        capture_output=True, text=True, timeout=120)
    return r.stdout if r.returncode == 0 else None


def extract_pymupdf(pdf_path):
    import fitz  # PyMuPDF
    doc = fitz.open(pdf_path)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    doc.close()
    return '\n\f'.join(pages)


def main():
    ap = argparse.ArgumentParser(description='Ré-extraction texte des PDF de sessions')
    ap.add_argument('--out', default=DEFAULT_OUT, help='dossier de sortie')
    ap.add_argument('--session', default=None,
                    help='une seule session (ex. 2025_12) au lieu de toutes')
    args = ap.parse_args()

    if not os.path.isdir(PDF_DIR):
        sys.exit(f'dossier introuvable : {PDF_DIR}')
    pdfs = sorted(f for f in os.listdir(PDF_DIR) if re.match(r'session_\d{4}_\d{2}\.pdf$', f))
    if args.session:
        pdfs = [f for f in pdfs if f'_{args.session}.' in f or args.session in f]
    if not pdfs:
        sys.exit('aucun PDF de session trouvé')

    os.makedirs(args.out, exist_ok=True)
    manifest = []
    for fname in pdfs:
        stem = fname[:-4]  # session_YYYY_MM
        pdf_path = os.path.join(PDF_DIR, fname)
        text = extract_pdftotext(pdf_path) or extract_pymupdf(pdf_path)
        if text is None:
            print(f'  ✗ {stem}: extraction impossible', file=sys.stderr)
            continue
        out_path = os.path.join(args.out, stem + '.txt')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(text)
        n_pages = text.count('\f') + 1
        n_lines = len([l for l in text.splitlines() if l.strip()])
        manifest.append({'session': stem, 'pdf': fname, 'pages': n_pages, 'lignes': n_lines})
        print(f'  ✓ {stem}: {n_pages} pages, {n_lines} lignes → {os.path.relpath(out_path, ROOT)}')

    with open(os.path.join(args.out, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump({'note': 'Ré-extraction texte brut des comptes-rendus de sessions.',
                   'extrait_le': None, 'nb_sessions': len(manifest), 'sessions': manifest},
                  f, ensure_ascii=False, indent=1)
    print(f'\n{len(manifest)}/{len(pdfs)} sessions extraites dans {args.out}')


if __name__ == '__main__':
    main()
