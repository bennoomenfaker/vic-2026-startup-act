#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = ROOT/'public'/'data'


def main():
    c = json.loads((D/'reextraction_88_canonical.json').read_text(encoding='utf-8'))
    counts = {}
    for e in c['entries']:
        counts[e.get('resultat_normalise')] = counts.get(e.get('resultat_normalise'), 0) + 1
    p = D/'dashboard_data.json'
    obj = json.loads(p.read_text(encoding='utf-8'))
    meta = obj.setdefault('meta', {})
    for k, v in {
        'detailedEntries': len(c['entries']),
        'totalLignesPdf': len(c['entries']),
        'totalCandidaturesCorrigees': len(c['entries']) + 3,
        'correctedCandidatures': len(c['entries']) + 3,
        'totalLabelsPdfDetail': counts.get('Label accordé', 0),
        'totalPreLabelsPdfDetail': counts.get('Prélabel accordé', 0) + counts.get('Prélabel non accordé', 0),
        'ajournesHorsPdf': 3,
    }.items(): meta[k] = v
    meta['dataNote'] = '3 569 candidatures corrigées = 3 566 lignes PDF + 3 ajournés hors PDF ; 3 079 candidatures officielles conservées séparément.'
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print({'detailedEntries': len(c['entries']), 'corrected': len(c['entries'])+3, 'label_detail': counts.get('Label accordé',0), 'prelabel_detail_total': counts.get('Prélabel accordé',0)+counts.get('Prélabel non accordé',0)})

if __name__ == '__main__': main()
