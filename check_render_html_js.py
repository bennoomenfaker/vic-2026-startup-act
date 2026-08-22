from pathlib import Path
import re, subprocess, tempfile, sys
html=Path('/home/ubuntu/vic-2026-startup-act-4339943/streamlit-app/public/index.html').read_text(encoding='utf-8')
scripts=[]
for match in re.finditer(r'<script([^>]*)>(.*?)</script>', html, flags=re.S|re.I):
    attrs, body = match.group(1).lower(), match.group(2)
    if 'application/ld+json' in attrs or 'application/json' in attrs:
        continue
    scripts.append(body)
errors=[]
for i,script in enumerate(scripts,1):
    if not script.strip():
        continue
    p=Path('/tmp/render_inline_%02d.js'%i)
    p.write_text(script, encoding='utf-8')
    r=subprocess.run(['node','--check',str(p)],capture_output=True,text=True)
    if r.returncode:
        errors.append((i,r.stderr.strip()))
print('executable_scripts',len(scripts),'nonempty',sum(bool(s.strip()) for s in scripts))
if errors:
    for i,e in errors: print('ERROR',i,e)
    sys.exit(1)
print('all_inline_scripts_syntax_ok')
