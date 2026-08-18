#!/usr/bin/env python3
"""
Parse all 85 .firecrawl MD files into structured JSON session files.
Handles both table-format (pipe-delimited) and non-table formats.
"""
import json
import re
from pathlib import Path

FIRECRAWL_DIR = Path('/home/himawari/Desktop/startup-act/.firecrawl')
OUTPUT_DIR = Path('/home/himawari/Desktop/startup-act/.firecrawl')

# Valid sectors
VALID_SECTORS = {
    'e-commerce', 'logiciel', 'edtech', 'fintech', 'health tech', 'iot',
    'big data', 'ai', 'marketing', 'robotique', 'biotechnologie', 'cleantech',
    'telecom', 'agritech', 'agtech', 'logistique', 'gaming', 'hr',
    'plateforme sociale', 'cybersecurité', 'cybersecurity', 'energie',
    'autre contenu créatif', 'media', 'mobile', 'nanotech', 'deeptech',
    'green tech', 'regtech', 'insurtech', 'legaltech', 'proptech',
    'foodtech', 'travel', 'hrtech', 'adtech', 'legal tech'
}

def classify_result(text):
    """Classify result into label/preLabel/refused/irrecevable"""
    t = text.lower().strip()
    if 'irrecevable' in t or 'irreceval' in t or 'irreecev' in t:
        return 'irrecevable'
    if 'retrait' in t:
        return 'retrait'
    if 'label' in t and 'non' not in t:
        return 'label'
    if 'prélabel' in t or 'prelabel' in t:
        if 'non' in t:
            return 'refused'
        return 'preLabel'
    if 'label' in t and 'non' in t:
        return 'refused'
    if 'prèlabel' in t:
        if 'non' in t:
            return 'refused'
        return 'preLabel'
    if 'accord' in t and 'non' not in t:
        return 'label'
    if 'non accord' in t:
        return 'refused'
    return 'unknown'

def classify_type_label(text):
    """Get type from column: Label, Prélabel, Prelabel"""
    t = text.lower().strip()
    if 'prélabel' in t or 'prelabel' in t or 'prèlabel' in t or 'preislabel' in t:
        return 'PreLabel'
    if 'label' in t:
        return 'Label'
    return ''

def clean_name(name):
    """Clean OCR artifacts from names"""
    name = name.strip()
    # Remove leading/trailing pipes, dashes
    name = re.sub(r'^[\|\-\s]+', '', name)
    name = re.sub(r'[\|\-\s]+$', '', name)
    # Fix common OCR errors
    name = name.replace('&amp;', '&')
    name = name.replace('&#x27;', "'")
    name = name.replace('&#x27;', "'")
    name = name.replace('\\-', '-')
    name = re.sub(r'\\-', '-', name)
    return name.strip()

def parse_table_md(text):
    """Parse pipe-delimited markdown table"""
    entries = []
    lines = text.split('\n')
    
    # Track which table we're in
    in_main_table = False
    in_conversion_table = False
    in_retrait_table = False
    
    for line in lines:
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped or stripped == '---' or stripped == '* * *':
            continue
        
        # Detect section headers
        if 'Passage de Prélabels' in stripped or 'Passage de prélabels' in stripped:
            in_conversion_table = True
            in_main_table = False
            continue
        if 'Retrait de Label' in stripped or 'retrait de label' in stripped.lower():
            in_retrait_table = True
            in_main_table = False
            in_conversion_table = False
            continue
        
        # Skip non-table lines
        if '|' not in stripped:
            continue
        
        # Parse cells
        cells = [c.strip() for c in stripped.strip('|').split('|')]
        
        # Skip separator lines
        if all(c.strip() in ['', '-', '---', '----'] for c in cells):
            continue
        
        # Skip header rows
        header_words = ['société', 'fondateurs', 'fondation', 'secteur', 'résultat',
                       'handlateurs', 'señeur', 'seitur', 'label/preislabel', 'label/prélibel',
                       'commentaires', 'session d', 'projet', 'décision']
        line_lower = ' '.join(cells).lower()
        if any(hw in line_lower for hw in header_words):
            # But check if it's a data row with a company name
            if len(cells) >= 10 and cells[0] and not any(c in cells[0].lower() for c in ['société', 'fondation']):
                pass  # Could be data
            else:
                continue
        
        # Need at least 10 columns for main table
        if len(cells) < 10:
            continue
        
        societe = clean_name(cells[0])
        if not societe or len(societe) < 2:
            continue
        
        if in_retrait_table:
            # Retrait table: Société | Fondateurs | Secteur | Session | Décision | Commentaires
            entry = {
                'societe': societe,
                'fondateurs': clean_name(cells[1]) if len(cells) > 1 else '',
                'secteur': clean_name(cells[2]) if len(cells) > 2 else '',
                'type_label': '',
                'labelType': '',
                'votes_for': 0,
                'votes_against': 0,
                'resultat': 'retrait',
                'recevable': '',
                'commentaires': clean_name(cells[5]) if len(cells) > 5 else '',
                'conflit': '',
                'is_conversion': False,
                'is_retrait': True
            }
            entries.append(entry)
            continue
        
        if in_conversion_table:
            # Conversion table: Société | Projet | Fondateurs | Secteur | Session | Résultat | Commentaires
            entry = {
                'societe': societe,
                'fondateurs': clean_name(cells[2]) if len(cells) > 2 else '',
                'secteur': clean_name(cells[3]) if len(cells) > 3 else '',
                'type_label': 'PreLabel',
                'labelType': 'PreLabel',
                'votes_for': 0,
                'votes_against': 0,
                'resultat': classify_result(cells[5] if len(cells) > 5 else ''),
                'recevable': '',
                'commentaires': clean_name(cells[6]) if len(cells) > 6 else '',
                'conflit': '',
                'is_conversion': True,
                'is_retrait': False
            }
            entries.append(entry)
            continue
        
        # Main table
        type_label = classify_type_label(cells[3] if len(cells) > 3 else '')
        recevable = cells[4] if len(cells) > 4 else ''
        
        # Get result from column 10 or 11
        resultat_text = cells[10] if len(cells) > 10 else ''
        if not resultat_text or resultat_text.strip() in ['', '-']:
            resultat_text = cells[11] if len(cells) > 11 else ''
        
        # Get commentaires
        commentaires = cells[11] if len(cells) > 11 else ''
        if not commentaires or commentaires.strip() in ['', '-']:
            commentaires = cells[12] if len(cells) > 12 else ''
        
        # Parse votes
        try:
            votes_for = int(cells[5]) if cells[5].strip().isdigit() else 0
        except:
            votes_for = 0
        try:
            votes_against = int(cells[6]) if cells[6].strip().isdigit() else 0
        except:
            votes_against = 0
        
        # Check for conflit
        conflit = ''
        full_line = ' '.join(cells)
        if 'conflit' in full_line.lower():
            # Extract the conflit mention
            conflit_match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+a\s+(?:déclaré?|declairé?|declaire?)\s+un\s+conflit', full_line, re.IGNORECASE)
            if conflit_match:
                conflit = conflit_match.group(1)
            else:
                conflit = 'oui'
        
        entry = {
            'societe': societe,
            'fondateurs': clean_name(cells[1]) if len(cells) > 1 else '',
            'secteur': clean_name(cells[2]) if len(cells) > 2 else '',
            'type_label': type_label,
            'labelType': type_label,
            'votes_for': votes_for,
            'votes_against': votes_against,
            'resultat': classify_result(resultat_text),
            'recevable': recevable,
            'commentaires': clean_name(commentaires),
            'conflit': conflit,
            'is_conversion': False,
            'is_retrait': False
        }
        entries.append(entry)
    
    return entries

def main():
    md_files = sorted(FIRECRAWL_DIR.glob('*.md'))
    print(f"Found {len(md_files)} MD files in .firecrawl/")
    
    all_sessions = []
    total_entries = 0
    sessions_with_entries = 0
    
    for md_file in md_files:
        session_id = md_file.stem  # e.g. session_2019_03
        
        # Parse year/month from session_id
        parts = session_id.split('_')
        year = int(parts[1])
        month = int(parts[2])
        
        # Read MD
        with open(md_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Parse entries
        entries = parse_table_md(text)
        
        # Save individual JSON
        session_data = {
            'session_id': session_id,
            'session': f'{month:02d}/{year}',
            'year': year,
            'month': month,
            'total_entries': len(entries),
            'source': 'firecrawl_md',
            'entries': entries
        }
        
        output_file = OUTPUT_DIR / f'{session_id}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        
        all_sessions.append(session_data)
        total_entries += len(entries)
        if entries:
            sessions_with_entries += 1
        
        print(f"{'✅' if entries else '⚠️'} {month:02d}/{year}: {len(entries)} entries")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Total: {len(all_sessions)} sessions, {total_entries} entries")
    print(f"Sessions with entries: {sessions_with_entries}/{len(all_sessions)}")
    
    # Save summary
    summary = {
        'total_sessions': len(all_sessions),
        'total_entries': total_entries,
        'sessions_with_entries': sessions_with_entries,
        'sessions': [{
            'session_id': s['session_id'],
            'session': s['session'],
            'total_entries': s['total_entries']
        } for s in sorted(all_sessions, key=lambda x: x['session_id'])]
    }
    
    with open(OUTPUT_DIR / 'summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"\nSummary saved to {OUTPUT_DIR / 'summary.json'}")

if __name__ == '__main__':
    main()
