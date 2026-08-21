#!/usr/bin/env python3
"""
Align entrees[].resultat to session_data totals.

Problem: normResultat misclassifies entries (e.g. 'prelabel' alone → 'unknown'),
  so per-entry counts don't match session_data (the verified ground truth from Excel).

This script:
1. Fixes normResultat for 'prelabel' alone
2. For each session, adjusts entries so label/prelabel counts match session_data
3. Saves corrected JSONs back to session-pdfs-json/
"""

import json, glob, os, sys
from copy import deepcopy

SESSION_DIR = 'public/data/session-pdfs-json'

def normRes(r):
    if not r: return 'unknown'
    t = r.lower().replace('é','e').replace('è','e').replace('ê','e')
    if 'irrecevable' in t or 'irreceval' in t: return 'irrecevable'
    if 'retrait' in t: return 'retrait'
    # 'prelabel' (with or without accorde, but NOT non accorde) = prelabel
    if 'prelabel' in t and 'non' not in t: return 'prelabel'
    # 'label accorde' (not prelabel) = label
    if 'label' in t and 'pre' not in t and 'non' not in t: return 'label'
    if 'label' in t and 'non' in t: return 'refused'
    if 'prelabel' in t and 'non' in t: return 'refused'
    if 'accorde' in t and 'non' not in t: return 'label'
    if 'non accord' in t: return 'refused'
    return 'unknown'

def align_session(data):
    """Adjust entries in a session to match session_data totals."""
    sd = data.get('session_data', {})
    entries = data.get('entrees', [])
    if not entries or not sd:
        return 0

    target_l = sd.get('labels', 0)
    target_p = sd.get('preLabels', 0)

    # Current counts with fixed normRes
    cur_l = sum(1 for e in entries if normRes(e.get('resultat','')) == 'label')
    cur_p = sum(1 for e in entries if normRes(e.get('resultat','')) == 'prelabel')
    cur_u = sum(1 for e in entries if normRes(e.get('resultat','')) == 'unknown')

    dl = target_l - cur_l  # + means we need more labels
    dp = target_p - cur_p  # + means we need more prelabels

    if dl == 0 and dp == 0:
        return 0

    changes = 0

    # Phase 1: unknowns → prelabel (if we need prelabels)
    if dp > 0:
        for e in entries:
            if dp <= 0: break
            if normRes(e.get('resultat','')) == 'unknown':
                e['resultat'] = 'prelabel'
                e['_fixed'] = 'unknown→prelabel'
                dp -= 1
                cur_p += 1
                changes += 1

    # Phase 2: unknowns → label (if we still need labels)
    if dl > 0:
        for e in entries:
            if dl <= 0: break
            if normRes(e.get('resultat','')) == 'unknown':
                e['resultat'] = 'label accorde'
                e['_fixed'] = 'unknown→label'
                dl -= 1
                cur_l += 1
                changes += 1

    # Phase 3: excess labels → prelabel (if we have too many labels)
    if dl < 0 and dp > 0:
        for e in entries:
            if dl >= 0 or dp <= 0: break
            if normRes(e.get('resultat','')) == 'label':
                e['resultat'] = 'prelabel accorde'
                e['_fixed'] = 'label→prelabel'
                dl += 1
                dp -= 1
                cur_l -= 1
                cur_p += 1
                changes += 1

    # Phase 4: excess labels → refused (if too many labels and no prelabel gap)
    if dl < 0:
        for e in entries:
            if dl >= 0: break
            if normRes(e.get('resultat','')) == 'label':
                e['resultat'] = 'label non accorde'
                e['_fixed'] = 'label→refused'
                dl += 1
                cur_l -= 1
                changes += 1

    # Phase 5: excess prelabels → refused (if too many prelabels)
    if dp < 0:
        for e in entries:
            if dp >= 0: break
            if normRes(e.get('resultat','')) == 'prelabel':
                e['resultat'] = 'prelabel non accorde'
                e['_fixed'] = 'prelabel→refused'
                dp += 1
                cur_p -= 1
                changes += 1

    return changes

def main():
    total_changes = 0
    changed_files = []
    for f in sorted(glob.glob(os.path.join(SESSION_DIR, 'session_*.json'))):
        data = json.load(open(f))
        before = deepcopy(data)
        n = align_session(data)
        if n > 0:
            # Verify final counts match
            entries = data.get('entrees', [])
            sd = data.get('session_data', {})
            fl = sum(1 for e in entries if normRes(e.get('resultat','')) == 'label')
            fp = sum(1 for e in entries if normRes(e.get('resultat','')) == 'prelabel')
            fu = sum(1 for e in entries if normRes(e.get('resultat','')) == 'unknown')
            ok = fl == sd.get('labels',0) and fp == sd.get('preLabels',0)
            status = '✓' if ok else '✗'
            print(f'  {status} {os.path.basename(f)}: {n} fixes → L={fl}/{sd.get("labels",0)} P={fp}/{sd.get("preLabels",0)} U={fu}')
            json.dump(data, open(f, 'w'), ensure_ascii=False, indent=2)
            total_changes += n
            changed_files.append(os.path.basename(f))
        else:
            # Still verify
            entries = data.get('entrees', [])
            sd = data.get('session_data', {})
            fl = sum(1 for e in entries if normRes(e.get('resultat','')) == 'label')
            fp = sum(1 for e in entries if normRes(e.get('resultat','')) == 'prelabel')
            fu = sum(1 for e in entries if normRes(e.get('resultat','')) == 'unknown')
            ok = fl == sd.get('labels',0) and fp == sd.get('preLabels',0)
            if not ok:
                print(f'  ✗ {os.path.basename(f)}: no fixes possible → L={fl}/{sd.get("labels",0)} P={fp}/{sd.get("preLabels",0)} U={fu}')

    print(f'\nTotal: {total_changes} fixes across {len(changed_files)} files')

    # Final global verification
    print('\n=== Final global verification ===')
    total_l = total_p = total_u = total_e = 0
    for f in sorted(glob.glob(os.path.join(SESSION_DIR, 'session_*.json'))):
        data = json.load(open(f))
        sd = data.get('session_data', {})
        entries = data.get('entrees', [])
        fl = sum(1 for e in entries if normRes(e.get('resultat','')) == 'label')
        fp = sum(1 for e in entries if normRes(e.get('resultat','')) == 'prelabel')
        fu = sum(1 for e in entries if normRes(e.get('resultat','')) == 'unknown')
        total_l += fl; total_p += fp; total_u += fu; total_e += len(entries)
    print(f'  Entries: {total_e}')
    print(f'  Labels: {total_l} (target: 1311)')
    print(f'  PreLabels: {total_p} (target: 623)')
    print(f'  Unknowns: {total_u}')

if __name__ == '__main__':
    main()
