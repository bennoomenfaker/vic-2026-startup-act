#!/usr/bin/env python3
"""
Vérification v2 : extraction par colonne du PDF (Résultat uniquement).
Compare les données JSON avec le texte réel extrait des PDF.
"""
import json
import os
import re
import subprocess
from collections import defaultdict

JSON_DIR = "public/data/session-pdfs-json"
PDF_DIR = "public/data/session-pdfs"

EXPECTED = {
    "labels": 1311,
    "prelabels": 623,
    "retraits": 140,
    "candidatures": 2958,
    "taux_moyen_pct": 44.3,
}

def load_all_sessions():
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
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", pdf_path, "-"],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        return result.stdout
    except:
        return ""

def count_results_from_text(text):
    """
    Count label/prelabel/refus occurrences by analyzing the full text.
    Strategy: find all lines that contain result patterns in the Résultat column area.
    The Résultat column is typically right-aligned near the end of lines.
    We look for patterns like "Label Accordé", "Label Non Accordé", "Prélabel Accordé", etc.
    """
    lines = text.split('\n')
    
    labels = 0
    prelabels = 0
    refus = 0
    irrecevables = 0
    candidatures = 0
    
    # Track which company blocks we've seen to avoid double counting
    seen_companies = set()
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        # Look for result patterns in this line
        # The Résultat column text appears near the right side of the line
        # Split by multiple spaces to find the rightmost content
        parts = re.split(r'\s{2,}', line_stripped)
        
        for part in parts:
            part_lower = part.lower().strip()
            
            # Match label accordé (but not "Label Non Accordé")
            if re.match(r'^label\s+(?:accordé|accordé\s+au\s+\d)', part_lower) and 'non' not in part_lower:
                labels += 1
            # Match prélabel accordé
            elif re.match(r'^prélabel\s+(?:accordé|accordé\s+au\s+\d)', part_lower) and 'non' not in part_lower:
                prelabels += 1
            # Match label non accordé
            elif re.match(r'^label\s+non\s*accordé', part_lower):
                refus += 1
            # Match prélabel non accordé
            elif re.match(r'^prélabel\s+non\s*accordé', part_lower):
                refus += 1
            # Match irrecevable
            elif 'irrecevable' in part_lower:
                irrecevables += 1
    
    # Alternative: count from the Résultat column specifically
    # Find the Résultat column position
    resultat_lines = []
    for i, line in enumerate(lines):
        if 'Résultat' in line or 'Resultat' in line:
            # Found the header, subsequent lines have results
            break
    
    return labels, prelabels, refus, irrecevables

def count_results_from_entrees(sessions):
    """Count results from the entrees array in JSON."""
    total_labels = 0
    total_prelabels = 0
    total_retraits = 0
    total_candidatures = 0
    
    for fname, data in sessions.items():
        entrees = data.get("entrees", [])
        session_data = data.get("session_data", {})
        
        # Use session_data counts (these are the authoritative counts)
        total_labels += session_data.get("labels", 0)
        total_prelabels += session_data.get("preLabels", 0)
        total_retraits += session_data.get("retraits", 0)
        total_candidatures += session_data.get("candidatures", 0)
    
    return total_labels, total_prelabels, total_retraits, total_candidatures

def main():
    print("=" * 80)
    print("VÉRIFICATION v2 — EXTRACTION PAR COLONNE RÉSULTAT")
    print("=" * 80)
    
    sessions = load_all_sessions()
    print(f"✅ {len(sessions)} fichiers JSON chargés")
    
    # JSON totals
    json_labels, json_prelabels, json_retraits, json_candidatures = count_results_from_entrees(sessions)
    json_taux = (json_labels / json_candidatures * 100) if json_candidatures > 0 else 0
    
    print(f"\n📊 Totaux JSON: Labels={json_labels}, Pré-Labels={json_prelabels}, Candidatures={json_candidatures}, Retraits={json_retraits}, Taux={json_taux:.1f}%")
    
    # Analyze each PDF
    discrepancies = []
    pdf_total_labels = 0
    pdf_total_prelabels = 0
    pdf_total_refus = 0
    pdf_total_irrecevables = 0
    
    for fname, data in sorted(sessions.items()):
        pdf_name = data.get("pdf", "")
        if not pdf_name:
            continue
        
        pdf_path = os.path.join(PDF_DIR, pdf_name)
        if not os.path.exists(pdf_path):
            continue
        
        pdf_text = extract_pdf_text(pdf_path)
        
        # Count from PDF text
        pdf_labels, pdf_prelabels, pdf_refus, pdf_irrecevables = count_results_from_text(pdf_text)
        
        pdf_total_labels += pdf_labels
        pdf_total_prelabels += pdf_prelabels
        pdf_total_refus += pdf_refus
        pdf_total_irrecevables += pdf_irrecevables
        
        session_id = data.get("session", "")
        session_data = data.get("session_data", {})
        json_l = session_data.get("labels", 0)
        json_pl = session_data.get("preLabels", 0)
        
        # Check for discrepancies
        if pdf_labels != json_l or pdf_prelabels != json_pl:
            discrepancies.append({
                "session": session_id,
                "pdf": pdf_name,
                "json_labels": json_l,
                "pdf_labels": pdf_labels,
                "json_prelabels": json_pl,
                "pdf_prelabels": pdf_prelabels,
            })
    
    print(f"\n📊 Totaux PDF (extraction colonne Résultat):")
    print(f"   Labels:      {pdf_total_labels}")
    print(f"   Pré-Labels:  {pdf_total_prelabels}")
    print(f"   Refus:       {pdf_total_refus}")
    print(f"   Irrecevables: {pdf_total_irrecevables}")
    
    print(f"\n📊 Valeurs attendues:")
    print(f"   Labels:      {EXPECTED['labels']}")
    print(f"   Pré-Labels:  {EXPECTED['prelabels']}")
    
    # Compare
    print(f"\n{'='*80}")
    print("COMPARAISON JSON vs PDF")
    print(f"{'='*80}")
    
    if json_labels == EXPECTED["labels"]:
        print(f"  ✅ Labels JSON:      {json_labels} = {EXPECTED['labels']} (CORRECT)")
    else:
        print(f"  ❌ Labels JSON:      {json_labels} ≠ {EXPECTED['labels']}")
    
    if json_prelabels == EXPECTED["prelabels"]:
        print(f"  ✅ Pré-Labels JSON:  {json_prelabels} = {EXPECTED['prelabels']} (CORRECT)")
    else:
        print(f"  ❌ Pré-Labels JSON:  {json_prelabels} ≠ {EXPECTED['prelabels']}")
    
    if json_candidatures == EXPECTED["candidatures"]:
        print(f"  ✅ Candidatures:     {json_candidatures} = {EXPECTED['candidatures']} (CORRECT)")
    else:
        print(f"  ❌ Candidatures:     {json_candidatures} ≠ {EXPECTED['candidatures']}")
    
    if abs(json_taux - EXPECTED["taux_moyen_pct"]) < 0.1:
        print(f"  ✅ Taux moyen:       {json_taux:.1f}% ≈ {EXPECTED['taux_moyen_pct']}% (CORRECT)")
    else:
        print(f"  ❌ Taux moyen:       {json_taux:.1f}% ≠ {EXPECTED['taux_moyen_pct']}%")
    
    # Discrepancies
    print(f"\n{'='*80}")
    print(f"ÉCARTS JSON vs PDF ({len(discrepancies)} sessions)")
    print(f"{'='*80}")
    
    if discrepancies:
        for d in discrepancies:
            print(f"\n  Session {d['session']}:")
            print(f"    JSON Labels={d['json_labels']}, PDF Labels={d['pdf_labels']}")
            print(f"    JSON PréLabels={d['json_prelabels']}, PDF PréLabels={d['pdf_prelabels']}")
    else:
        print(f"  ✅ Aucun écart")
    
    # Detailed session-by-session
    print(f"\n{'='*80}")
    print("DÉTAIL PAR SESSION")
    print(f"{'='*80}")
    print(f"{'Session':<12} {'Candid.':>8} {'Labels':>7} {'Pré-Lab':>8}")
    print("-" * 40)
    
    for fname, data in sorted(sessions.items()):
        session_data = data.get("session_data", {})
        session_id = data.get("session", "")
        c = session_data.get("candidatures", 0)
        l = session_data.get("labels", 0)
        pl = session_data.get("preLabels", 0)
        print(f"{session_id:<12} {c:>8} {l:>7} {pl:>8}")
    
    print("-" * 40)
    print(f"{'TOTAL':<12} {json_candidatures:>8} {json_labels:>7} {json_prelabels:>8}")
    
    print(f"\n{'='*80}")
    print("CONCLUSION")
    print(f"{'='*80}")
    print(f"  Labels:      {json_labels} {'✅' if json_labels == EXPECTED['labels'] else '❌'}")
    print(f"  Pré-Labels:  {json_prelabels} {'✅' if json_prelabels == EXPECTED['prelabels'] else '❌'}")
    print(f"  Candidatures: {json_candidatures} {'✅' if json_candidatures == EXPECTED['candidatures'] else '❌'}")
    print(f"  Taux moyen:  {json_taux:.1f}% {'✅' if abs(json_taux - EXPECTED['taux_moyen_pct']) < 0.1 else '❌'}")

if __name__ == "__main__":
    main()
