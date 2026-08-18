#!/usr/bin/env python3
"""Parse antigravity text with multi-line format"""
import os
import re
import json
from pathlib import Path

def parse_antigravity_multiline(text):
    """Parse antigravity text where each entry spans multiple lines"""
    lines = text.split('\n')
    entries = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip headers and empty lines
        if not line or 'PAGE BREAK' in line or line in ['Société', 'Fondateurs', 'Secteur', 'Label/Prélabel', '1er Tour', '2ème Tour', '3ème Tour', 'Résultat', 'Recevabilité']:
            i += 1
            continue
        
        # Look for company name pattern: followed by founder names and sector
        # A company name is typically short and followed by multiple lines
        if (not line.isdigit() and 
            line not in ['Oui', 'Non', 'N.A', 'Pitching', 'Conflit', 'Label', 'Prélabel'] and
            'Accordé' not in line and
            'Non' not in line):
            
            company = line
            founders = []
            sector = ''
            label_type = ''
            votes = []
            result = ''
            
            j = i + 1
            while j < len(lines) and j < i + 15:
                next_line = lines[j].strip()
                
                if 'Accordé' in next_line or 'Non Accordé' in next_line:
                    result = next_line
                    break
                
                if next_line in ['Label', 'Prélabel']:
                    label_type = next_line
                
                if next_line.isdigit():
                    votes.append(int(next_line))
                
                if next_line in ['Oui', 'Non', 'N.A']:
                    pass  # Skip vote indicators
                
                j += 1
            
            if result and votes:
                entry = {
                    'societe': company,
                    'fondateurs': ' '.join(founders) if founders else '',
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
    
    problem_sessions = ['session_2020_07', 'session_2020_12', 'session_2021_01', 
                        'session_2024_01', 'session_2024_02', 'session_2025_09']
    
    for session_id in problem_sessions:
        antigravity_file = antigravity_dir / f'{session_id}.json'
        
        if not antigravity_file.exists():
            print(f'❌ {session_id}: file not found')
            continue
        
        with open(antigravity_file) as f:
            data = json.load(f)
        
        text = data.get('full_text', '')
        entries = parse_antigravity_multiline(text)
        
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
        
        output_file = output_dir / f'{session_id}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        
        print(f'{"✅" if len(entries) > 0 else "⚠️"} {session_key}: {len(entries)} entries')

if __name__ == '__main__':
    main()
