import json
from pathlib import Path
from collections import Counter
root=Path('/home/ubuntu/vic-2026-startup-act-4339943/public/data')
files=sorted((root/'session-pdfs-json').glob('session_*.json'))
entries=[]
for path in files:
    try: d=json.loads(path.read_text(encoding='utf-8'))
    except Exception: continue
    if isinstance(d, list):
        sid=path.stem.replace('session_','').replace('_','/')
        es=d
    else:
        sid=d.get('session') or path.stem.replace('session_','').replace('_','/')
        es=d.get('entries') or d.get('entrees') or []
    for e in es:
        entries.append((sid,e))

def norm(r):
    import unicodedata
    t=unicodedata.normalize('NFD',str(r or '')).lower()
    t=''.join(c for c in t if unicodedata.category(c)!='Mn')
    if 'report' in t: return 'Reporté'
    if 'pitch' in t and 'decal' in t: return 'Pitch décalé'
    if 'retrait' in t: return 'Retrait Label'
    pre='prelabel' in t or 'pre-label' in t
    if pre and ('non' in t or 'refus' in t): return 'Prélabel non accordé'
    if (not pre) and 'label' in t and ('non' in t or 'refus' in t): return 'Label non accordé'
    if pre and ('accord' in t): return 'Prélabel accordé'
    if 'label' in t and 'accord' in t: return 'Label accordé'
    return 'Inconnu'
print('files',len(files),'entries',len(entries))
print('decisions',Counter(norm(e.get('resultat_normalise') or e.get('resultat') or e.get('decision')) for _,e in entries))
print('sessions',Counter(s for s,_ in entries).most_common(3))
