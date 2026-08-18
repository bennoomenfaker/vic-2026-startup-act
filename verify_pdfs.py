#!/usr/bin/env python3
"""
Vérification des données extraites des 85 sessions PDF.
Compare les données des JSON avec le texte réel extrait des PDF.
"""
import json
import os
import re
import subprocess
from collections import defaultdict

# Chemins
JSON_DIR = "public/data/session-pdfs-json"
PDF_DIR = "public/data/session-pdfs"

# Valeurs corrigées attendues (depuis AGENTS.md)
EXPECTED = {
    "labels": 1311,
    "prelabels": 623,
    "retraits": 140,
    "candidatures": 2958,
    "taux_moyen_pct": 44.3,
}

def load_all_sessions():
    """Charge tous les JSON de sessions."""
    sessions = {}
    for fname in sorted(os.listdir(JSON_DIR)):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(JSON_DIR, fname)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        sessions[fname] = data
    return sessions

def extract_pdf_text(pdf_path):
    """Extrait le texte d'un PDF avec pdftotext."""
    try:
        result = subprocess.run(
            ["pdftotext", pdf_path, "-"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        return result.stdout
    except Exception as e:
        return ""

def parse_pdf_results(text):
    """Parse le texte PDF pour extraire les résultats (labels, prelabels, retraits)."""
    text_lower = text.lower()
    
    # Compter les résultats dans le texte PDF
    labels = 0
    prelabels = 0
    retraits = 0
    candidatures = 0
    
    # Patterns pour les résultats
    label_patterns = [
        r'label\s+accord[eé]',
        r'label\s+accordé\s+dès',
        r'label\s+accordé\s+après',
        r'label\s+accordé\s+au',
    ]
    
    prelabel_patterns = [
        r'prélabel\s+accord[eé]',
        r'prélabel\s+accordé\s+dès',
        r'prélabel\s+accordé\s+après',
    ]
    
    refuse_patterns = [
        r'label\s+non\s*accord[eé]',
        r'prélabel\s+non\s*accord[eé]',
        r'prélabel\s+non\s+accordé',
    ]
    
    retrait_patterns = [
        r'retrait',
        r'ajourné',
        r'dossier\s+irrecevable',
    ]
    
    # Compter les résultats
    for pattern in label_patterns:
        labels += len(re.findall(pattern, text_lower))
    
    for pattern in prelabel_patterns:
        prelabels += len(re.findall(pattern, text_lower))
    
    for pattern in refuse_patterns:
        # Ces résultats ne sont pas des labels/prelabels accordés
        pass
    
    for pattern in retrait_patterns:
        retraits += len(re.findall(pattern, text_lower))
    
    # Compter les lignes de résultats (chaque ligne = 1 candidature)
    # Chercher les patterns "Label accordé", "Label non accordé", etc.
    result_lines = re.findall(r'(label\s+(?:non\s*)?accord[eé]|prélabel\s+(?:non\s*)?accord[eé]|retrait|ajourné|irrecevable)', text_lower)
    candidatures = len(result_lines)
    
    return candidatures, labels, prelabels, retraits

def count_json_results(sessions):
    """Compte les résultats depuis les JSON."""
    total_labels = 0
    total_prelabels = 0
    total_retraits = 0
    total_candidatures = 0
    
    for fname, data in sessions.items():
        session_data = data.get("session_data", {})
        total_labels += session_data.get("labels", 0)
        total_prelabels += session_data.get("preLabels", 0)
        total_retraits += session_data.get("retraits", 0)
        total_candidatures += session_data.get("candidatures", 0)
    
    return total_labels, total_prelabels, total_retraits, total_candidatures

def main():
    print("=" * 80)
    print("VÉRIFICATION DES DONNÉES EXTRAITES - 85 SESSIONS STARTUP ACT")
    print("Comparaison JSON vs PDF réel")
    print("=" * 80)
    
    # 1. Charger les sessions JSON
    sessions = load_all_sessions()
    print(f"\n✅ {len(sessions)} fichiers JSON chargés depuis {JSON_DIR}")
    
    # 2. Compter les résultats JSON
    json_labels, json_prelabels, json_retraits, json_candidatures = count_json_results(sessions)
    
    print(f"\n📊 Résultats depuis les JSON:")
    print(f"   Labels:      {json_labels}")
    print(f"   Pré-Labels:  {json_prelabels}")
    print(f"   Candidatures: {json_candidatures}")
    print(f"   Retraits:    {json_retraits}")
    
    # 3. Vérifier chaque PDF
    print(f"\n{'='*80}")
    print("VÉRIFICATION DÉTAILLÉE PAR PDF")
    print(f"{'='*80}")
    
    discrepancies = []
    pdf_labels_total = 0
    pdf_prelabels_total = 0
    pdf_retraits_total = 0
    pdf_candidatures_total = 0
    
    for fname, data in sorted(sessions.items()):
        pdf_name = data.get("pdf", "")
        if not pdf_name:
            continue
        
        pdf_path = os.path.join(PDF_DIR, pdf_name)
        if not os.path.exists(pdf_path):
            print(f"  ⚠️  PDF manquant: {pdf_name}")
            continue
        
        # Extraire le texte du PDF
        pdf_text = extract_pdf_text(pdf_path)
        
        # Parser les résultats du PDF
        pdf_candidatures, pdf_labels, pdf_prelabels, pdf_retraits = parse_pdf_results(pdf_text)
        
        # Résultats du JSON
        session_data = data.get("session_data", {})
        json_c = session_data.get("candidatures", 0)
        json_l = session_data.get("labels", 0)
        json_pl = session_data.get("preLabels", 0)
        json_r = session_data.get("retraits", 0)
        
        # Accumuler les totaux
        pdf_labels_total += pdf_labels
        pdf_prelabels_total += pdf_prelabels
        pdf_retraits_total += pdf_retraits
        pdf_candidatures_total += pdf_candidatures
        
        # Vérifier les écarts
        session_id = data.get("session", fname.replace("session_", "").replace(".json", ""))
        
        if pdf_labels != json_l or pdf_prelabels != json_pl or pdf_candidatures != json_c:
            discrepancies.append({
                "session": session_id,
                "pdf": pdf_name,
                "json_labels": json_l,
                "pdf_labels": pdf_labels,
                "json_prelabels": json_pl,
                "pdf_prelabels": pdf_prelabels,
                "json_candidatures": json_c,
                "pdf_candidatures": pdf_candidatures,
            })
            print(f"\n  ⚠️  Session {session_id} ({pdf_name}):")
            print(f"      JSON:  Labels={json_l}, Pré-Labels={json_pl}, Candidatures={json_c}")
            print(f"      PDF:   Labels={pdf_labels}, Pré-Labels={pdf_prelabels}, Candidatures={pdf_candidatures}")
    
    # 4. Résumé
    print(f"\n{'='*80}")
    print("RÉSUMÉ COMPARATIF")
    print(f"{'='*80}")
    
    print(f"\n  Source JSON:")
    print(f"    Labels:      {json_labels}")
    print(f"    Pré-Labels:  {json_prelabels}")
    print(f"    Candidatures: {json_candidatures}")
    
    print(f"\n  Source PDF (extraction):")
    print(f"    Labels:      {pdf_labels_total}")
    print(f"    Pré-Labels:  {pdf_prelabels_total}")
    print(f"    Candidatures: {pdf_candidatures_total}")
    
    print(f"\n  Valeurs attendues (corrigées):")
    print(f"    Labels:      {EXPECTED['labels']}")
    print(f"    Pré-Labels:  {EXPECTED['prelabels']}")
    print(f"    Candidatures: {EXPECTED['candidatures']}")
    
    # 5. Écarts
    print(f"\n{'='*80}")
    print("ÉCARTS DÉTECTÉS")
    print(f"{'='*80}")
    
    if discrepancies:
        print(f"\n  ⚠️  {len(discrepancies)} sessions avec écarts:")
        for d in discrepancies:
            print(f"\n    Session {d['session']}:")
            print(f"      Labels: JSON={d['json_labels']}, PDF={d['pdf_labels']}")
            print(f"      Pré-Labels: JSON={d['json_prelabels']}, PDF={d['pdf_prelabels']}")
            print(f"      Candidatures: JSON={d['json_candidatures']}, PDF={d['pdf_candidatures']}")
    else:
        print(f"\n  ✅ Aucun écart détecté entre JSON et PDF")
    
    # 6. Taux moyen
    taux_moyen = (json_labels / json_candidatures * 100) if json_candidatures > 0 else 0
    print(f"\n{'='*80}")
    print("TAUX MOYEN")
    print(f"{'='*80}")
    print(f"  Calculé (JSON):    {taux_moyen:.1f}% ({json_labels}/{json_candidatures})")
    print(f"  Attendu:           {EXPECTED['taux_moyen_pct']}%")
    
    print(f"\n{'='*80}")
    print("FIN DE LA VÉRIFICATION")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
