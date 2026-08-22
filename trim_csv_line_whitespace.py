from pathlib import Path
root=Path('/home/ubuntu/vic-2026-startup-act-4339943/public/data')
files=list((root/'reextraction_validee_88').glob('*.csv')) + [root/n for n in ['database_sessions.csv','database_entrees_brutes.csv','database_founders.csv','database_startup_founders.csv','database_88.csv','database_sessions_88.csv','database_entrees_brutes_88.csv','database_founders_88.csv','database_startup_founders_88.csv','gender_stats_88.csv'] if (root/n).exists()]
changed=0
for p in sorted(set(files)):
    b=p.read_bytes()
    t=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
    t=b'\n'.join(line.rstrip(b' \t') for line in t.split(b'\n'))
    if t!=b:
        p.write_bytes(t)
        changed+=1
print('files_trimmed',changed)
