#!/usr/bin/env python3
"""Improved parser for Firecrawl markdown - handles various table formats"""
import os
import re
import json
from pathlib import Path

def parse_markdown_table(filepath):
    """Parse markdown table with various formats"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    rows = []
    
    for line in lines:
        # Skip empty lines and separators
        if not line.strip() or re.match(r'^[\s\-|]+$', line):
            continue
        
        # Parse table rows (with pipes)
        if '|' in line and line.count('|') >= 3:
            # Remove leading/trailing pipes and split
            cells = [c.strip() for c in line.strip('|').split('|')]
            
            # Skip header-like rows
            header_keywords = ['société', 'fondateurs', 'fondationurs', 'secteur', 'label', 'résultat']
            if any(kw in ' '.join(cells).lower() for kw in header_keywords):
                continue
            
            # Skip separator rows
            if all(c in ['', '-', '---'] for c in cells):
                continue
            
            # Only keep rows with enough data
            if len(cells) >= 6 and cells[0]:  # Must have a company name
                rows.append(cells)
        
        # Also handle lines without pipes (some PDFs have this format)
        elif not line.startswith('|') and not line.startswith('*') and not line.startswith('#'):
            # Try to split by multiple spaces
            cells = re.split(r'\s{2,}', line.strip())
            if len(cells) >= 6 and cells[0] and not any(kw in cells[0].lower() for kw in ['société', 'startup']):
                rows.append(cells)
    
    return rows

def parse_session(filepath):
    """Parse a session file"""
    rows = parse_markdown_table(filepath)
    
    filename = os.path.basename(filepath).replace('.md', '')
    parts = filename.split('_')
    year = parts[1]
    month = parts[2]
    
    entries = []
    for row in rows:
        try:
            # Find where the actual data starts (skip founder name if it's the first cell)
            # The pattern should be: company, founders, sector, type, votes, result
            
            entry = {
                'societe': row[0],
                'fondateurs': row[1] if len(row) > 1 else '',
                'secteur': row[2] if len(row) > 2 else '',
                'type_label': row[3] if len(row) > 3 else '',
                'recevabilite': row[4] if len(row) > 4 else '',
                'oui': int(row[5]) if len(row) > 5 and row[5].isdigit() else 0,
                'non': int(row[6]) if len(row) > 6 and row[6].isdigit() else 0,
                'resultat': row[10] if len(row) > 10 else (row[9] if len(row) > 9 else ''),
                'commentaires': row[11] if len(row) > 11 else (row[10] if len(row) > 10 else '')
            }
            entries.append(entry)
        except Exception as e:
            continue
    
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
    issues = []
    
    for md_file in sorted(firecrawl_dir.glob('session_*.md')):
        session_data = parse_session(md_file)
        
        # Save individual session
        output_file = output_dir / f'{md_file.stem}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        
        results.append(session_data)
        
        # Check for issues
        if session_data['total_entries'] == 0:
            issues.append(f"⚠️  {session_data['session']}: 0 entries!")
        elif session_data['total_entries'] < 5:
            issues.append(f"⚠️  {session_data['session']}: only {session_data['total_entries']} entries")
        
        print(f"{'✅' if session_data['total_entries'] > 0 else '⚠️'} {session_data['session']}: {session_data['total_entries']} entries")
    
    # Save summary
    summary_file = output_dir / 'summary.json'
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total_sessions': len(results),
            'total_entries': sum(r['total_entries'] for r in results),
            'sessions': [{'session': r['session'], 'entries': r['total_entries']} for r in results],
            'issues': issues
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== TOTAL: {len(results)} sessions, {sum(r['total_entries'] for r in results)} entries ===")
    if issues:
        print(f"\n=== ISSUES ({len(issues)}) ===")
        for issue in issues:
            print(issue)

if __name__ == '__main__':
    main()
