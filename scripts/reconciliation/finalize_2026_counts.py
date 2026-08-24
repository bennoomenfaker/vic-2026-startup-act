#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'public' / 'data'
CANONICAL = DATA / 'reextraction_88_canonical.json'
TARGETS = {'04/2026': 50, '05/2026': 48, '06/2026': 47}


def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p, v): p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    c = load(CANONICAL)
    for s in c['sessions']:
        if s.get('session') in TARGETS:
            actual = sum(1 for e in c['entries'] if e.get('session') == s['session'])
            assert actual == TARGETS[s['session']], (s['session'], actual)
            s['entries'] = actual
    c['meta']['detailed_entries'] = len(c['entries'])
    c['meta']['detailedEntries'] = len(c['entries'])
    dump(CANONICAL, c)

    for p in [DATA/'sessions_88.json', DATA/'startup_act_88_sessions.json', DATA/'sessions_table.json']:
        if not p.exists(): continue
        obj = load(p)
        rows = obj.get('sessions') if isinstance(obj, dict) else obj
        if not isinstance(rows, list): continue
        for row in rows:
            period = row.get('session')
            if period in TARGETS:
                row['entries'] = TARGETS[period]
                row['entries_detaillees'] = TARGETS[period]
                row['candidatures_reexamen_pdf'] = TARGETS[period]
                row['candidatures_corrigees'] = TARGETS[period] + int(row.get('ajournes_hors_pdf') or row.get('ajournes') or 0)
        if isinstance(obj, dict) and isinstance(obj.get('meta'), dict):
            m = obj['meta']
            for k in ('totalCandidaturesReexamenPdf','detailedEntries','detailed_entries'):
                if k in m: m[k] = len(c['entries'])
            if 'totalCandidaturesCorrigees' in m: m['totalCandidaturesCorrigees'] = len(c['entries']) + 3
            if 'ecartTotalPdfMoinsOfficiel' in m: m['ecartTotalPdfMoinsOfficiel'] = len(c['entries']) - 3079
        dump(p, obj)
    print({'total_entries': len(c['entries']), 'session_counts': TARGETS, 'corrected_with_ajournes': len(c['entries']) + 3})

if __name__ == '__main__': main()
