#!/usr/bin/env python3
"""Improved parser for antigravity text format"""
import os
import re
import json
from pathlib import Path

def parse_antigravity_text(text):
    """Parse antigravity text - handles standalone result lines"""
    lines = text.split('\n')
    entries = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines, PAGE BREAK, headers
        if not line or 'PAGE BREAK' in line or line in ['Société', 'Fondateurs', 'Secteur', 'Label/Prélabel']:
            i += 1
            continue
        
        # Check if this looks like a company name (not a number, not a result)
        if (not line.isdigit() and 
            line not in ['Oui', 'Non', 'N.A', 'Pitching', 'Conflit'] and
            'Accordé' not in line and
            'Non' not in line.split()[0:1]):
            
            # This might be a company name - look ahead for more data
            company = line
            founders = ''
            sector = ''
            label_type = ''
            votes = [0, 0, 0, 0]
            result = ''
            
            # Try to find the next lines with data
            j = i + 1
            while j < len(lines) and j < i + 10:
                next_line = lines[j].strip()
                
                if 'Accordé' in next_line or 'Non Accordé' in next_line:
                    result = next_line
                    break
                
                if next_line in ['Label', 'Prélabel']:
                    label_type = next_line
                
                if next_line.isdigit():
                    votes.append(int(next_line))
                
                j += 1
            
            if result:
                entry = {
                    'societe': company,
                    'fondateurs': founders,
                    'secteur': sector,
                    'type_label': label_type,
                    'oui': votes[0] if len(votes) > 0 else 0,
                    'non': votes[1] if len(votes) > 1 else 0,
                    'resultat': result,
                    'commentaires': ''
                }
                entries.append(entry)
        
        i += 1
    
    return entries

def main():
    antigravity_dir = Path('/tmp/antigravity_pdf_json')
    output_dir = Path('public/data/firecrawl_sessions')
    output_dir.mkdir(exist_ok=True)
    
    # Sessions that need antigravity
    problem_sessions = ['session_2020_07', 'session_2020_12', 'session_2021_01', 
                        'session_2024_01', 'session_2024_02', 'session_2025_09']
    
    for session_id in problem_sessions:
        antigravity_file = antigravity_dir / f'{session_id}.json'
        
        if not antigravity_file.exists():
            print(f'❌ {session_id}: antigravity file not found')
            continue
        
        with open(antigravity_file) as f:
            data = json.load(f)
        
        text = data.get('full_text', '')
        entries = parse_antigravity_text(text)
        
        yyyy, mm = session_id.replace('session_', '').split('_')
        session_key = f'{mm}/{yyyy}'
        
        session_data = {
            'session': session_key,
            'year': int(yyyy),
            'month': int(mm),
            'total_entries': len(entries),
            'source': 'antigravity',
            'entries': entries
        }
        
        # Save
        output_file = output_dir / f'{session_id}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        
        print(f'{"✅" if len(entries) > 0 else "⚠️"} {session_key}: {len(entries)} entries')
        
        # Show first few entries
        for e in entries[:3]:
            print(f'   {e["societe"]}: {e["resultat"]}')

if __name__ == '__main__':
    main()
