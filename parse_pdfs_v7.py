#!/usr/bin/env python3
"""Parser v7 : extraction par positions de spans (get_text('dict')).

Robuste pour tous les formats de PDFs de sessions (2019-2026).

Stratégie :
- On détecte les positions x des colonnes "Résultat" et "Commentaires" via
  les lignes d'en-tête (qui peuvent être réparties sur plusieurs lignes).
- Dans la table principale, le type (Label/Prélabel) est déduit du texte
  du résultat lui-même ("Label accordé" vs "Pré-label accordé").
- La cellule résultat est celle dont le centre est le plus à gauche parmi
  les textes commençant par label/prelabel + "accordé", et située à gauche
  du point médian entre Résultat et Commentaires.

Usage : python3 parse_pdfs_v7.py [out.json]
"""
import json
import os
import re
import sys

import fitz


def norm(s):
    s = str(s or "").lower()
    for a, b in [("é", "e"), ("è", "e"), ("ê", "e"), ("ë", "e"), ("à", "a"), ("â", "a"), ("î", "i"), ("ô", "o")]:
        s = s.replace(a, b)
    s = s.replace("-", "").replace("_", "").replace(".", "").replace("  ", " ")
    return re.sub(r"\s+", " ", s).strip()


def is_result_cell(text):
    """Retourne 'label' | 'prelabel' si le texte est une cellule résultat
    accordée (sans 'non'), sinon None. Le texte doit commencer par label/prelabel
    et contenir 'accorde'."""
    n = norm(text)
    if "non" in n:
        return None
    if "accorde" not in n:
        return None
    if n.startswith("prelabel"):
        return "prelabel"
    if n.startswith("label"):
        return "label"
    return None


def collect_lines(page, y_tol=3.0):
    d = page.get_text("dict")
    lines = {}
    for block in d["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                t = span["text"]
                if not t.strip():
                    continue
                y = round(span["bbox"][1] / y_tol) * y_tol
                lines.setdefault(y, []).append((span["bbox"][0], span["bbox"][2], t))
    return {y: sorted(spans) for y, spans in lines.items()}


def parse_pdf(path):
    doc = fitz.open(path)
    new_labels = 0
    new_prelabels = 0
    conversions = 0
    retraits = 0
    section = "main"
    x_result = None
    x_comment = None

    def center(sp):
        return (sp[0] + sp[1]) / 2

    for page in doc:
        lines = collect_lines(page)
        for y in sorted(lines):
            spans = lines[y]
            text_line = " ".join(t for _, _, t in spans)
            nl = norm(text_line)

            # Section markers
            if "prelabels aux labels" in nl or "passage de prelabels" in nl:
                section = "conversion"
                x_result = None
                x_comment = None
                continue
            if len(spans) <= 2 and "retrait" in nl and "label" in nl and section != "retrait":
                section = "retrait"
                x_result = None
                x_comment = None
                continue

            # Update column positions from header keywords
            for sx0, sx1, t in spans:
                n = norm(t)
                if n == "resultat":
                    x_result = sx0
                elif n == "commentaires":
                    x_comment = sx0

            if section == "main":
                if x_result is None:
                    continue
                matches = [(center(sp), sp) for sp in spans if is_result_cell(sp[2])]
                if not matches:
                    continue
                matches.sort()
                c, sp = matches[0]
                if x_comment is not None and c >= (x_result + x_comment) / 2:
                    continue
                if is_result_cell(sp[2]) == "label":
                    new_labels += 1
                else:
                    new_prelabels += 1
            elif section == "conversion":
                if x_result is None:
                    continue
                matches = [(center(sp), sp) for sp in spans if is_result_cell(sp[2]) == "label"]
                if not matches:
                    continue
                matches.sort()
                c, sp = matches[0]
                if x_comment is not None and c >= (x_result + x_comment) / 2:
                    continue
                conversions += 1
            elif section == "retrait":
                if any("retrait" in norm(t) and "label" in norm(t) for _, _, t in spans):
                    retraits += 1

    return {
        "new_labels": new_labels,
        "new_prelabels": new_prelabels,
        "conversions": conversions,
        "retraits": retraits,
        "total_labels": new_labels + conversions,
        "total_prelabels": new_prelabels,
    }


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/opencode/pdf_parsed_v7.json"
    base = "public/data/session-pdfs"
    results = {}
    for f in sorted(os.listdir(base)):
        if not f.endswith(".pdf"):
            continue
        sess = f.replace("session_", "").replace(".pdf", "")
        month, year = sess.split("_")
        key = f"{int(month):02d}/{year}"
        r = parse_pdf(os.path.join(base, f))
        results[key] = r
        print(f"{key}: {r}", flush=True)
    with open(out, "w") as fh:
        json.dump(results, fh, ensure_ascii=False, indent=1)
    print(f"Saved {len(results)} sessions to {out}")


if __name__ == "__main__":
    main()
