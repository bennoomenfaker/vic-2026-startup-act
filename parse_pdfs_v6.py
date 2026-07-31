#!/usr/bin/env python3
"""Parser v6 : extraction par positions de spans (get_text('dict')).

Robuste pour tous les formats de PDFs de sessions (2019-2026).
Usage : python3 parse_pdfs_v6.py [out.json]
"""
import json
import os
import re
import sys

import fitz


def norm(s):
    s = str(s or "").lower()
    for a, b in [("é", "e"), ("è", "e"), ("ê", "e"), ("ë", "e"), ("à", "a"), ("â", "a"), ("î", "i")]:
        s = s.replace(a, b)
    s = s.replace("-", "").replace("_", "").replace(".", "").replace("  ", " ")
    return re.sub(r"\s+", " ", s).strip()


RESULT_LABEL = "label accorde"
RESULT_PRELABEL = "prelabel accorde"


def is_result(s):
    n = norm(s)
    if n in (RESULT_LABEL, RESULT_PRELABEL):
        return n
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
    x_type = None

    for page in doc:
        lines = collect_lines(page)
        for y in sorted(lines):
            spans = lines[y]
            text_line = " ".join(t for _, _, t in spans)

            # Detect section markers
            nl = norm(text_line)
            if "prelabels aux labels" in nl or "passage de prelabels" in nl:
                section = "conversion"
                x_result = None
                x_comment = None
                continue
            if "retrait de label" in nl:
                section = "retrait"
                x_result = None
                x_comment = None
                continue

            # Detect header lines to capture column x positions
            has_type = any(norm(t) in ("label", "prelabel", "label/prelabel") for _, _, t in spans)
            has_result = any(norm(t) == "resultat" for _, _, t in spans)
            has_societe = any(norm(t) == "societe" for _, _, t in spans)
            has_session = any(norm(t) in ("session", "d'obtention") or "session" in norm(t) for _, _, t in spans)

            if has_result and has_societe:
                if section == "conversion":
                    # conversion header: Résultat + Commentaires (different x)
                    for _, _, t in spans:
                        n = norm(t)
                        if n == "resultat":
                            x_result = [s[0] for s in spans if norm(s[2]) == "resultat"][0]
                            x_comment = [s[0] for s in spans if norm(s[2]) == "commentaires"][0] \
                                if any(norm(s[2]) == "commentaires" for s in spans) else x_comment
                elif section == "retrait":
                    for _, _, t in spans:
                        n = norm(t)
                        if n == "resultat":
                            x_result = [s[0] for s in spans if norm(s[2]) == "resultat"][0]
                else:
                    if has_type:
                        for _, _, t in spans:
                            n = norm(t)
                            if n == "label/prelabel":
                                x_type = [s[0] for s in spans if norm(s[2]) == "label/prelabel"][0]
                            elif n == "resultat":
                                x_result = [s[0] for s in spans if norm(s[2]) == "resultat"][0]
                            elif n == "commentaires":
                                x_comment = [s[0] for s in spans if norm(s[2]) == "commentaires"][0]
                continue

            if section == "main":
                if x_result is None or x_type is None:
                    continue
                # find result cell: span whose center is closest to x_result, but before commentaires boundary
                result_spans = []
                bound = ((x_result + x_comment) / 2) if x_comment else x_result + 80
                for sx0, sx1, t in spans:
                    center = (sx0 + sx1) / 2
                    if center < bound and norm(t) in (RESULT_LABEL, RESULT_PRELABEL):
                        result_spans.append((center, t))
                if not result_spans:
                    continue
                result_spans.sort()
                result_text = norm(result_spans[0][1])
                if result_text == RESULT_LABEL:
                    new_labels += 1
                elif result_text == RESULT_PRELABEL:
                    new_prelabels += 1
            elif section == "conversion":
                if x_result is None:
                    continue
                bound = ((x_result + x_comment) / 2) if x_comment else x_result + 80
                for sx0, sx1, t in spans:
                    center = (sx0 + sx1) / 2
                    if center < bound and norm(t) == RESULT_LABEL:
                        conversions += 1
                        break
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
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/opencode/pdf_parsed_v6.json"
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
