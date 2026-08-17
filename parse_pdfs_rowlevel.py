#!/usr/bin/env python3
"""Parser row-level v3 : extraction des lignes individuelles (société, fondateurs, secteur, résultat)
depuis les 85 PDFs de sessions Startup Act.

Stratégie :
1. Détecter la ligne d'en-tête principale (Société/Fondateurs/Secteur/...)
2. Détecter la ligne de sous-en-têtes (Recevabilité/Pitching/Conflit) pour couper les colonnes de vote
3. N'extraire que : Société, Fondateurs, Secteur, Résultat (décision finale)
4. Filtrer les artefacts (scores, N.A, Oui/Non)

Usage : python3 parse_pdfs_rowlevel.py [out_dir]
"""
import json
import os
import re
import sys
from collections import defaultdict

import fitz


def norm(s):
    """Normalisation basique pour comparaison de textes."""
    s = str(s or "").lower()
    for a, b in [("é", "e"), ("è", "e"), ("ê", "e"), ("ë", "e"), ("à", "a"), ("â", "a"),
                  ("î", "i"), ("ô", "o"), ("ù", "u"), ("û", "u")]:
        s = s.replace(a, b)
    s = s.replace("-", "").replace("_", "").replace(".", "").replace(",", " ")
    return re.sub(r"\s+", " ", s).strip()


def collect_lines(page, y_tol=3.0):
    """Regroupe les spans par position Y (tolérance y_tol points)."""
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


def is_noise_row(spans, text_line):
    """Détermine si une ligne est du bruit (titre, en-tête, sous-titre de section)."""
    nl = norm(text_line)

    # Titre du PDF
    if "startup act" in nl and "session" in nl and ("compte" in nl or "rendu" in nl):
        return True

    # En-tête de colonnes principal
    if "societe" in nl and "fondateurs" in nl and "secteur" in nl:
        return True

    # Sous-titre 1er/2ème/3ème Tour + colonnes
    if ("1er tour" in nl or "1er  tour" in nl) and ("recevabilite" in nl or "pitching" in nl):
        return True
    if "recevabilite" in nl and ("pitching" in nl or "conflit" in nl):
        return True

    # Sous-titres de section
    if "prelabels aux labels" in nl or "passage de prelabels" in nl:
        return True
    if len(spans) <= 3 and "retrait" in nl and "label" in nl:
        return True

    # Ligne de conflit d'intérêt
    if "declare" in nl and ("conflit" in nl or "interet" in nl):
        return True
    if nl.strip() in ("d'interet", "d interet", "dinteret", "d'intérêt"):
        return True

    return False


def detect_layout(all_lines):
    """Détecte la structure de colonnes du PDF.
    Retourne (header_y, col_positions, sub_header_y, vote_start_x)
    - col_positions: dict {col_name: x_center} pour les colonnes utiles
    - vote_start_x: position X où commencent les colonnes de vote (pour filtrer)
    """
    header_y = None
    col_positions = {}
    sub_header_y = None
    vote_start_x = None

    for y in sorted(all_lines):
        spans = all_lines[y]
        text_line = " ".join(t for _, _, t in spans)
        nl = norm(text_line)

        # Ligne d'en-tête principal
        if "societe" in nl and "fondateurs" in nl and "secteur" in nl:
            header_y = y
            for x0, x1, t in spans:
                nt = norm(t)
                cx = (x0 + x1) / 2
                if nt in ("societe", "société"):
                    col_positions["societe"] = cx
                elif nt in ("fondateurs", "fondateur"):
                    col_positions["fondateurs"] = cx
                elif nt == "secteur":
                    col_positions["secteur"] = cx
                elif nt in ("label/prelabel", "label prelabel", "label/pre label"):
                    col_positions["label_type"] = cx
                elif nt in ("resultat", "résultat"):
                    col_positions["resultat"] = cx
                elif nt == "commentaires":
                    col_positions["commentaires"] = cx
            continue

        # Ligne de sous-en-têtes (juste après l'en-tête principal)
        if header_y is not None and sub_header_y is None:
            if "recevabilite" in nl or "pitching" in nl:
                sub_header_y = y
                # Le premier span de cette ligne = début des colonnes de vote
                if spans:
                    vote_start_x = spans[0][0]
                break

    return header_y, col_positions, sub_header_y, vote_start_x


def build_smart_boundaries(col_positions, vote_start_x, page_width=800):
    """Construit des frontières intelligentes.
    Inclut Commentaires comme colonne "mur" pour borner Résultat à droite."""
    if not col_positions:
        return {}

    # Colonnes à extraire
    extract_cols = ["societe", "fondateurs", "secteur"]
    if "label_type" in col_positions:
        extract_cols.append("label_type")
    if "resultat" in col_positions:
        extract_cols.append("resultat")

    # Toutes les colonnes pour les frontières (y compris commentaires comme mur)
    all_cols_for_bounds = list(extract_cols)
    if "commentaires" in col_positions:
        all_cols_for_bounds.append("commentaires")

    sorted_cols = sorted(
        [(col_positions[c], c) for c in all_cols_for_bounds if c in col_positions],
        key=lambda x: x[0]
    )

    boundaries = {}
    for i, (cx, name) in enumerate(sorted_cols):
        # Left boundary
        if i > 0:
            left = (sorted_cols[i-1][0] + cx) / 2
        else:
            left = 0

        # Right boundary
        if i < len(sorted_cols) - 1:
            right = (cx + sorted_cols[i+1][0]) / 2
        else:
            right = page_width

        # On ne garde que les colonnes à extraire (pas commentaires)
        if name in extract_cols:
            boundaries[name] = (left, right)

    # Réduire label_type si vote_start_x disponible
    if vote_start_x and "label_type" in boundaries:
        left, right = boundaries["label_type"]
        boundaries["label_type"] = (left, min(right, vote_start_x))

    return boundaries


def assign_by_boundaries(spans, boundaries):
    """Assigne chaque span à la colonne dont il tombe dans les frontières."""
    result = defaultdict(list)
    for x0, x1, t in spans:
        cx = (x0 + x1) / 2
        for col_name, (left, right) in boundaries.items():
            if left <= cx < right:
                result[col_name].append(t)
                break
    return dict(result)


def extract_final_result(text):
    """Extrait la décision finale (Label/Prélabel Accordé/Non Accordé) depuis le texte.
    Ignore les scores et artefacts de vote."""
    if not text:
        return ""
    nl = norm(text)

    # Patterns de décision finale (les plus spécifiques d'abord)
    patterns = [
        (r"prelabel\s+non\s+accorde", "prelabel non accorde"),
        (r"prelabel\s+accorde", "prelabel accorde"),
        (r"label\s+non\s+accorde", "label non accorde"),
        (r"label\s+accorde", "label accorde"),
        (r"ajourne", "ajourne"),
        (r"retrait", "retrait"),
    ]
    for pat, label in patterns:
        if re.search(pat, nl):
            # Extraire le texte complet contenant le pattern
            m = re.search(r"(" + pat + r"[^\n]*)", nl)
            if m:
                return m.group(1).strip()
            return label

    # Si c'est juste "Label" ou "Prélabel" (type sans décision)
    if nl.strip() in ("label", "prelabel"):
        return nl.strip()

    # Si c'est du bruit (scores, N.A, Oui/Non), retourner vide
    if re.match(r"^[\d\s\-\.na]+$", nl) or nl in ("oui", "non", ""):
        return ""

    return text.strip()


def clean_secteur(text):
    """Nettoie le texte secteur en enlevant les artefacts de vote."""
    if not text:
        return text
    words = text.split()
    clean = []
    for w in words:
        nw = norm(w)
        if nw in ("oui", "non", "na", "n.a", ""):
            continue
        if re.match(r"^\d+$", nw):
            continue
        clean.append(w)
    return " ".join(clean)


def parse_pdf_rowlevel(path):
    """Parse un PDF et retourne la liste des entrées."""
    doc = fitz.open(path)
    entries = []

    for page in doc:
        all_lines = collect_lines(page)
        header_y, col_positions, sub_header_y, vote_start_x = detect_layout(all_lines)

        if header_y is None or not col_positions or "societe" not in col_positions:
            continue

        # Déterminer la largeur de page
        page_rect = page.rect
        page_width = page_rect.width if page_rect else 800

        boundaries = build_smart_boundaries(col_positions, vote_start_x, page_width)
        if not boundaries:
            continue

        current_entry = None
        for y in sorted(all_lines):
            if y <= header_y:
                continue

            spans = all_lines[y]
            text_line = " ".join(t for _, _, t in spans)

            if is_noise_row(spans, text_line):
                if current_entry and current_entry.get("societe"):
                    entries.append(current_entry)
                    current_entry = None
                continue

            assigned = assign_by_boundaries(spans, boundaries)

            societe = " ".join(assigned.get("societe", [])).strip()
            fondateurs = " ".join(assigned.get("fondateurs", [])).strip()
            secteur = clean_secteur(" ".join(assigned.get("secteur", [])).strip())
            resultat = extract_final_result(
                " ".join(assigned.get("resultat", []) or
                         assigned.get("label_type", [])).strip()
            )

            has_new_societe = bool(societe and len(societe) > 1)
            has_other_fields = bool(fondateurs or secteur or resultat)

            # Heuristique : le texte societe ressemble à une continuation
            # (prépositions, minuscules, ponctuation en début)
            soc_lower = societe.lower().strip() if societe else ""
            looks_like_continuation = (
                soc_lower.startswith(("pour ", "de ", "du ", "des ", "la ", "le ", "les ", "un ", "une "))
                or soc_lower.startswith(("car ", "et ", "ou ", "mais "))
                or (len(societe) > 2 and societe[0].islower() and " " in societe)
                or soc_lower.endswith((" et", " de", " la", " le"))
            )

            # Cas 1 : juste du texte dans societe → continuation ou début d'entrée
            if has_new_societe and not has_other_fields:
                if current_entry and current_entry.get("societe"):
                    # Continuation du nom multi-ligne
                    current_entry["societe"] += " " + societe
                else:
                    # Début d'une nouvelle entrée
                    current_entry = {
                        "societe": societe,
                        "fondateurs": fondateurs,
                        "secteur": secteur,
                        "resultat": resultat
                    }

            # Cas 2 : societe + autres champs, mais l'entrée précédente n'a pas de fondateurs
            # → c'est la fin du nom multi-ligne + début des données
            elif has_new_societe and has_other_fields and current_entry and not current_entry.get("fondateurs"):
                if current_entry["societe"]:
                    current_entry["societe"] += " " + societe
                else:
                    current_entry["societe"] = societe
                if fondateurs:
                    current_entry["fondateurs"] = fondateurs
                if secteur:
                    current_entry["secteur"] = secteur
                if resultat:
                    current_entry["resultat"] = resultat

            # Cas 2b : societe qui ressemble à une continuation + fondateurs
            # → ajouter au nom, pas créer une nouvelle entrée
            elif has_new_societe and has_other_fields and looks_like_continuation and current_entry:
                if current_entry["societe"]:
                    current_entry["societe"] += " " + societe
                else:
                    current_entry["societe"] = societe
                if fondateurs:
                    if current_entry["fondateurs"]:
                        current_entry["fondateurs"] += ", " + fondateurs
                    else:
                        current_entry["fondateurs"] = fondateurs
                if secteur and not current_entry["secteur"]:
                    current_entry["secteur"] = secteur
                if resultat and not current_entry["resultat"]:
                    current_entry["resultat"] = resultat

            # Cas 3 : nouvelle entrée complète
            elif has_new_societe and has_other_fields:
                if current_entry and current_entry.get("societe"):
                    entries.append(current_entry)
                current_entry = {
                    "societe": societe,
                    "fondateurs": fondateurs,
                    "secteur": secteur,
                    "resultat": resultat
                }

            # Cas 4 : pas de societe → continuation/fondateur supplémentaire
            else:
                if current_entry:
                    if fondateurs:
                        if current_entry["fondateurs"]:
                            current_entry["fondateurs"] += ", " + fondateurs
                        else:
                            current_entry["fondateurs"] = fondateurs
                    if secteur and not current_entry["secteur"]:
                        current_entry["secteur"] = secteur
                    if resultat and not current_entry["resultat"]:
                        current_entry["resultat"] = resultat

        if current_entry and current_entry.get("societe"):
            entries.append(current_entry)

    return entries


def get_session_data(session_key):
    """Charge les données corrigées (session_data) depuis sessions.json + corrections.json."""
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "data")

    sessions_file = os.path.join(base, "sessions.json")
    with open(sessions_file) as f:
        sessions = json.load(f)

    session_entry = None
    for s in sessions:
        if s.get("session") == session_key:
            session_entry = s
            break

    if not session_entry:
        return None

    corrections_file = os.path.join(base, "corrections.json")
    with open(corrections_file) as f:
        corrections_raw = json.load(f)

    correction = None
    for c in corrections_raw.get("corrections", []):
        if c.get("session") == session_key:
            correction = c
            break

    candidatures = session_entry.get("candidatures", 0)
    labels = session_entry.get("labels", 0)
    preLabels = session_entry.get("preLabels", 0)
    retraits = session_entry.get("retraits", 0)
    conversions = session_entry.get("conversions", 0)

    statut = "corrigee" if correction else "conforme"
    taux = round(labels / candidatures * 100, 1) if candidatures else 0

    session_data = {
        "candidatures": candidatures,
        "labels": labels,
        "preLabels": preLabels,
        "taux_acceptation_pct": taux,
        "statut": statut,
        "retraits": retraits,
        "conversions": conversions,
        "newLabels": labels - conversions
    }

    if correction:
        session_data["correction"] = correction

    return session_data


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "public/data/session-pdfs-json"
    base = "public/data/session-pdfs"

    os.makedirs(out_dir, exist_ok=True)

    total = 0
    for f in sorted(os.listdir(base)):
        if not f.endswith(".pdf"):
            continue

        sess = f.replace("session_", "").replace(".pdf", "")
        year, month = sess.split("_")
        session_key = f"{int(month):02d}/{year}"

        pdf_path = os.path.join(base, f)
        print(f"Parsing {f}...", end=" ", flush=True)

        entries = parse_pdf_rowlevel(pdf_path)
        session_data = get_session_data(session_key)

        out = {
            "session": session_key,
            "annee": int(year),
            "mois": int(month),
            "pdf": f,
            "nb_entrees": len(entries),
            "source": "Extraction des PDF officiels des sessions — startup.gov.tn",
            "entrees": entries,
            "session_data": session_data or {}
        }

        out_file = os.path.join(out_dir, f"session_{year}_{month}.json")
        with open(out_file, "w") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=2)

        print(f"{len(entries)} entrées")
        total += 1

    print(f"\nTerminé : {total} fichiers générés dans {out_dir}")


if __name__ == "__main__":
    main()
