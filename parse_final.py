#!/usr/bin/env python3
"""Final parser: Firecrawl + Antigravity for all 85 sessions"""
import os
import re
import json
from pathlib import Path

def parse_firecrawl_table(filepath):
    """Parse Firecrawl markdown table"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    rows = []
    
    for line in lines:
        if not line.strip() or re.match(r'^[\s\-|]+$', line):
            continue
        
        if '|' in line and line.count('|') >= 3:
            cells = [c.strip() for c in line.strip('|').split('|')]
            
            header_keywords = ['société', 'fondateurs', 'fondationurs', 'secteur', 'résultat']
            if any(kw in ' '.join(cells).lower() for kw in header_keywords):
                continue
            
            if all(c in ['', '-', '---'] for c in cells):
                continue
            
            if len(cells) >= 6 and cells[0]:
                rows.append(cells)
        
        elif not line.startswith('|') and not line.startswith('*') and not line.startswith('#'):
            if 'Accordé' in line or 'Non Accordé' in line:
                parts = re.split(r'\s{2,}', line.strip())
                if len(parts) >= 5:
                    for i, part in enumerate(parts):
                        if part.isdigit() and i > 3:
                            company = ' '.join(parts[:i-2])
                            sector = parts[i-2]
                            label_type = parts[i-1]
                            votes = parts[i:i+4] if len(parts) > i+4 else parts[i:]
                            result = ' '.join(parts[i+4:]) if len(parts) > i+4 else ''
                            row = [company, '', sector, label_type, 'Oui'] + votes + [result]
                            rows.append(row)
                            break
    
    return rows

def parse_antigravity_text(text):
    """Parse antigravity text into rows"""
    lines = text.split('\n')
    rows = []
    
    for line in lines:
        line = line.strip()
        if not line or 'PAGE BREAK' in line:
            continue
        
        if 'Accordé' in line or 'Non Accordé' in line:
            parts = re.split(r'\s{2,}', line)
            if len(parts) >= 5:
                for i, part in enumerate(parts):
                    if part.isdigit() and i > 3:
                        company = ' '.join(parts[:i-2])
                        sector = parts[i-2]
                        label_type = parts[i-1]
                        votes = parts[i:i+4] if len(parts) > i+4 else parts[i:]
                        result = ' '.join(parts[i+4:]) if len(parts) > i+4 else ''
                        row = [company, '', sector, label_type, 'Oui'] + votes + [result]
                        rows.append(row)
                        break
    
    return rows

def rows_to_entries(rows):
    """Convert rows to structured entries"""
    entries = []
    for row in rows:
        try:
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
        except:
            continue
    return entries

def main():
    firecrawl_dir = Path('.firecrawl')
    antigravity_dir = Path('/tmp/antigravity_pdf_json')
    output_dir = Path('public/data/firecrawl_sessions')
    output_dir.mkdir(exist_ok=True)
    
    # Get all sessions
    all_sessions = sorted([f.stem.replace('session_', '') for f in Path('public/data/session-pdfs').glob('session_*.pdf')])
    
    results = []
    issues = []
    
    for session_id in all_sessions:
        yyyy, mm = session_id.split('_')
        session_key = f'{mm}/{yyyy}'
        
        # Skip if already parsed with entries
        output_file = output_dir / f'session_{session_id}.json'
        if output_file.exists():
            try:
                with open(output_file) as f:
                    existing = json.load(f)
                if existing.get('total_entries', 0) > 0:
                    results.append(existing)
                    print(f"⏭️  {session_key}: {existing['total_entries']} entries (existing)")
                    continue
            except:
                pass
        
        # Try Firecrawl first
        firecrawl_file = firecrawl_dir / f'session_{session_id}.md'
        antigravity_file = antigravity_dir / f'session_{session_id}.json'
        
        entries = []
        source = 'firecrawl'
        
        if firecrawl_file.exists():
            rows = parse_firecrawl_table(firecrawl_file)
            entries = rows_to_entries(rows)
        
        # Fallback to antigravity
        if len(entries) == 0 and antigravity_file.exists():
            try:
                with open(antigravity_file) as f:
                    data = json.load(f)
                text = data.get('full_text', '')
                if text:
                    rows = parse_antigravity_text(text)
                    entries = rows_to_entries(rows)
                    source = 'antigravity'
            except:
                pass
        
        session_data = {
            'session': session_key,
            'year': int(yyyy),
            'month': int(mm),
            'total_entries': len(entries),
            'source': source,
            'entries': entries
        }
        
        # Save individual session
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        
        results.append(session_data)
        
        if session_data['total_entries'] == 0:
            issues.append(f"⚠️  {session_key}: 0 entries!")
        
        status = '✅' if session_data['total_entries'] > 0 else '⚠️'
        print(f"{status} {session_key}: {session_data['total_entries']} entries ({source})")
    
    # Save summary
    summary_file = output_dir / 'summary.json'
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total_sessions': len(results),
            'total_entries': sum(r['total_entries'] for r in results),
            'sessions': [{'session': r['session'], 'entries': r['total_entries'], 'source': r['source']} for r in results],
            'issues': issues
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== TOTAL: {len(results)} sessions, {sum(r['total_entries'] for r in results)} entries ===")
    if issues:
        print(f"\n=== ISSUES ({len(issues)}) ===")
        for issue in issues:
            print(issue)

if __name__ == '__main__':
    main()
