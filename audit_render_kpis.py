import json
from collections import Counter
from pathlib import Path
root=Path('/home/ubuntu/vic-2026-startup-act-4339943/public/data')
d=json.loads((root/'dashboard_data.json').read_text(encoding='utf-8'))
print('meta',d['meta'])
print('yearly')
for r in d.get('yearly',[]): print(r)
print('session sums', {k:sum(int(s.get(k) or 0) for s in d.get('sessions',[])) for k in ['candidatures','labels','preLabels','retraits','nbSessions']})
print('sessions first',d.get('sessions',[])[:3])
startups=d.get('database',{}).get('startups',[])
print('database totalStartups',d.get('database',{}).get('totalStartups'),'startups_len',len(startups))
print('startups label years',Counter(str(s.get('labelDate',''))[-4:] for s in startups).most_common(20))
rows=d.get('pdfExtracted',[])
print('detailed decision counts',Counter(r.get('resultat_normalise','') for r in rows))
print('detailed session counts',Counter(r.get('session') for r in rows).most_common(10))
