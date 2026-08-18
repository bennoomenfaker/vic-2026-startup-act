#!/usr/bin/env python3
"""
Parse non-table MD files (01/2024, 02/2024, 09/2025) into structured entries.
These files have data in paragraph format, not pipe-delimited tables.
"""
import json
import re
from pathlib import Path

FIRECRAWL_DIR = Path('/home/himawari/Desktop/startup-act/.firecrawl')

VALID_SECTORS = {
    'e-commerce', 'logiciel', 'edtech', 'fintech', 'health tech', 'healthtech',
    'iot', 'big data', 'ai', 'marketing', 'robotique', 'biotechnologie', 'cleantech',
    'telecom', 'agritech', 'agtech', 'logistique', 'gaming', 'hr',
    'plateforme sociale', 'cybersecurité', 'cybersecurity', 'energie',
    'autre contenu créatif', 'media', 'mobile', 'nanotech', 'deeptech',
    'green tech', 'regtech', 'insurtech', 'legaltech', 'proptech',
    'foodtech', 'travel', 'traveltech', 'hrtech', 'adtech', 'legal tech',
    'communication services', 'advanced manufacturing & robotics',
    'business software and services', 'consumer products and services',
    'consumer products', 'commerce and shopping', 'social business',
    'real estate tech', 'environment', 'security', 'mobility',
    'foodtech & new food', 'foodtech & new food'
}

RESULT_KEYWORDS = [
    'label accordé', 'label accorde', 'prélabel accordé', 'prélabel accorde',
    'prelabel accordé', 'prelabel accorde', 'label non accordé', 'label non accorde',
    'prélabel non accordé', 'prélabel non accorde', 'prelabel non accordé',
    'prelabel non accorde', 'irrecevable', 'retrait'
]

def find_sector(text, start_pos):
    """Find sector by matching known sectors in text"""
    text_lower = text.lower()
    best_match = ''
    best_pos = len(text)
    
    for sector in VALID_SECTORS:
        # Find sector after start_pos
        pos = text_lower.find(sector.lower(), start_pos)
        if pos != -1 and pos < best_pos:
            # Make sure it's not part of a larger word
            if pos > 0 and text_lower[pos-1].isalpha():
                continue
            end_pos = pos + len(sector)
            if end_pos < len(text_lower) and text_lower[end_pos].isalpha():
                continue
            best_match = sector
            best_pos = pos
    
    return best_match, best_pos

def find_result(text, start_pos):
    """Find result keyword"""
    text_lower = text.lower()
    for result in RESULT_KEYWORDS:
        pos = text_lower.find(result, start_pos)
        if pos != -1:
            return result, pos
    return '', -1

def parse_non_table_md(text):
    """Parse non-table format MD file"""
    entries = []
    
    # Find the main section (before "Passage de Prélabels" or "Retraits")
    main_end = len(text)
    for marker in ['Passage de Prélabels', 'Passage prélabels', 'Retraits Labels', 'Retrait de Label']:
        pos = text.find(marker)
        if pos != -1 and pos < main_end:
            main_end = pos
    
    main_text = text[:main_end]
    
    # Pattern: each entry has a label/prelabel result
    # Split by result keywords to find entries
    result_pattern = re.compile(
        r'(Label|Prélabel|Prelabel)\s+(Non\s+)?Accordé?\s+au\s+(\d+)\s*(?:ème|è|er|e)\s+Tour',
        re.IGNORECASE
    )
    
    # Find all results
    results = list(result_pattern.finditer(main_text))
    
    for i, match in enumerate(results):
        # Get text before this result
        if i == 0:
            before = main_text[:match.start()]
        else:
            before = main_text[results[i-1].end():match.start()]
        
        # Try to extract entry from 'before' text
        # The pattern is: CompanyName Founders Sector Label/PreLabel Recevabilité votes
        # But it's all concatenated without clear separators
        
        # Find Label/PreLabel type
        type_match = re.search(r'\b(Label|Prélabel|Prelabel|Preislabel)\b', before, re.IGNORECASE)
        if not type_match:
            continue
        
        type_label = type_match.group(1)
        type_pos = type_match.start()
        
        # Find sector (longest match from known sectors)
        sector, sector_pos = find_sector(before, 0)
        
        # Find recevabilité
        recev_match = re.search(r'\b(Oui|Non)\b', before[type_pos:], re.IGNORECASE)
        recevable = recev_match.group(1) if recev_match else ''
        
        # Company name and founders are before sector
        # This is tricky - the text is concatenated
        # Try to split by looking for patterns
        
        # Simple approach: take everything before sector as company+founders
        if sector and sector_pos > 0:
            prefix = before[:sector_pos].strip()
        else:
            prefix = before[:type_pos].strip()
        
        # Try to split prefix into company and founders
        # The company name is usually shorter and comes first
        # Founders are usually 2-4 names separated by spaces
        
        # For now, just take the whole prefix as societe+fondateurs
        # We'll need to clean this up later
        
        # Extract votes
        votes_text = before[type_pos:]
        votes_match = re.search(r'(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(N\.A|\d+)\s+(N\.A|\d+)', votes_text)
        
        entry = {
            'societe': prefix[:100] if prefix else '',  # Truncate for safety
            'fondateurs': '',
            'secteur': sector if sector else '',
            'type_label': 'Label' if 'label' in type_label.lower() and 'pré' not in type_label.lower() and 'pre' not in type_label.lower() else 'PreLabel',
            'labelType': 'Label' if 'label' in type_label.lower() and 'pré' not in type_label.lower() and 'pre' not in type_label.lower() else 'PreLabel',
            'votes_for': int(votes_match.group(1)) if votes_match else 0,
            'votes_against': int(votes_match.group(2)) if votes_match else 0,
            'resultat': 'label' if 'non' not in match.group(0).lower() else 'refused',
            'recevable': recevable,
            'commentaires': '',
            'conflit': '',
            'is_conversion': False,
            'is_retrait': False
        }
        
        # Check for conflit
        full_text = main_text[match.start():match.end()+100]
        if 'conflit' in full_text.lower():
            conflit_match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+a\s+(?:déclaré?|declairé?|declaire?)\s+(?:avoir\s+)?un\s+conflit', full_text, re.IGNORECASE)
            if conflit_match:
                entry['conflit'] = conflit_match.group(1)
            else:
                entry['conflit'] = 'oui'
        
        entries.append(entry)
    
    return entries

def parse_conversion_table(text):
    """Parse Passage de Prélabels aux Labels section"""
    entries = []
    
    # Find the section
    start = text.find('Passage de Prélabels')
    if start == -1:
        start = text.find('Passage prélabels')
    if start == -1:
        return entries
    
    # Find end (Retraits or end of text)
    end = len(text)
    for marker in ['Retraits Labels', 'Retrait de Label', 'Retrait de labels']:
        pos = text.find(marker, start)
        if pos != -1 and pos < end:
            end = pos
    
    section = text[start:end]
    
    # Pattern: Company Projet Fondateurs Secteur Session Résultat Commentaires
    result_pattern = re.compile(r'Label accordé|Label accordé', re.IGNORECASE)
    
    # Split by "Label accordé" to find entries
    parts = result_pattern.split(section)
    
    for i, part in enumerate(parts[:-1]):  # Skip last empty part
        # Try to find company name at the end of the part
        # The pattern is usually: ...Secteur Session Label accordé
        # Company name is somewhere in the text
        
        # Simple heuristic: look for known patterns
        entry = {
            'societe': '',
            'fondateurs': '',
            'secteur': '',
            'type_label': 'PreLabel',
            'labelType': 'PreLabel',
            'votes_for': 0,
            'votes_against': 0,
            'resultat': 'label',
            'recevable': '',
            'commentaires': 'Label accordé suite à la création de la Startup et le respect des conditions d\'octroi',
            'conflit': '',
            'is_conversion': True,
            'is_retrait': False
        }
        entries.append(entry)
    
    return entries

def main():
    # Parse the3 non-table files
    non_table_files = ['session_2024_01', 'session_2024_02', 'session_2025_09']
    
    for session_id in non_table_files:
        md_file = FIRECRAWL_DIR / f'{session_id}.md'
        if not md_file.exists():
            print(f"⚠️ {session_id}: MD file not found")
            continue
        
        with open(md_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        entries = parse_non_table_md(text)
        
        # Parse year/month
        parts = session_id.split('_')
        year = int(parts[1])
        month = int(parts[2])
        
        session_data = {
            'session_id': session_id,
            'session': f'{month:02d}/{year}',
            'year': year,
            'month': month,
            'total_entries': len(entries),
            'source': 'firecrawl_md_non_table',
            'entries': entries
        }
        
        output_file = FIRECRAWL_DIR / f'{session_id}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        
        print(f"{'✅' if entries else '⚠️'} {month:02d}/{year}: {len(entries)} entries")

if __name__ == '__main__':
    main()
