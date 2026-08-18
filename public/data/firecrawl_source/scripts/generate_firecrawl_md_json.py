#!/usr/bin/env python3
"""
Script d'extraction PDF vers Markdown et JSON via Firecrawl CLI Parse
Auteur: Antigravity / AGY
"""

import os
import glob
import time
import json
import subprocess

INPUT_DIR = '/home/himawari/Desktop/startup-act/public/data/session-pdfs'
OUTPUT_DIR = '/home/himawari/Desktop/startup-act/public/data/agy/firecrawl_pdf_json'

os.makedirs(OUTPUT_DIR, exist_ok=True)

pdf_files = sorted(glob.glob(os.path.join(INPUT_DIR, 'session_*.pdf')))
print(f"Début de l'extraction de {len(pdf_files)} PDFs avec Firecrawl Parse...")

summary = {}
processed_count = 0

for pdf_path in pdf_files:
    basename = os.path.basename(pdf_path)
    session_id = os.path.splitext(basename)[0]
    out_md_path = os.path.join(OUTPUT_DIR, f"{session_id}.md")
    out_json_path = os.path.join(OUTPUT_DIR, f"{session_id}.json")
    
    # Éviter de re-traiter les fichiers déjà valides
    if os.path.exists(out_json_path) and os.path.exists(out_md_path):
        try:
            with open(out_json_path, 'r', encoding='utf-8') as f:
                d = json.load(f)
                if d.get('char_count', 0) > 0:
                    summary[session_id] = {
                        'char_count': d.get('char_count', 0),
                        'has_text': True
                    }
                    continue
        except Exception:
            pass

    # Exécution de Firecrawl CLI Parse
    cmd = f'firecrawl parse "{pdf_path}" -o "{out_md_path}"'
    os.system(cmd)
    
    md_content = ''
    if os.path.exists(out_md_path):
        with open(out_md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
            
    json_data = {
        'session_id': session_id,
        'pdf_filename': basename,
        'has_text': len(md_content.strip()) > 0,
        'char_count': len(md_content.strip()),
        'full_text_markdown': md_content.strip()
    }
    
    with open(out_json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
        
    summary[session_id] = {
        'char_count': len(md_content.strip()),
        'has_text': len(md_content.strip()) > 0
    }
    
    processed_count += 1
    print(f"[{processed_count}] {session_id} -> {len(md_content.strip())} caractères")
    
    # Pause séquentielle de 6s pour respecter le rate limit de 10-15 req/min
    time.sleep(6)

with open(os.path.join(OUTPUT_DIR, 'summary.json'), 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print(f"Extraction Firecrawl terminée avec succès dans : {OUTPUT_DIR}")
