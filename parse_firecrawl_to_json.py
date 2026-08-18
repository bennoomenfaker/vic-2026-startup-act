#!/usr/bin/env python3
"""Parse Firecrawl markdown tables into structured JSON"""
import os
import re
import json
from pathlib import Path

def parse_markdown_table(filepath):
    """Parse a markdown table file into rows"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    rows = []
    in_table = False
    
    for line in lines:
        # Skip separator lines
        if re.match(r'^\|[\s\-|]+\|$', line):
            continue
        
        # Parse table rows
        if line.startswith('|') and line.endswith('|'):
            # Remove leading/trailing pipes and split
            cells = [c.strip() for c in line.strip('|').split('|')]
            
            # Skip header rows (they contain "Société" or "Fondateurs")
            if any(h in ' '.join(cells).lower() for h in ['société', 'fondateurs', 'honduras']):
                continue
            
            # Skip empty rows
            if all(c in ['', '-'] for c in cells):
                continue
            
            rows.append(cells)
    
    return rows

def parse_session(filepath):
    """Parse a session file and extract structured data"""
    rows = parse_markdown_table(filepath)
    
    filename = os.path.basename(filepath).replace('.md', '')
    # Extract year and month from filename like session_2023_04
    parts = filename.split('_')
    year = parts[1]
    month = parts[2]
    
    entries = []
    for row in rows:
        if len(row) >= 10:
            entry = {
                'societe': row[0],
                'fondateurs': row[1],
                'secteur': row[2],
                'type_label': row[3],  # Label or Prélabel
                'recevabilite': row[4] if row[4] else None,
                'oui': int(row[5]) if row[5] and row[5].isdigit() else 0,
                'non': int(row[6]) if row[6] and row[6].isdigit() else 0,
                'pitching': int(row[7]) if row[7] and row[7].isdigit() else 0,
                'conflit': int(row[8]) if row[8] and row[8].isdigit() else 0,
                'resultat': row[10] if len(row) > 10 else None,
                'commentaires': row[11] if len(row) > 11 else None
            }
            entries.append(entry)
    
    return {
        'session': f'{month}/{year}',
        'year': int(year),
        'month': int(month),
        'total_entries': len(entries),
        'entries': entries
    }

def main():
    firecrawl_dir = Path('.firecrawl')
    output_dir = Path('public/data/firecrawl_sessions')
    output_dir.mkdir(exist_ok=True)
    
    results = []
    
    for md_file in sorted(firecrawl_dir.glob('session_*.md')):
        session_data = parse_session(md_file)
        
        # Save individual session
        output_file = output_dir / f'{md_file.stem}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        
        results.append(session_data)
        print(f"✅ {session_data['session']}: {session_data['total_entries']} entries")
    
    # Save summary
    summary_file = output_dir / 'summary.json'
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total_sessions': len(results),
            'total_entries': sum(r['total_entries'] for r in results),
            'sessions': [{'session': r['session'], 'entries': r['total_entries']} for r in results]
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== TOTAL: {len(results)} sessions, {sum(r['total_entries'] for r in results)} entries ===")

if __name__ == '__main__':
    main()
