#!/usr/bin/env python3
"""
Verify individual JSON entries against PDF text.
Strategy: For each session, extract company names from PDF, 
compare with JSON entrees. Flag mismatches.
"""
import json
import os
import re
import subprocess

JSON_DIR = "public/data/session-pdfs-json"
PDF_DIR = "public/data/session-pdfs"

def extract_pdf_text(pdf_path):
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", pdf_path, "-"],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        return result.stdout
    except:
        return ""

def extract_companies_from_pdf(text):
    """
    Extract company names from PDF text.
    Strategy: Find lines that contain company names in the Société column.
    Company names appear as standalone words/phrases before the sector column.
    """
    lines = text.split('\n')
    companies = []
    
    # Skip header lines
    header_found = False
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        # Skip until we find the table header
        if 'Société' in stripped or 'Societe' in stripped:
            header_found = True
            continue
        
        if not header_found:
            continue
        
        # Stop at footer (retraits, commentaires section)
        if any(footer in stripped.lower() for footer in ['retrait du label', 'sociétés bénéficiaires', 'societes beneficiaires', 'les sociétés']):
            break
        
        # Try to extract company name from the beginning of the line
        # In layout mode, the company name is typically the first significant text
        parts = re.split(r'\s{2,}', stripped)
        if parts:
            candidate = parts[0].strip()
            # Filter out non-company entries
            if (candidate and 
                len(candidate) > 1 and 
                not candidate.isdigit() and 
                candidate not in ['Oui', 'Non', 'N.A', 'N.A.', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] and
                'Label' not in candidate and
                'Prélabel' not in candidate and
                'Fondateurs' not in candidate and
                'Secteur' not in candidate and
                'Résultat' not in candidate and
                'Commentaires' not in candidate and
                'Recevabilité' not in candidate and
                'Pitching' not in candidate and
                'Conflit' not in candidate and
                'Startup Act' not in candidate and
                'Compte-Rendu' not in candidate and
                'Session' not in candidate and
                '1er Tour' not in candidate and
                '2ème Tour' not in candidate and
                '3ème Tour' not in candidate):
                companies.append(candidate)
    
    return companies

def normalize_name(name):
    """Normalize a company name for comparison."""
    name = name.strip().lower()
    # Remove common prefixes/suffixes
    name = re.sub(r'\s+', ' ', name)
    return name

def main():
    print("=" * 80)
    print("VÉRIFICATION DES ENTRÉES INDIVIDUELLES vs PDF")
    print("=" * 80)
    
    all_sessions = []
    total_entries_json = 0
    total_entries_pdf = 0
    total_matches = 0
    total_mismatches = 0
    
    for fname in sorted(os.listdir(JSON_DIR)):
        if not fname.endswith(".json"):
            continue
        
        path = os.path.join(JSON_DIR, fname)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        session_id = data.get("session", "")
        pdf_name = data.get("pdf", "")
        entrees = data.get("entrees", [])
        nb_entrees = data.get("nb_entrees", 0)
        
        pdf_path = os.path.join(PDF_DIR, pdf_name)
        if not os.path.exists(pdf_path):
            print(f"⚠️  PDF manquant: {pdf_name}")
            continue
        
        pdf_text = extract_pdf_text(pdf_path)
        pdf_companies = extract_companies_from_pdf(pdf_text)
        
        # Get JSON company names
        json_companies = [e.get("societe", "").strip() for e in entrees if e.get("societe", "").strip()]
        
        # Count garbage entries in JSON (empty resultat, empty societe, etc.)
        garbage = [e for e in entrees if not e.get("societe", "").strip() or 
                   not e.get("resultat", "").strip() or
                   len(e.get("societe", "")) > 50]
        
        total_entries_json += len(json_companies)
        total_entries_pdf += len(pdf_companies)
        
        # Check if JSON companies match PDF companies
        json_norm = set(normalize_name(c) for c in json_companies)
        pdf_norm = set(normalize_name(c) for c in pdf_companies)
        
        matches = json_norm & pdf_norm
        json_only = json_norm - pdf_norm
        pdf_only = pdf_norm - json_norm
        
        match_ratio = len(matches) / max(len(json_norm), 1) * 100
        
        status = "✅" if match_ratio > 80 else "⚠️" if match_ratio > 50 else "❌"
        
        all_sessions.append({
            "session": session_id,
            "json_entries": len(entrees),
            "json_companies": len(json_companies),
            "pdf_companies": len(pdf_companies),
            "garbage": len(garbage),
            "matches": len(matches),
            "json_only": json_only,
            "pdf_only": pdf_only,
            "match_ratio": match_ratio,
            "status": status,
        })
        
        total_matches += len(matches)
        total_mismatches += len(json_only) + len(pdf_only)
        
        if match_ratio < 80:
            print(f"\n{status} Session {session_id} ({fname}):")
            print(f"   JSON: {len(entrees)} entrées, {len(json_companies)} sociétés")
            print(f"   PDF:  {len(pdf_companies)} sociétés")
            print(f"   Garbage: {len(garbage)} entrées")
            print(f"   Match: {match_ratio:.0f}% ({len(matches)}/{max(len(json_norm), len(pdf_norm))})")
            if json_only:
                print(f"   Seulement dans JSON ({len(json_only)}):")
                for c in sorted(json_only)[:5]:
                    print(f"      - {c[:60]}")
            if pdf_only:
                print(f"   Seulement dans PDF ({len(pdf_only)}):")
                for c in sorted(pdf_only)[:5]:
                    print(f"      - {c[:60]}")
    
    print(f"\n{'='*80}")
    print("RÉSUMÉ")
    print(f"{'='*80}")
    print(f"Sessions vérifiées: {len(all_sessions)}")
    print(f"Total entrées JSON: {total_entries_json}")
    print(f"Total sociétés PDF: {total_entries_pdf}")
    print(f"Matches: {total_matches}")
    print(f"Mismatches: {total_mismatches}")
    
    # Count by status
    clean = sum(1 for s in all_sessions if s['status'] == '✅')
    warning = sum(1 for s in all_sessions if s['status'] == '⚠️')
    error = sum(1 for s in all_sessions if s['status'] == '❌')
    print(f"\nStatut: ✅ {clean} propres, ⚠️ {warning} avertissements, ❌ {error} erreurs")
    
    # List sessions with issues
    if warning + error > 0:
        print(f"\n{'='*80}")
        print("SESSIONS AVEC PROBLÈMES")
        print(f"{'='*80}")
        for s in all_sessions:
            if s['status'] != '✅':
                print(f"\n{s['status']} Session {s['session']}:")
                print(f"   JSON: {s['json_entries']} entrées ({s['json_companies']} sociétés, {s['garbage']} garbage)")
                print(f"   PDF:  {s['pdf_companies']} sociétés")
                print(f"   Match: {s['match_ratio']:.0f}%")
                if s['json_only']:
                    print(f"   Faux positifs JSON ({len(s['json_only'])}):")
                    for c in sorted(s['json_only'])[:3]:
                        print(f"      - {c[:70]}")
                if s['pdf_only']:
                    print(f"   Manquants JSON ({len(s['pdf_only'])}):")
                    for c in sorted(s['pdf_only'])[:3]:
                        print(f"      - {c[:70]}")

if __name__ == "__main__":
    main()
