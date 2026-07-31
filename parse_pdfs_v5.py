#!/usr/bin/env python3
"""Parser v5 : extrait labels/prélabels/conversions/retraits des PDFs de sessions.

Utilise PyMuPDF find_tables() pour une extraction structurée fiable.
Usage : python3 parse_pdfs_v5.py [--out chemin.json]
"""
import json
import re
import sys
import time

import fitz


def norm(s):
    s = str(s or "").lower()
    for a, b in [("é", "e"), ("è", "e"), ("ê", "e"), ("ë", "e"), ("à", "a"), ("â", "a")]:
        s = s.replace(a, b)
    s = s.replace("-", "").replace("_", "").replace(".", "").replace("  ", " ").strip()
    return re.sub(r"\s+", " ", s)


def classify_result(cell):
    n = norm(cell)
    if "non" in n and "accorde" in n:
        return "rejected_label" if "label" in n and "prelabel" not in n else (
            "rejected_prelabel" if "prelabel" in n else None)
    if "accorde" in n:
        if "prelabel" in n:
            return "granted_prelabel"
        if "label" in n:
            return "granted_label"
    return None


def classify_type(cell):
    n = norm(cell)
    if n in ("label", "prelabel"):
        return n
    return None


def parse_pdf(path, timeout_per_page=45):
    doc = fitz.open(path)
    new_labels = 0
    new_prelabels = 0
    conversions = 0
    retraits = 0
    section = "main"
    errors = []

    for pno, page in enumerate(doc):
        t0 = time.time()
        try:
            tabs = page.find_tables()
        except Exception as e:
            errors.append(f"page {pno + 1} find_tables: {e}")
            continue
        if time.time() - t0 > timeout_per_page:
            errors.append(f"page {pno + 1} slow")
            continue

        for table in tabs.tables:
            try:
                data = table.extract()
            except Exception as e:
                errors.append(f"page {pno + 1} extract: {e}")
                continue
            if not data:
                continue

            for row in data:
                if not row or all(not str(c).strip() for c in row):
                    continue
                joined = norm(" | ".join(str(c) for c in row))
                if "passage de prelabels aux labels" in joined:
                    section = "conversion"
                    continue
                if "retrait de label startup" in joined or "retrait de label" in joined:
                    section = "retrait"
                    continue

                if section == "main":
                    type_cell = None
                    result = None
                    for cell in row:
                        t = classify_type(cell)
                        if t:
                            type_cell = t
                        r = classify_result(cell)
                        if r:
                            result = r
                    if type_cell == "label" and result == "granted_label":
                        new_labels += 1
                    elif type_cell == "prelabel" and result == "granted_prelabel":
                        new_prelabels += 1
                elif section == "conversion":
                    if any(classify_result(c) == "granted_label" for c in row):
                        conversions += 1
                elif section == "retrait":
                    for c in row:
                        n = norm(c)
                        if "retrait" in n and "label" in n:
                            retraits += 1
                            break

    return {
        "new_labels": new_labels,
        "new_prelabels": new_prelabels,
        "conversions": conversions,
        "retraits": retraits,
        "total_labels": new_labels + conversions,
        "total_prelabels": new_prelabels,
        "errors": errors,
    }


def main():
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/opencode/pdf_parsed_v5.json"
    import os
    base = "public/data/session-pdfs"
    results = {}
    files = sorted(os.listdir(base))
    for f in files:
        if not f.endswith(".pdf"):
            continue
        sess = f.replace("session_", "").replace(".pdf", "")
        month, year = sess.split("_")
        key = f"{int(month):02d}/{year}"
        t0 = time.time()
        r = parse_pdf(os.path.join(base, f))
        dt = time.time() - t0
        r.pop("errors", None)
        results[key] = r
        print(f"{key}: {r} ({dt:.1f}s)", flush=True)
    with open(out, "w") as fh:
        json.dump(results, fh, ensure_ascii=False, indent=1)
    print(f"Saved to {out} ({len(results)} sessions)")


if __name__ == "__main__":
    main()
