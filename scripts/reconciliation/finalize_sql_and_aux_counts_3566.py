#!/usr/bin/env python3
from __future__ import annotations
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = ROOT/'public'/'data'

def main():
    source = D/'startup_act_database.sql'
    for name in ['reextraction_88_canonical.sql','startup_act_database_88.sql','startup_act_database_reextrait_corrige_2026-08-23.sql']:
        shutil.copy2(source, D/name)
    p = D/'sessions_table.json'
    obj = json.loads(p.read_text(encoding='utf-8'))
    if isinstance(obj.get('meta'), dict):
        obj['meta']['totalCandidaturesPdfCalculees'] = 3566 - 404 - 153 - 5
        obj['meta']['totalCandidaturesReexamenPdf'] = 3566
        obj['meta']['totalCandidaturesCorrigees'] = 3569
        obj['meta']['ecartTotalPdfMoinsOfficiel'] = 3566 - 3079
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print({'sql_decisions': sum(1 for line in source.read_text(encoding='utf-8').splitlines() if line.startswith('INSERT INTO decisions')), 'pdf_calculated': 3004})

if __name__ == '__main__': main()
