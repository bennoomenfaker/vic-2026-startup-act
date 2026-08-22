import json
from collections import Counter
from pathlib import Path
root=Path('/home/ubuntu/vic-2026-startup-act-4339943/public/data')
for name in ['dashboard_data.json','sessions.json','session_pdfs_extracted.json','founder_db.json','parcours.json']:
    p=root/name
    if not p.exists():
        print(name,'MISSING'); continue
    d=json.loads(p.read_text(encoding='utf-8'))
    print('\n',name, type(d).__name__)
    if isinstance(d,dict):
        print('keys',list(d.keys())[:20])
        if 'meta' in d: print('meta',d['meta'])
        if 'totalStartups' in d: print('totalStartups',d['totalStartups'])
        if 'sessions' in d and isinstance(d['sessions'],list): print('sessions_len',len(d['sessions']))
        if 'entries' in d and isinstance(d['entries'],list): print('entries_len',len(d['entries']))
    elif isinstance(d,list): print('len',len(d))
# detailed variants
for name in ['session_pdfs_extracted.json']:
    p=root/name
    if p.exists():
        d=json.loads(p.read_text(encoding='utf-8'))
        rows=d.get('entries',d) if isinstance(d,dict) else d
        print('rows',len(rows))
        print('decision_counts',Counter(r.get('resultat_normalise',r.get('decision','')) for r in rows).most_common())
        names=[str(r.get('societe','')).strip().casefold() for r in rows if str(r.get('societe','')).strip()]
        print('unique_societe_casefold',len(set(names)))
