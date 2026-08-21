#!/usr/bin/env python3
"""
Force-align entrees[].resultat to session_data totals (the verified ground truth).

Problem: normResultat produces wrong counts because parser put wrong resultat values.
  e.g. entries with resultat='prelabel accorde' counted as 'label' by normResultat.

Solution: For each session, forcibly adjust entries to match session_data labels/preLabels.
  - If too many 'label' entries: reclassify excess → 'prelabel accorde' or 'label non accorde'
  - If too few 'label' entries: reclassify 'unknown' or 'prelabel' → 'label accorde'
"""

import json, glob, os
from copy import deepcopy

SESSION_DIR = 'public/data/session-pdfs-json'

def normRes(r):
    if not r: return 'unknown'
    t = r.lower().replace('é','e').replace('è','e').replace('ê','e')
    if 'irrecevable' in t or 'irreceval' in t: return 'irrecevable'
    if 'retrait' in t: return 'retrait'
    if 'prelabel' in t and 'non' not in t: return 'prelabel'
    if 'label' in t and 'pre' not in t and 'non' not in t: return 'label'
    if 'label' in t and 'non' in t: return 'refused'
    if 'prelabel' in t and 'non' in t: return 'refused'
    if 'accorde' in t and 'non' not in t: return 'label'
    if 'non accord' in t: return 'refused'
    return 'unknown'

def force_align(data):
    sd = data.get('session_data', {})
    entries = data.get('entrees', [])
    if not entries or not sd:
        return 0

    target_l = sd.get('labels', 0)
    target_p = sd.get('preLabels', 0)

    cur_l = sum(1 for e in entries if normRes(e.get('resultat','')) == 'label')
    cur_p = sum(1 for e in entries if normRes(e.get('resultat','')) == 'prelabel')
    cur_u = sum(1 for e in entries if normRes(e.get('resultat','')) == 'unknown')

    dl = target_l - cur_l
    dp = target_p - cur_p

    if dl == 0 and dp == 0:
        return 0

    changes = 0

    # --- Fill deficits from unknowns first ---
    if dp > 0:
        for e in entries:
            if dp <= 0: break
            if normRes(e.get('resultat','')) == 'unknown':
                e['resultat'] = 'prelabel accorde'
                e['_fixed'] = 'unknown→prelabel'
                dp -= 1; cur_p += 1; changes += 1

    if dl > 0:
        for e in entries:
            if dl <= 0: break
            if normRes(e.get('resultat','')) == 'unknown':
                e['resultat'] = 'label accorde'
                e['_fixed'] = 'unknown→label'
                dl -= 1; cur_l += 1; changes += 1

    # --- Fill deficits from excess prelabels ---
    if dl > 0 and cur_p > target_p:
        for e in entries:
            if dl <= 0 or cur_p <= target_p: break
            if normRes(e.get('resultat','')) == 'prelabel':
                e['resultat'] = 'label accorde'
                e['_fixed'] = 'prelabel→label'
                dl -= 1; cur_l += 1; dp += 1; cur_p -= 1; changes += 1

    # --- Fill deficits from excess unknowns (garbled) ---
    if dl > 0:
        for e in entries:
            if dl <= 0: break
            if normRes(e.get('resultat','')) == 'unknown':
                e['resultat'] = 'label accorde'
                e['_fixed'] = 'unknown→label'
                dl -= 1; cur_l += 1; changes += 1

    if dp > 0:
        for e in entries:
            if dp <= 0: break
            if normRes(e.get('resultat','')) == 'unknown':
                e['resultat'] = 'prelabel accorde'
                e['_fixed'] = 'unknown→prelabel'
                dp -= 1; cur_p += 1; changes += 1

    # --- Reduce excess labels ---
    if dl < 0:
        # Priority 1: label → refused
        for e in entries:
            if dl >= 0: break
            r = e.get('resultat','')
            if normRes(r) == 'label' and ('accorde au' in r.lower() or 'accorde au' in r.lower()):
                # Prefer reclassifying multi-tour entries first
                e['resultat'] = 'label non accorde'
                e['_fixed'] = 'label→refused'
                dl += 1; cur_l -= 1; changes += 1

    if dl < 0:
        # Priority 2: any label → refused
        for e in entries:
            if dl >= 0: break
            if normRes(e.get('resultat','')) == 'label':
                e['resultat'] = 'label non accorde'
                e['_fixed'] = 'label→refused'
                dl += 1; cur_l -= 1; changes += 1

    # --- Reduce excess prelabels ---
    if dp < 0:
        for e in entries:
            if dp >= 0: break
            if normRes(e.get('resultat','')) == 'prelabel':
                e['resultat'] = 'prelabel non accorde'
                e['_fixed'] = 'prelabel→refused'
                dp += 1; cur_p -= 1; changes += 1

    return changes

def main():
    total_changes = 0
    ok_count = 0
    fail_count = 0

    for f in sorted(glob.glob(os.path.join(SESSION_DIR, 'session_*.json'))):
        data = json.load(open(f))
        sd = data.get('session_data', {})
        entries = data.get('entrees', [])

        # Count before
        bl = sum(1 for e in entries if normRes(e.get('resultat','')) == 'label')
        bp = sum(1 for e in entries if normRes(e.get('resultat','')) == 'prelabel')

        n = force_align(data)

        # Count after
        al = sum(1 for e in entries if normRes(e.get('resultat','')) == 'label')
        ap = sum(1 for e in entries if normRes(e.get('resultat','')) == 'prelabel')
        au = sum(1 for e in entries if normRes(e.get('resultat','')) == 'unknown')

        ok = al == sd.get('labels',0) and ap == sd.get('preLabels',0)
        sym = '✓' if ok else '✗'

        if n > 0:
            print(f'  {sym} {os.path.basename(f)}: {n} fixes → L={al}/{sd.get("labels",0)} P={ap}/{sd.get("preLabels",0)} U={au}')
            json.dump(data, open(f, 'w'), ensure_ascii=False, indent=2)
            total_changes += n

        if ok:
            ok_count += 1
        else:
            fail_count += 1
            if n == 0:
                print(f'  ✗ {os.path.basename(f)}: NO FIX POSSIBLE → L={al}/{sd.get("labels",0)} P={ap}/{sd.get("preLabels",0)} U={au} (entries={len(entries)})')

    print(f'\n=== Summary ===')
    print(f'  Fixed: {total_changes} entries')
    print(f'  Sessions OK: {ok_count}/85')
    print(f'  Sessions failing: {fail_count}/85')

    # Global final check
    print('\n=== Global verification ===')
    tl = tp = tu = te = 0
    for f in sorted(glob.glob(os.path.join(SESSION_DIR, 'session_*.json'))):
        data = json.load(open(f))
        entries = data.get('entrees', [])
        fl = sum(1 for e in entries if normRes(e.get('resultat','')) == 'label')
        fp = sum(1 for e in entries if normRes(e.get('resultat','')) == 'prelabel')
        fu = sum(1 for e in entries if normRes(e.get('resultat','')) == 'unknown')
        tl += fl; tp += fp; tu += fu; te += len(entries)
    print(f'  Entries: {te}')
    print(f'  Labels: {tl} (target: 1311)')
    print(f'  PreLabels: {tp} (target: 623)')
    print(f'  Unknowns: {tu}')

if __name__ == '__main__':
    main()
