"""Correct the per-session reconciliation lines for S86-S88.

Bug found 29/08/2026: the per-session reconciliation (`reconciliation88[].pdf_detail`)
under-counted the physical PDF lines for the three 2026 sessions it drives (04/05/06
2026): 47/42/45 instead of the true entry totals 50/48/47. The header total
(3 571 lines PDF, sum of all session entries) was correct, so a reader adding the
per-session "Lignes PDF" column found 3 560 instead of 3 571.

Root cause: these three blocks were built before all their entries were aligned in the
source session JSONs, and they merged the `conversion` (Prélabel -> Label) entries into
the wrong category buckets. There is no checked-in generator for `reconciliation88`;
it is a static artifact, so this script corrects the three blocks directly from the
source session JSONs, using the exact convention already proven correct on the 01-03/2026
sessions (which are left untouched).

Usage:  python3 scripts/reconciliation/fix_reconciliation_2026_lignes.py
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / 'public' / 'data'
CORRECTIONS = DATA / 'corrections.json'
SESSION_JSON_DIR = DATA / 'session-pdfs-json'

TARGET_SESSION_IDS = {'S85', 'S86', 'S87'}  # 04/2026, 05/2026, 06/2026


def recompute_pdf_detail(entries):
    labels = labels_na = prelabels = prelabels_na = retraits = reportes = dec_na = pitch = 0
    total = 0
    for e in entries:
        res = e.get('resultat_normalise')
        total += 1
        if res == 'Label accordé':
            labels += 1
        elif res == 'Prélabel accordé':
            prelabels += 1
        elif res == 'Label non accordé':
            labels_na += 1
        elif res == 'Prélabel non accordé':
            prelabels_na += 1
        elif res == 'Retrait Label':
            retraits += 1
        elif res == 'Reporté':
            reportes += 1
        elif res == 'Décision non précisée — motif administratif':
            dec_na += 1
        elif res == 'Pitch décalé':
            pitch += 1
    categories = {
        'Label accordé': labels,
        'Label non accordé': labels_na,
        'Prélabel accordé': prelabels,
        'Prélabel non accordé': prelabels_na,
        'Retrait Label': retraits,
    }
    if categories['Retrait Label'] == 0:
        del categories['Retrait Label']
    if reportes:
        categories['Reporté'] = reportes
    if dec_na:
        categories['Décision non précisée — motif administratif'] = dec_na
    if pitch:
        categories['Pitch décalé'] = pitch
    return {
        'categories': categories,
        'decisionsNonPrecisees': dec_na,
        'labels': labels,
        'labelsNonAccordes': labels_na,
        'lignes': total,
        'pitchDecales': pitch,
        'preLabels': prelabels,
        'preLabelsNonAccordes': prelabels_na,
        'reportes': reportes,
        'retraits': retraits,
    }


def main():
    data = json.loads(CORRECTIONS.read_text(encoding='utf-8'))
    recs = data.get('reconciliation88', [])
    changed = 0
    for r in recs:
        if r.get('session_id') not in TARGET_SESSION_IDS:
            continue
        # Normalise the file name: session field is "MM/YYYY".
        month, year = r['session'].split('/')
        path = SESSION_JSON_DIR / f"session_{year}_{month}.json"
        if not path.exists():
            print('  SKIP (no source JSON):', r['session'])
            continue
        session = json.loads(path.read_text(encoding='utf-8'))
        entries = session.get('entrees', [])
        new_pd = recompute_pdf_detail(entries)

        official = r.get('official', {})
        off_cand = official.get('candidatures', 0)
        off_labels = official.get('labels', 0)
        off_prelabels = official.get('preLabels', 0)

        r['pdf_detail'] = new_pd

        cc = r.setdefault('corrected_counter', {})
        # Only the candidatures (physical line) count was wrong. The labels and
        # preLabels series are a SEPARATE corrected-Label series (sum = 1 343) that
        # must be preserved unchanged — do NOT derive them from the raw result bucket.
        cc['candidatures'] = new_pd['lignes']
        cc['candidatures_officielles_reprises'] = official.get(
            'candidatures', cc.get('candidatures_officielles_reprises', 0))
        cc['candidatures_source'] = 'lignes PDF détaillées, méthode corrigée de l’étude'
        cc['source'] = ('candidatures corrigées depuis les lignes PDF (fix 29/08/2026) : '
                        f"{new_pd['lignes']} lignes physiques dont "
                        f"{new_pd['retraits']} retraits documentés; labels/prélabels "
                        "série corrigée conservée telle quelle (total 1 343)")

        ec = r.setdefault('ecarts', {})
        ec['candidatures_corrigees_moins_officiel'] = new_pd['lignes'] - off_cand
        # labels/prélabels ecarts unchanged (their series is preserved)
        ec.setdefault('corrige_moins_officiel_labels',
                      cc.get('labels', 0) - off_labels)
        ec.setdefault('corrige_moins_officiel_preLabels',
                      cc.get('preLabels', 0) - off_prelabels)
        ec['lignes_moins_officiel'] = new_pd['lignes'] - off_cand

        changed += 1
        print(f"  fixed {r['session']} ({r['session_id']}): lignes -> {new_pd['lignes']}")

    # Keep the raw-PDF classification manifest (meta.pdfDetailTotals88) coherent
    # with the corrected per-session pdf_detail blocks. This is the raw-PDF bucket
    # series (labels here are ~1 233), NOT the corrected-Label series (1 343).
    agg = {k: 0 for k in (
        'Décision non précisée — motif administratif', 'Label accordé',
        'Label non accordé', 'Pitch décalé', 'Prélabel accordé',
        'Prélabel non accordé', 'Reporté', 'Retrait Label')}
    lignes = 0
    for r in recs:
        pd = r.get('pdf_detail', {})
        lignes += pd.get('lignes', 0)
        for k, v in pd.get('categories', {}).items():
            agg[k] = agg.get(k, 0) + v
    data['meta']['pdfDetailTotals88'] = {
        'lignes': lignes,
        'categories': agg,
        'labels': agg['Label accordé'],
        'preLabels': agg['Prélabel accordé'],
        'labelsNonAccordes': agg['Label non accordé'],
        'preLabelsNonAccordes': agg['Prélabel non accordé'],
        'retraits': agg['Retrait Label'],
        'reportes': agg['Reporté'],
        'decisionsNonPrecisees': agg['Décision non précisée — motif administratif'],
        'pitchDecales': agg['Pitch décalé'],
    }

    CORRECTIONS.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"FIXED_SESSIONS {changed}; pdfDetailTotals88.lignes re-synced to {lignes}")


if __name__ == '__main__':
    main()
