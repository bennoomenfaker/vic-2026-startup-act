#!/usr/bin/env python3
"""Convertit les livrables Office (docx/xlsx) en PDF pour l'aperçu intégré dans l'app.

- CHARTE DE CADRAGE DE Veille_ AE1- État des lieux quantitatif.docx  -> PDF (portrait)
- Plan de veille AE1- État des lieux quantitatif.xlsx                -> PDF (paysage, tableau 7 colonnes)

Le PDF paysage est généré via HTML (conversion LibreOffice writer), car l'export
Calc direct produit un tableau coupé/illisible sur 1 page portrait.
"""
import re
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
LIV = BASE / 'livrables'
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

DOCX = LIV / 'CHARTE DE CADRAGE DE Veille_ AE1- État des lieux quantitatif.docx'
XLSX = LIV / 'Plan de veille AE1- État des lieux quantitatif.xlsx'
PDF_DOCX = DOCX.with_suffix('.pdf')
PDF_XLSX = XLSX.with_suffix('.pdf')


def conv_docx_to_pdf():
    if not DOCX.exists():
        print('⚠ docx introuvable :', DOCX)
        return False
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', str(LIV), str(DOCX)],
                   check=True, capture_output=True)
    print('✅ PDF généré :', PDF_DOCX.name)
    return True


def read_shared_strings(z):
    try:
        root = ET.fromstring(z.read('xl/sharedStrings.xml'))
    except KeyError:
        return []
    out = []
    for si in root.findall('m:si', NS):
        out.append(''.join(t.text or '' for t in si.findall('.//m:t', NS)))
    return out


def read_sheet(z, shared):
    name = next(n for n in z.namelist() if re.match(r'xl/worksheets/sheet\d+\.xml$', n))
    root = ET.fromstring(z.read(name))
    rows = []
    for row in root.findall('.//m:sheetData/m:row', NS):
        cells = {}
        for c in row.findall('m:c', NS):
            col = re.match(r'([A-Z]+)', c.get('r', 'A')).group(1)
            t = c.get('t', '')
            v = c.find('m:v', NS)
            inline = c.find('m:is', NS)
            val = ''
            if t == 's' and v is not None:
                val = shared[int(v.text)]
            elif t == 'str' and v is not None:
                val = v.text or ''
            elif t == 'inlineStr' and inline is not None:
                val = ''.join(x.text or '' for x in inline.findall('.//m:t', NS))
            elif v is not None:
                val = v.text or ''
            cells[col] = val
        cols = sorted(cells.keys(), key=lambda x: (len(x), x))
        rows.append([cells.get(c, '') for c in cols])
    return rows


def esc(text):
    return (text or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def conv_xlsx_to_pdf():
    if not XLSX.exists():
        print('⚠ xlsx introuvable :', XLSX)
        return False
    with zipfile.ZipFile(XLSX) as z:
        shared = read_shared_strings(z)
        rows = read_sheet(z, shared)

    body = []
    first_data = True
    for row in rows:
        non_empty = [c for c in row if c.strip()]
        if len(non_empty) <= 1:
            txt = esc(non_empty[0]) if non_empty else ''
            cls = 'title' if first_data else 'sub'
            body.append(f'<p class="{cls}">{txt}</p>')
            continue
        if first_data:
            first_data = False
            body.append('<tr>' + ''.join(f'<th class="c{i}">{esc(c)}</th>' for i, c in enumerate(row[:7])) + '</tr>')
            continue
        cells = (row + [''] * 7)[:7]
        body.append('<tr>' + ''.join(
            f'<td class="c{i}">{"<b>" + esc(c) + "</b>" if i == 0 else esc(c)}</td>'
            for i, c in enumerate(cells)) + '</tr>')

    html = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8">
<title>Plan de veille AE1 — État des lieux quantitatif</title>
<style>
  @page {{ size: A4 landscape; margin: 1.1cm 1.3cm; }}
  body {{ font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 10px; color: #1a1a2e; line-height: 1.4; }}
  p.title {{ font-size: 15px; font-weight: bold; color: #16213e; margin: 0 0 6px; }}
  p.sub {{ font-size: 9.5px; font-style: italic; color: #666; margin: 0 0 4px; }}
  table {{ width: 100%; border-collapse: collapse; table-layout: fixed; margin-top: 8px; }}
  th {{ background: #16213e; color: #fff; padding: 6px 8px; text-align: left; font-size: 8.5px; }}
  td {{ border: 1px solid #c3c9d4; padding: 6px 8px; vertical-align: top; font-size: 8.5px; word-wrap: break-word; }}
  th.c0, td.c0 {{ font-weight: bold; width: 12%; }}
  th.c1, td.c1 {{ width: 17%; }}
  th.c2, td.c2 {{ width: 16%; }}
  th.c3, td.c3 {{ width: 17%; }}
  th.c4, td.c4 {{ width: 13%; }}
  th.c5, td.c5 {{ width: 12%; }}
  th.c6, td.c6 {{ width: 13%; }}
  tr:nth-child(even) td {{ background: #f6f8fb; }}
</style></head><body>
{''.join(body)}
</body></html>"""

    tmp = Path('/tmp/opencode')
    tmp.mkdir(exist_ok=True)
    tmp_html = tmp / (PDF_XLSX.stem + '.html')
    tmp_html.write_text(html, encoding='utf-8')
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', str(tmp_html),
                    '--outdir', str(LIV)], check=True, capture_output=True)
    print('✅ PDF généré :', PDF_XLSX.name)
    return True


if __name__ == '__main__':
    ok = True
    if '--docx' in sys.argv or '--all' in sys.argv or len(sys.argv) == 1:
        ok &= conv_docx_to_pdf()
    if '--xlsx' in sys.argv or '--all' in sys.argv or len(sys.argv) == 1:
        ok &= conv_xlsx_to_pdf()
    print('Terminé.' if ok else 'Erreur lors de la conversion.')
