from pathlib import Path
root=Path('/home/ubuntu/vic-2026-startup-act-4339943/public/data/session-pdfs-json')
old='Généré depuis le master harmonisé 85 sessions + trois PDF officiels 2026; décisions normalisées et sections conservées'
new='Généré depuis le corpus final validé de 88 sessions (S0–S87); décisions normalisées et sections conservées'
changed=0
for p in sorted(root.glob('*.json')):
    s=p.read_text(encoding='utf-8')
    if old in s:
        p.write_text(s.replace(old,new),encoding='utf-8')
        changed+=1
print('changed',changed)
