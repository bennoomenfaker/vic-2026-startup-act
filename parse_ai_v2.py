#!/usr/bin/env python3
"""
Parser AI v2 — Extraction structurée des PDFs Startup Act.
Corrige le bug colonne TYPE (Label/Prélabel) vs DÉCISION (Résultat).
"""

import re
import os
import json
import sys

# Mois français
MOIS = {"janvier":1, "fevrier":2, "mars":3, "avril":4, "mai":5, "juin":6,
        "juillet":7, "aout":8, "aûout":8, "septembre":9, "octobre":10,
        "novembre":11, "decembre":12}

# Mots-bruit à ignorer
NOISE_WORDS = {
    "conflit", "d'intérêt", "d'intêrét", "déclaré", "a déclaré",
    "m.", "mr", "mme", "la société", "le startuppeur", "les membres",
    "conformément", "bénéficiaires", "article", "loi", "n°",
    "compte-rendu", "session", "startup act", "décision", "commentaires",
    "société secteur", "societe secteur", "1er tour", "2ème tour",
    "recevabilité", "pitching", "conflit", "label", "prélabel",
    "prelabel", "accordé", "accordée", "non-accordé", "non accordé",
    "n.a", "retrait", "passage", "obtention"
}

# Secteurs connus
KNOWN_SECTORS = {
    "edtech", "fintech", "iot", "ai", "healthtech", "health tech",
    "agritech", "foodtech", "food tech", "ecommerce", "e-commerce",
    "logiciel", "it", "web", "mobile", "saas", "platform",
    "energy", "energie", "environment", "cleantech", "hrtech",
    "hr tech", "legaltech", "legal tech", "proptech", "proptech",
    "insurtech", "traveltech", "retailtech", "logistics",
    "biotech", "medtech", "deeptech", "spacetech", "gametech",
    "adtech", "ad tech", "martech", "regtech", "govtech",
    "autre contenu créatif", "plateforme sociale", "business software",
    "business software and services", "business software & services",
    "services", "consulting", "training", "education",
    "manufacturing", "industry", "retail", "wholesale",
    "telecom", "media", "entertainment", "culture",
    "finance", "banking", "insurance", "investment",
    "health", "medical", "pharmaceutical", "biomedical",
    "agriculture", "farming", "food", "beverage",
    "construction", "real estate", "property",
    "transport", "logistics", "supply chain",
    "tourism", "hospitality", "hotel", "restaurant",
    "fashion", "beauty", "cosmetics",
    "security", "cybersecurity", "privacy",
    "ai & deep learning", "machine learning", "data",
    "blockchain", "crypto", "web3",
    "iot & embedded", "embedded", "hardware",
    "software", "cloud", "devops",
    "marketplace", "platform", "social",
    "b2b", "b2c", "b2g",
}

# Patterns de résultat
RESULT_PATTERNS = [
    # Format exact
    (r"label\s+accordé", "label accorde"),
    (r"label\s+accordée", "label accorde"),
    (r"label\s+non[\s-]+accordé", "label non accorde"),
    (r"label\s+non[\s-]+accordée", "label non accorde"),
    (r"prélabel\s+accordé", "prelabel accorde"),
    (r"prélabel\s+accordée", "prelabel accorde"),
    (r"prélabel\s+non[\s-]+accordé", "prelabel non accorde"),
    (r"prélabel\s+non[\s-]+accordée", "prelabel non accorde"),
    (r"prelabel\s+accordé", "prelabel accorde"),
    (r"prelabel\s+accordée", "prelabel accorde"),
    (r"prelabel\s+non[\s-]+accordé", "prelabel non accorde"),
    (r"prelabel\s+non[\s-]+accordée", "prelabel non accorde"),
    # Variants
    (r"label\s+accordé\s+au", "label accorde"),
    (r"label\s+accordé\s+dès", "label accorde"),
    (r"label\s+accordé\s+après", "label accorde"),
    (r"prélabel\s+accordé\s+au", "prelabel accorde"),
    (r"prélabel\s+accordé\s+dès", "prelabel accorde"),
    (r"prélabel\s+accordé\s+après", "prelabel accorde"),
    # Retrait
    (r"retrait\s+du\s+label", "retrait du label"),
    (r"retrait\s+du\s+prélabel", "retrait du prelabel"),
]


def detect_format(lines):
    """Détecte le format du PDF (A ou B)."""
    header_text = " ".join(lines[:20]).lower()
    has_type_column = "label/prélabel" in header_text or "label/prelabel" in header_text
    return "B" if has_type_column else "A"


def is_noise_line(line):
    """Vérifie si une ligne est du bruit."""
    nl = line.lower().strip()
    
    # Lignes vides
    if len(nl) < 2:
        return True
    
    # Conflits d'intérêt
    if "conflit" in nl and ("déclaré" in nl or "declare" in nl):
        return True
    if "m." in nl and ("déclaré" in nl or "conflit" in nl):
        return True
    
    # Headers
    if nl.startswith("1er tour") or nl.startswith("recevabilité"):
        return True
    if nl.startswith("société") and "secteur" in nl:
        return True
    if nl.startswith("startup act"):
        return True
    
    # Texte légal
    if "conformément" in nl or "bénéficiaires" in nl:
        return True
    if "article" in nl and "loi" in nl:
        return True
    
    # N.A
    if nl == "n.a" or nl == "n.a.":
        return True
    
    return False


def parse_result(text):
    """Extrait le résultat normalisé."""
    nl = text.lower().strip()
    for pattern, result in RESULT_PATTERNS:
        if re.search(pattern, nl):
            return result
    return ""


def parse_sector(text):
    """Extrait et nettoie le secteur."""
    sector = text.strip()
    # Retirer les mois
    for m in MOIS:
        sector = re.sub(r'\b' + m + r'\b', '', sector, flags=re.IGNORECASE)
    # Retirer les mots-bruit
    words = sector.split()
    clean = [w for w in words if w.lower() not in NOISE_WORDS]
    return " ".join(clean).strip()


def is_sector(text):
    """Vérifie si le texte est un secteur."""
    nl = text.lower().strip()
    # Secteur connu
    if nl in KNOWN_SECTORS:
        return True
    # Contient un mot de secteur
    for s in KNOWN_SECTORS:
        if s in nl:
            return True
    return False


def is_founder_name(text):
    """Vérifie si le texte est un nom de fondateur."""
    text = text.strip()
    if len(text) < 3:
        return False
    # Pas un chiffre
    if text.isdigit():
        return False
    # Pas un résultat
    if parse_result(text):
        return False
    # Pas un secteur
    if is_sector(text):
        return False
    # Contient au moins une majuscule
    if not any(c.isupper() for c in text):
        return False
    # Longueur raisonnable
    if len(text) > 100:
        return False
    return True


def parse_session_from_text(text, session_key):
    """Parse une session complète depuis le texte brut."""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    if len(lines) < 10:
        return {"session": session_key, "entries": [], "error": "Texte trop court"}
    
    # Détecter le format
    fmt = detect_format(lines)
    
    # Trouver le début des données (après les headers)
    start_idx = 0
    for i, line in enumerate(lines):
        nl = line.lower()
        if "résultat" in nl or "resultat" in nl:
            start_idx = i + 1
            break
        if "label accordé" in nl or "label accorde" in nl:
            start_idx = i
            break
    
    # Parser les entrées
    entries = []
    current_entry = None
    i = start_idx
    
    while i < len(lines):
        line = lines[i]
        
        # Ignorer le bruit
        if is_noise_line(line):
            if current_entry and current_entry.get("societe"):
                entries.append(current_entry)
                current_entry = None
            i += 1
            continue
        
        # Vérifier si c'est un résultat
        result = parse_result(line)
        if result:
            if current_entry:
                current_entry["resultat"] = result
                # La ligne suivante est souvent un commentaire
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if not parse_result(next_line) and not is_sector(next_line):
                        if len(next_line) > 5 and not is_noise_line(next_line):
                            current_entry["commentaires"] = next_line
                            i += 1
            i += 1
            continue
        
        # Vérifier si c'est un secteur
        if is_sector(line) and current_entry and not current_entry.get("secteur"):
            current_entry["secteur"] = parse_sector(line)
            i += 1
            continue
        
        # Vérifier si c'est un nom de fondateur
        if is_founder_name(line) and current_entry:
            if current_entry.get("fondateurs"):
                current_entry["fondateurs"] += ", " + line
            else:
                current_entry["fondateurs"] = line
            i += 1
            continue
        
        # Vérifier si c'est le début d'une nouvelle société
        # Pattern: ligne avec peu de texte, pas un résultat, pas un secteur
        if (len(line) > 2 and len(line) < 100 and 
            not result and not is_sector(line) and 
            not line.replace('.','').replace('-','').isdigit()):
            
            # Vérifier si la ligne suivante est un nom de fondateur
            if i + 1 < len(lines) and is_founder_name(lines[i + 1]):
                # Nouvelle entrée
                if current_entry and current_entry.get("societe"):
                    entries.append(current_entry)
                current_entry = {
                    "societe": line.strip(),
                    "fondateurs": "",
                    "secteur": "",
                    "resultat": "",
                    "commentaires": ""
                }
                i += 1
                continue
        
        i += 1
    
    # Dernière entrée
    if current_entry and current_entry.get("societe"):
        entries.append(current_entry)
    
    # Normaliser les résultats
    for e in entries:
        r = e.get("resultat", "")
        # "Label Accordé" → "label accorde"
        if "label" in r.lower() and "accordé" in r.lower() and "non" not in r.lower():
            e["resultat"] = "label accorde"
        elif "label" in r.lower() and "non" in r.lower():
            e["resultat"] = "label non accorde"
        elif "prélabel" in r.lower() and "accordé" in r.lower() and "non" not in r.lower():
            e["resultat"] = "prelabel accorde"
        elif "prélabel" in r.lower() and "non" in r.lower():
            e["resultat"] = "prelabel non accorde"
        elif "prelabel" in r.lower() and "accordé" in r.lower() and "non" not in r.lower():
            e["resultat"] = "prelabel accorde"
        elif "prelabel" in r.lower() and "non" in r.lower():
            e["resultat"] = "prelabel non accorde"
    
    return {
        "session": session_key,
        "format": fmt,
        "entries": entries
    }


def main():
    """Test sur un ou plusieurs PDFs."""
    txt_dir = "/tmp/pdf_texts"
    
    if len(sys.argv) > 1:
        # Parser un fichier spécifique
        txt_path = sys.argv[1]
        session_key = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(txt_path).replace('.txt', '')
    else:
        # Parser tous les fichiers
        files = sorted([f for f in os.listdir(txt_dir) if f.endswith('.txt') and f != 'summary.json'])
        
        for f in files:
            txt_path = os.path.join(txt_dir, f)
            parts = f.replace('.txt', '').split('_')
            if len(parts) == 3:
                session_key = f"{parts[2]}/{parts[1]}"
            else:
                session_key = f.replace('.txt', '')
            
            with open(txt_path, 'r', encoding='utf-8') as fh:
                text = fh.read()
            
            result = parse_session_from_text(text, session_key)
            
            # Charger l'officiel
            with open('/home/himawari/Desktop/startup-act/public/data/sessions.json') as fh:
                sessions = {s['session']: s for s in json.load(fh)}
            
            official = sessions.get(session_key, {})
            exp_labels = official.get('labels', 0)
            exp_prelabels = official.get('preLabels', 0)
            exp_cand = official.get('candidatures', 0)
            
            # Compter
            labels = sum(1 for e in result['entries'] if e.get('resultat') == 'label accorde')
            prelabels = sum(1 for e in result['entries'] if e.get('resultat') == 'prelabel accorde')
            
            # Statut
            ld = abs(labels - exp_labels)
            pd = abs(prelabels - exp_prelabels)
            cd = abs(len(result['entries']) - exp_cand)
            
            if ld <= 1 and pd <= 1:
                status = "✅"
            else:
                status = "❌"
            
            fmt = result.get('format', '?')
            print(f"{status} {session_key}: entries={len(result['entries'])}/{exp_cand} labels={labels}/{exp_labels} prelabels={prelabels}/{exp_prelabels} fmt={fmt}")
        
        return
    
    # Parser un fichier
    with open(txt_path, 'r', encoding='utf-8') as fh:
        text = fh.read()
    
    result = parse_session_from_text(text, session_key)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
