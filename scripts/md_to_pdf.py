#!/usr/bin/env python3
"""Convertit un fichier Markdown (livrables) en PDF via HTML + LibreOffice."""
import re
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent


def inline(text):
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text


def convert(md_text):
    lines = md_text.splitlines()
    html = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith('### '):
            html.append(f'<h3>{inline(line[4:].strip())}</h3>')
        elif line.startswith('## '):
            html.append(f'<h2>{inline(line[3:].strip())}</h2>')
        elif line.startswith('# '):
            html.append(f'<h1>{inline(line[2:].strip())}</h1>')
        elif line.startswith('---'):
            html.append('<hr>')
        elif line.startswith('|'):
            table, i = _table(lines, i)
            html.append(table)
            continue
        elif re.match(r'^\s*[-*] ', line):
            items = []
            while i < len(lines) and re.match(r'^\s*[-*] ', lines[i]):
                items.append(f'<li>{inline(lines[i].lstrip())[2:].strip()}</li>')
                i += 1
            html.append('<ul>' + ''.join(items) + '</ul>')
        elif re.match(r'^\s*\d+\.\s', line):
            items = []
            while i < len(lines) and re.match(r'^\s*\d+\.\s', lines[i]):
                items.append(f'<li>{inline(re.sub(r"^\s*\d+\.\s", "", lines[i]).strip())}</li>')
                i += 1
            html.append('<ol>' + ''.join(items) + '</ol>')
        elif line.startswith('>'):
            q = []
            while i < len(lines) and lines[i].startswith('>'):
                q.append(inline(lines[i][1:].strip()))
                i += 1
            html.append(f'<blockquote>{" ".join(q)}</blockquote>')
        elif line.strip() == '☒' or line.strip().startswith('☐') or line.strip().startswith('☒'):
            html.append(f'<p>{inline(line)}</p>')
        else:
            html.append(f'<p>{inline(line)}</p>')
        i += 1
    return '\n'.join(html)


def _table(lines, i):
    header = lines[i]
    i += 1
    sep = lines[i] if i < len(lines) else ''
    i += 1 if i < len(lines) and set(sep.replace('|', '').replace('-', '').replace(':', '').strip()) == set() else 0
    rows = []
    while i < len(lines) and lines[i].startswith('|'):
        rows.append(lines[i])
        i += 1
    cells = [c.strip() for c in header.strip('|').split('|')]
    h = '<tr>' + ''.join(f'<th>{inline(c)}</th>' for c in cells) + '</tr>'
    body = ''
    for r in rows:
        cs = [c.strip() for c in r.strip('|').split('|')]
        body += '<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in cs) + '</tr>'
    return '<table>' + h + body + '</table>', i


def to_pdf(md_path, out_pdf):
    md = Path(md_path).read_text(encoding='utf-8')
    body = convert(md)
    title = md.splitlines()[0].lstrip('# ').strip()
    html = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8">
<title>{title}</title>
<style>
  body {{ font-family: 'DejaVu Sans', Arial, sans-serif; color: #1a1a2e; font-size: 11px; line-height: 1.55; }}
  h1 {{ font-size: 17px; color: #16213e; border-bottom: 3px solid #e94560; padding-bottom: 6px; }}
  h2 {{ font-size: 13px; color: #e94560; border-bottom: 1px solid #ddd; padding-bottom: 3px; margin-top: 18px; }}
  h3 {{ font-size: 11.5px; color: #16213e; margin-top: 12px; }}
  table {{ width: 100%; border-collapse: collapse; margin: 8px 0; }}
  th {{ background: #16213e; color: #fff; padding: 5px 7px; text-align: left; font-size: 10px; }}
  td {{ border: 1px solid #ccc; padding: 5px 7px; vertical-align: top; font-size: 10px; }}
  tr:nth-child(even) td {{ background: #f7f8fa; }}
  ul, ol {{ margin: 6px 0 6px 18px; }}
  li {{ margin: 3px 0; }}
  blockquote {{ border-left: 3px solid #e94560; background: #fff9f9; padding: 6px 12px; margin: 8px 0; }}
  code {{ background: #f0f2f5; padding: 1px 4px; border-radius: 3px; }}
  hr {{ border: none; border-top: 2px solid #16213e; margin: 18px 0; }}
</style></head><body>
{body}
</body></html>"""
    tmp = Path('/tmp/opencode') / (out_pdf.stem + '.html')
    tmp.write_text(html, encoding='utf-8')
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', str(tmp),
                    '--outdir', str(out_pdf.parent)], check=True)
    print('PDF généré :', out_pdf)


if __name__ == '__main__':
    name = sys.argv[1]
    md = BASE / 'livrables' / name
    pdf = md.with_suffix('.pdf')
    to_pdf(md, pdf)
