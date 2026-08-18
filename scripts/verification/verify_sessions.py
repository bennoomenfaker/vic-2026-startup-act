#!/usr/bin/env python3
"""
Vérification des données extraites des 85 sessions PDF.
Compare les données des JSON avec les valeurs corrigées attendues.
"""
import json
import os
import sys
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

def count_results(sessions):
    """Compte labels, prelabels, retraits, candidatures par session."""
    total_labels = 0
    total_prelabels = 0
    total_retraits = 0
    total_candidatures = 0
    total_conversions = 0
    
    session_details = []
    
    for fname, data in sorted(sessions.items()):
        session_id = data.get("session", fname.replace("session_", "").replace(".json", ""))
        nb_entrees = data.get("nb_entrees", 0)
        session_data = data.get("session_data", {})
        
        candidatures = session_data.get("candidatures", nb_entrees)
        labels = session_data.get("labels", 0)
        prelabels = session_data.get("preLabels", 0)
        retraits = session_data.get("retraits", 0)
        conversions = session_data.get("conversions", 0)
        
        # Vérifier aussi les entrées individuelles
        entrees = data.get("entrees", [])
        labels_from_entrees = sum(1 for e in entrees if "label" in e.get("resultat", "").lower() and "accorde" in e.get("resultat", "").lower() and "pre" not in e.get("resultat", "").lower())
        prelabels_from_entrees = sum(1 for e in entrees if "prelabel" in e.get("resultat", "").lower() or ("pre" in e.get("resultat", "").lower() and "label" in e.get("resultat", "").lower()))
        retraits_from_entrees = sum(1 for e in entrees if "retrait" in e.get("resultat", "").lower() or "ajourne" in e.get("resultat", "").lower())
        
        session_details.append({
            "session": session_id,
            "candidatures": candidatures,
            "labels": labels,
            "prelabels": prelabels,
            "retraits": retraits,
            "conversions": conversions,
            "labels_from_entrees": labels_from_entrees,
            "prelabels_from_entrees": prelabels_from_entrees,
        })
        
        total_labels += labels
        total_prelabels += prelabels
        total_retraits += retraits
        total_candidatures += candidatures
        total_conversions += conversions
    
    return total_labels, total_prelabels, total_retraits, total_candidatures, total_conversions, session_details

def check_pdf_files_exist(sessions):
    """Vérifie que chaque session a un PDF correspondant."""
    missing_pdfs = []
    for fname, data in sessions.items():
        pdf_name = data.get("pdf", "")
        if pdf_name:
            pdf_path = os.path.join(PDF_DIR, pdf_name)
            if not os.path.exists(pdf_path):
                missing_pdfs.append(pdf_name)
    return missing_pdfs

def main():
    print("=" * 70)
    print("VÉRIFICATION DES DONNÉES EXTRAITES - 85 SESSIONS STARTUP ACT")
    print("=" * 70)
    
    # 1. Charger les sessions
    sessions = load_all_sessions()
    print(f"\n✅ {len(sessions)} fichiers JSON chargés depuis {JSON_DIR}")
    
    # 2. Vérifier les PDFs
    missing_pdfs = check_pdf_files_exist(sessions)
    if missing_pdfs:
        print(f"\n⚠️  PDFs manquants : {missing_pdfs}")
    else:
        print(f"✅ Tous les PDFs existent dans {PDF_DIR}")
    
    # 3. Compter les résultats
    total_labels, total_prelabels, total_retraits, total_candidatures, total_conversions, session_details = count_results(sessions)
    
    # 4. Calculer le taux moyen
    taux_moyen = (total_labels / total_candidatures * 100) if total_candidatures > 0 else 0
    
    # 5. Afficher les résultats
    print(f"\n{'='*70}")
    print("RÉSULTATS AGRÉGÉS (depuis les JSON)")
    print(f"{'='*70}")
    print(f"  Labels       : {total_labels}")
    print(f"  Pré-Labels   : {total_prelabels}")
    print(f"  Candidatures : {total_candidatures}")
    print(f"  Retraits     : {total_retraits}")
    print(f"  Conversions  : {total_conversions}")
    print(f"  Taux moyen   : {taux_moyen:.1f}%")
    
    print(f"\n{'='*70}")
    print("VALEURS ATTENDUES (corrigées)")
    print(f"{'='*70}")
    print(f"  Labels       : {EXPECTED['labels']}")
    print(f"  Pré-Labels   : {EXPECTED['prelabels']}")
    print(f"  Candidatures : {EXPECTED['candidatures']}")
    print(f"  Retraits     : {EXPECTED['retraits']}")
    print(f"  Taux moyen   : {EXPECTED['taux_moyen_pct']}%")
    
    # 6. Comparer
    print(f"\n{'='*70}")
    print("COMPARAISON")
    print(f"{'='*70}")
    
    diffs = []
    if total_labels != EXPECTED["labels"]:
        diff = total_labels - EXPECTED["labels"]
        diffs.append(("Labels", total_labels, EXPECTED["labels"], diff))
        print(f"  ❌ Labels       : {total_labels} (attendu {EXPECTED['labels']}) → écart {diff:+d}")
    else:
        print(f"  ✅ Labels       : {total_labels} = {EXPECTED['labels']}")
    
    if total_prelabels != EXPECTED["prelabels"]:
        diff = total_prelabels - EXPECTED["prelabels"]
        diffs.append(("Pré-Labels", total_prelabels, EXPECTED["prelabels"], diff))
        print(f"  ❌ Pré-Labels   : {total_prelabels} (attendu {EXPECTED['prelabels']}) → écart {diff:+d}")
    else:
        print(f"  ✅ Pré-Labels   : {total_prelabels} = {EXPECTED['prelabels']}")
    
    if total_candidatures != EXPECTED["candidatures"]:
        diff = total_candidatures - EXPECTED["candidatures"]
        diffs.append(("Candidatures", total_candidatures, EXPECTED["candidatures"], diff))
        print(f"  ❌ Candidatures : {total_candidatures} (attendu {EXPECTED['candidatures']}) → écart {diff:+d}")
    else:
        print(f"  ✅ Candidatures : {total_candidatures} = {EXPECTED['candidatures']}")
    
    if total_retraits != EXPECTED["retraits"]:
        diff = total_retraits - EXPECTED["retraits"]
        diffs.append(("Retraits", total_retraits, EXPECTED["retraits"], diff))
        print(f"  ❌ Retraits     : {total_retraits} (attendu {EXPECTED['retraits']}) → écart {diff:+d}")
    else:
        print(f"  ✅ Retraits     : {total_retraits} = {EXPECTED['retraits']}")
    
    if abs(taux_moyen - EXPECTED["taux_moyen_pct"]) > 0.1:
        diffs.append(("Taux moyen", taux_moyen, EXPECTED["taux_moyen_pct"], taux_moyen - EXPECTED["taux_moyen_pct"]))
        print(f"  ❌ Taux moyen   : {taux_moyen:.1f}% (attendu {EXPECTED['taux_moyen_pct']}%) → écart {taux_moyen - EXPECTED['taux_moyen_pct']:+.1f}%")
    else:
        print(f"  ✅ Taux moyen   : {taux_moyen:.1f}% ≈ {EXPECTED['taux_moyen_pct']}%")
    
    # 7. Détail par session
    print(f"\n{'='*70}")
    print("DÉTAIL PAR SESSION")
    print(f"{'='*70}")
    print(f"{'Session':<12} {'Candid.':>8} {'Labels':>7} {'Pré-Lab':>8} {'Retraits':>9} {'Convers':>8}")
    print("-" * 60)
    
    for s in session_details:
        print(f"{s['session']:<12} {s['candidatures']:>8} {s['labels']:>7} {s['prelabels']:>8} {s['retraits']:>9} {s['conversions']:>8}")
    
    print("-" * 60)
    print(f"{'TOTAL':<12} {total_candidatures:>8} {total_labels:>7} {total_prelabels:>8} {total_retraits:>9} {total_conversions:>8}")
    
    # 8. Sessions avec écart potentiel
    if diffs:
        print(f"\n{'='*70}")
        print("⚠️  SESSIONS À VÉRIFIER MANUELLEMENT")
        print(f"{'='*70}")
        for name, current, expected, diff in diffs:
            print(f"  - {name}: écart de {diff:+d}")
    
    # 9. Vérification des résultats individuels
    print(f"\n{'='*70}")
    print("VÉRIFICATION DES RÉSULTATS INDIVIDUELS (entrees)")
    print(f"{'='*70}")
    
    for s in session_details:
        if s["labels"] != s["labels_from_entrees"] or s["prelabels"] != s["prelabels_from_entrees"]:
            print(f"  ⚠️  Session {s['session']}: session_data.labels={s['labels']}, entrees.labels={s['labels_from_entrees']}, session_data.prelabels={s['prelabels']}, entrees.prelabels={s['prelabels_from_entrees']}")
    
    print(f"\n{'='*70}")
    print("FIN DE LA VÉRIFICATION")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
