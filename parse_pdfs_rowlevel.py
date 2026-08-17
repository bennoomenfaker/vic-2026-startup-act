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

    # Titre de session seul (ex: "Session 25 | Avril 2021 | Compte-Rendu")
    if "session" in nl and ("compte" in nl or "rendu" in nl):
        return True

    # En-tête de colonnes principal
    if "societe" in nl and "fondateurs" in nl and "secteur" in nl:
        return True

    # Sous-titre 1er/ème/ème Tour + colonnes
    if ("1er tour" in nl or "1er  tour" in nl) and ("recevabilite" in nl or "pitching" in nl):
        return True
    if "recevabilite" in nl and ("pitching" in nl or "conflit" in nl):
        return True

    # Sous-titre "Label/Prélabel" seul
    if nl.strip() in ("label/prelabel", "label prelabel", "label/pre label", "label/prelabel", "resultat"):
        return True

    # Sous-titres de section
    if "prelabels aux labels" in nl or "passage de prelabels" in nl:
        return True
    if "passage de" in nl and "labels" in nl:
        return True
    if len(spans) <= 3 and "retrait" in nl and "label" in nl:
        return True

    # Ligne de conflit d'intérêt
    if "declare" in nl and ("conflit" in nl or "interet" in nl):
        return True
    if nl.strip() in ("d'interet", "d interet", "dinteret", "d'intérêt"):
        return True

    # Lignes de header de section (Société / Fondateurs / Secteur / Décision / Commentaires)
    if "societe" in nl and "secteur" in nl and ("decision" in nl or "commentaires" in nl):
        return True

    # Ligne "Société Secteur Bus Software IoT" (séparateur de section)
    if nl.startswith("societe secteur") or nl.startswith("société secteur"):
        return True

    # Ligne "Décision Commentaires"
    if nl.startswith("decision commentaires"):
        return True

    # Lignes de texte légal / droits
    if len(spans) > 5 and "conformement" in nl:
        return True
    if len(spans) > 5 and "bénéficiaires" in nl and "label" in nl:
        return True

    # Ligne purement numérique ou N.A
    if re.match(r"^[\d\s\-\.na/]+$", nl) or nl.strip() in ("oui", "non", ""):
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


def normalize_result(r):
    """Normalise le résultat pour avoir des variantes cohérentes."""
    r = r.strip()
    nl = norm(r)
    
    # Ne normaliser que si le texte contient des mots-clés de décision
    if not any(k in nl for k in ["label", "prelabel", "accorde", "non", "refus", "ajourne", "retrait"]):
        return r
    
    # Labels
    if "label" in nl and "prelabel" not in nl:
        if "non" in nl or "refus" in nl:
            return "label non accorde"
        return "label accorde"
    
    # Prelabels
    if "prelabel" in nl:
        if "non" in nl or "refus" in nl:
            return "prelabel non accorde"
        return "prelabel accorde"
    
    # Accordé sans type
    if nl in ("accorde", "label accordé"):
        return "label accorde"
    
    return r


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
                return normalize_result(m.group(1).strip())
            return normalize_result(label)

    # Si c'est juste "Label" ou "Prélabel" (type sans décision)
    if nl.strip() in ("label", "prelabel"):
        return normalize_result(nl.strip())

    # Si c'est du bruit (scores, N.A, Oui/Non), retourner vide
    if re.match(r"^[\d\s\-\.na]+$", nl) or nl in ("oui", "non", ""):
        return ""

    # Appliquer la normalisation sur le texte restant
    return normalize_result(text.strip())


def clean_secteur(text):
    """Nettoie le texte secteur en enlevant les artefacts de vote et les mois."""
    if not text:
        return text
    words = text.split()
    clean = []
    mois = ["janvier", "fevrier", "mars", "avril", "mai", "juin",
            "juillet", "aout", "septembre", "octobre", "novembre", "decembre"]
    for w in words:
        nw = norm(w)
        if nw in ("oui", "non", "na", "n.a", ""):
            continue
        if re.match(r"^\d+$", nw):
            continue
        if nw in mois:
            continue
        clean.append(w)
    return " ".join(clean)


def postprocess_entries(entries):
    """Nettoie les entrées : fusionne résultats splités, filtre garbage, supprime doublons."""
    if not entries:
        return entries

    # Étape 1 : Fusionner les résultats splités
    merged = []
    i = 0
    while i < len(entries):
        e = entries[i]
        r = (e.get("resultat") or "").strip()
        s = (e.get("societe") or "").strip()

        # Fragment "Label Non-"
        if r in ("Label Non-", "Label non-", "Prelabel Non-", "Prelabel non-", "label non-"):
            # Chercher le "Accordé" dans les entrées suivantes
            if i + 1 < len(entries):
                next_e = entries[i + 1]
                next_r = (next_e.get("resultat") or "").strip()
                next_soc = (next_e.get("societe") or "").strip()
                next_fond = (next_e.get("fondateurs") or "").strip()
                
                if next_r in ("Accordé", "Accorde") and not next_soc and not next_fond:
                    # Cas A : "Accordé" seul → fusionner et sauter
                    e = e.copy()
                    e["resultat"] = fragments.get(r, "label non accorde")
                    merged.append(e)
                    i += 2
                    continue
                elif next_r in ("Accordé", "Accorde") and next_soc:
                    # Cas B : "Accordé" + société → le résultat appartient à l'entrée précédente
                    e = e.copy()
                    e["resultat"] = fragments.get(r, "label non accorde")
                    merged.append(e)
                    # Réparer l'entrée suivante
                    entries[i + 1] = {
                        "societe": next_soc,
                        "fondateurs": next_fond,
                        "secteur": next_e.get("secteur", ""),
                        "resultat": ""
                    }
                    i += 1
                    continue
            
            # Pas de "Accordé" trouvé → compléter le fragment
            e = e.copy()
            e["resultat"] = fragments.get(r, "label non accorde")
            merged.append(e)
            i += 1
            continue

        # "Accordé" seul sans société → artefact, sauter
        if r in ("Accordé", "Accorde") and not s:
            i += 1
            continue

        merged.append(e)
        i += 1

    # Étape 2 : Fusionner les entrées avec même société (split sur 2 pages)
    deduped = []
    seen = {}
    for e in merged:
        s = (e.get("societe") or "").strip()
        if not s:
            continue
        s_key = norm(s)
        if s_key in seen:
            existing = seen[s_key]
            # Fusionner les champs manquants
            if e.get("fondateurs") and not existing.get("fondateurs"):
                existing["fondateurs"] = e["fondateurs"]
            if e.get("secteur") and not existing.get("secteur"):
                existing["secteur"] = e["secteur"]
            if e.get("resultat") and not existing.get("resultat"):
                existing["resultat"] = e["resultat"]
        else:
            seen[s_key] = e.copy()
            deduped.append(e)

    # Étape 3 : Filtrer les entrées garbage
    result = []
    for e in deduped:
        s = (e.get("societe") or "").strip()
        r = (e.get("resultat") or "").strip()

        # Filtrer les headers PDF
        if "compte-rendu" in norm(s) or "session" in norm(s) and "compte" in norm(s):
            continue
        if "startup act" in norm(s) and "session" in norm(s):
            continue

        # Filtrer les séparateurs de section
        if norm(s).startswith("societe secteur") or norm(s).startswith("société secteur"):
            continue

        # Filtrer les entrées sans société
        if not s or len(s) < 2:
            continue

        # Filtrer les résultats qui sont juste des headers
        if norm(r) in ("decision commentaires", "societe secteur"):
            continue

        # Filtrer les résultats de retrait
        if "retrait" in norm(r):
            continue

        # Filtrer les résultats qui sont des mois/dates (section Passage PL→L)
        mois = ["janvier", "fevrier", "mars", "avril", "mai", "juin",
                 "juillet", "aout", "septembre", "octobre", "novembre", "decembre"]
        if any(m in norm(r) for m in mois) and len(r) < 20:
            continue
        if any(m in norm(s) for m in mois) and len(s) < 30 and not e.get("fondateurs"):
            continue

        result.append(e)

    return result


def parse_pdf_rowlevel(path):
    """Parse un PDF et retourne la liste des entrées."""
    doc = fitz.open(path)
    entries = []

    # Layout persistant : réutilisé sur les pages 2+ (même table continuée)
    cached_header_y = None
    cached_col_positions = None
    cached_vote_start_x = None
    cached_boundaries = None

    for page_idx, page in enumerate(doc):
        all_lines = collect_lines(page)
        header_y, col_positions, sub_header_y, vote_start_x = detect_layout(all_lines)

        # Si la page a un header, mettre à jour le cache
        if header_y is not None and col_positions and "societe" in col_positions:
            cached_header_y = header_y
            cached_col_positions = col_positions
            cached_vote_start_x = vote_start_x
            page_rect = page.rect
            page_width = page_rect.width if page_rect else 800
            cached_boundaries = build_smart_boundaries(col_positions, vote_start_x, page_width)

        # Si pas de header mais on a un layout en cache → l'utiliser
        if cached_boundaries is None:
            # Tenter de détecter le layout depuis les données elles-mêmes
            # Chercher une ligne avec "Société" ou "Secteur" dans les 20 premières lignes
            potential_header_y = None
            potential_col_positions = {}
            for y in sorted(all_lines)[:20]:
                spans = all_lines[y]
                text_line = " ".join(t for _, _, t in spans)
                nl = norm(text_line)
                if "societe" in nl and ("fondateurs" in nl or "secteur" in nl):
                    potential_header_y = y
                    for x0, x1, t in spans:
                        nt = norm(t)
                        cx = (x0 + x1) / 2
                        if nt in ("societe", "société"):
                            potential_col_positions["societe"] = cx
                        elif nt in ("fondateurs", "fondateur"):
                            potential_col_positions["fondateurs"] = cx
                        elif nt == "secteur":
                            potential_col_positions["secteur"] = cx
                        elif nt in ("label/prelabel", "label prelabel", "label/pre label"):
                            potential_col_positions["label_type"] = cx
                        elif nt in ("resultat", "résultat"):
                            potential_col_positions["resultat"] = cx
                        elif nt == "commentaires":
                            potential_col_positions["commentaires"] = cx
                    break
            
            if potential_header_y is not None and "societe" in potential_col_positions:
                cached_header_y = potential_header_y
                cached_col_positions = potential_col_positions
                # Chercher vote_start_x dans les lignes suivantes
                for y in sorted(all_lines):
                    if y <= potential_header_y:
                        continue
                    spans = all_lines[y]
                    text_line = " ".join(t for _, _, t in spans)
                    nl = norm(text_line)
                    if "recevabilite" in nl or "pitching" in nl:
                        if spans:
                            cached_vote_start_x = spans[0][0]
                        break
                page_rect = page.rect
                page_width = page_rect.width if page_rect else 800
                cached_boundaries = build_smart_boundaries(cached_col_positions, cached_vote_start_x, page_width)
            else:
                # Fallback : boundaries par défaut selon la largeur de page
                page_rect = page.rect
                page_width = page_rect.width if page_rect else 800
                cached_boundaries = {
                    "societe": (0, page_width * 0.25),
                    "fondateurs": (page_width * 0.25, page_width * 0.5),
                    "secteur": (page_width * 0.5, page_width * 0.7),
                    "resultat": (page_width * 0.7, page_width),
                }
                cached_header_y = 0
                cached_col_positions = {}
                cached_vote_start_x = None

        # Déterminer le y de départ :
        # - Page 1 : utiliser header_y pour sauter l'en-tête
        # - Pages 2+ : utiliser cached_header_y pour sauter l'en-tête répété
        #   si aucun header n'est détecté sur cette page, utiliser 0
        if page_idx == 0 and header_y is not None:
            start_y = header_y
        elif header_y is not None:
            start_y = header_y
        else:
            start_y = 0

        current_entry = None
        in_main_section = True
        for y in sorted(all_lines):
            if y <= start_y:
                continue

            spans = all_lines[y]
            text_line = " ".join(t for _, _, t in spans)

            # Détecter les sections secondaires (Passage PL→L, Retraits)
            nl = norm(text_line)
            if in_main_section and (
                "prelabels aux labels" in nl or
                "passage de prelabels" in nl or
                "passage de" in nl and "labels" in nl or
                (len(spans) <= 4 and "retrait" in nl and "label" in nl)
            ):
                if current_entry and current_entry.get("societe"):
                    entries.append(current_entry)
                    current_entry = None
                in_main_section = False
                continue

            if is_noise_row(spans, text_line):
                if current_entry and current_entry.get("societe"):
                    entries.append(current_entry)
                    current_entry = None
                continue

            assigned = assign_by_boundaries(spans, cached_boundaries)

            societe = " ".join(assigned.get("societe", [])).strip()
            fondateurs = " ".join(assigned.get("fondateurs", [])).strip()
            secteur = clean_secteur(" ".join(assigned.get("secteur", [])).strip())
            resultat = extract_final_result(
                " ".join(assigned.get("resultat", []) or
                         assigned.get("label_type", [])).strip()
            )

            # Filtrer les entrées de retrait
            if "retrait" in norm(resultat):
                if current_entry and current_entry.get("societe"):
                    entries.append(current_entry)
                    current_entry = None
                continue

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

    doc.close()
    return postprocess_entries(entries)


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
