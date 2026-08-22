import json
from pathlib import Path
p=Path('/home/ubuntu/vic-2026-startup-act-4339943/public/data/dashboard_data.json')
d=json.loads(p.read_text(encoding='utf-8'))
for key in ['conversions','retraits','candidatures','labels','preLabels','entries','reportes']:
    print(key,sum(int(s.get(key) or 0) for s in d.get('sessions',[])))
print('meta', {k:d.get('meta',{}).get(k) for k in ['totalCandidatures','totalLabels','totalPreLabels','totalSessions','detailedEntries']})
print('database', {k:d.get('database',{}).get(k) for k in ['totalStartups']})
