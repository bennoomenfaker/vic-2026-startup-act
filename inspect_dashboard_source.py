import json
from pathlib import Path
p=Path('/home/ubuntu/vic-2026-startup-act-88-remote/public/data/dashboard_data.json')
d=json.loads(p.read_text(encoding='utf-8'))
print('keys',list(d.keys()))
for k,v in d.items():
    if isinstance(v,list): print(k,'len',len(v))
    elif isinstance(v,dict): print(k,'keys',list(v.keys())[:25])
print('meta',d.get('meta'))
rows=d.get('pdfExtracted',[])
print('pdfExtracted',len(rows))
print('sample',rows[:2])
for field in ['societe','nom','company']:
    vals=[str(r.get(field,'')).strip().casefold() for r in rows if str(r.get(field,'')).strip()]
    if vals: print(field,'nonblank',len(vals),'unique',len(set(vals)))
from collections import Counter
for key in ['resultat_normalise','section','secteur']:
    c=Counter(r.get(key,'') for r in rows); print(key,c.most_common(20))
print('session_id candidates',Counter(r.get('session') for r in rows).most_common(5))
