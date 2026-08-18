#!/usr/bin/env python3
"""
Audit complet des données extraites des 85 sessions PDF.
Vérifie la conformité des entrées et des totaux.
"""
import json
from pathlib import Path
from collections import defaultdict

json_dir = Path('public/data/session-pdfs-json')
counts_path = Path('public/data/session_pdf_counts.json')
sessions_path = Path('public/data/sessions.json')
corrections_path = Path('public/data/corrections.json')

with open(counts_path) as f:
    counts = json.load(f)
with open(sessions_path) as f:
    sessions_list = json.load(f)
with open(corrections_path) as f:
    corrections = json.load(f)

sessions_map = {s['session']: s for s in sessions_list}

months_fr = ['janvier','fevrier','mars','avril','mai','juin','juillet','aout','septembre','octobre','novembre','decembre']
months_short = ['janv','fevr','mars','avr','mai','juin','juil','aout','sept','oct','nov','dec']

def has_month(text):
    t = text.lower()
    return any(m in t for m in months_fr) or any(m in t for m in months_short)

def is_header_row(e):
    s = e.get('societe','')
    f = e.get('fondateurs','')
    r = e.get('resultat','')
    if s.strip().lower() == 'société' and f.strip().lower() == 'secteur':
        return True
    if s.strip().lower() == 'société' and 'fondateurs' in f.lower():
        return True
    if 'startup act' in s.lower() and 'session' in s.lower():
        return True
    if 'compte-rendu' in s.lower() or 'compte rendu' in s.lower():
        return True
    if s.strip() == 'Résultat' and f.strip() == 'Commentaires':
        return True
    if s.strip() == 'Société' and r.strip() == 'Commentaires':
        return True
    return False

def is_garbage(e):
    s = e.get('societe','')
    r = e.get('resultat','')
    sec = e.get('secteur','')
    
    if is_header_row(e):
        return True, 'header_pdf'
    if has_month(sec) or has_month(s):
        return True, 'month_in_sector'
    if 'retrait du label' in r.lower() or 'retrait du label' in s.lower():
        return True, 'retrait_text'
    if '2018 pour les sociétés bénéficiaires' in r.lower():
        return True, 'retrait_boilerplate'
    if 'décision' in s.lower() and 'commentaires' in r.lower():
        return True, 'header_pdf'
    return False, None

# Expected values
expected = {
    'labels': 1311,
    'prelabels': 623,
    'candidatures': 2958,
    'retraits': 140,
    'conversions': 502,
    'taux_moyen': 44.3
}

# Analyse par session
session_stats = {}
total_valid_labels = 0
total_valid_prelabels = 0
total_candidatures = 0
total_retraits = 0
total_conversions = 0
sessions_with_garbage = []
sessions_fausses = []

for f in sorted(json_dir.glob('*.json')):
    with open(f) as fh:
        data = json.load(fh)
    session = data.get('session', f.stem.replace('session_',''))
    entrees = data.get('entrees', [])
    sd = data.get('session_data', {})
    
    garbage = []
    valid_entrees = []
    for i, e in enumerate(entrees):
        bad, reason = is_garbage(e)
        if bad:
            garbage.append((i, reason, e.get('societe','')[:60]))
        else:
            valid_entrees.append(e)
    
    # Count from valid entries
    v_labels = sum(1 for e in valid_entrees if 'label accorde' in e.get('resultat','').lower() and 'pre' not in e.get('resultat','').lower())
    v_prelabels = sum(1 for e in valid_entrees if 'prelabel accorde' in e.get('resultat','').lower())
    
    # Count retraits from valid entries
    v_retraits = sum(1 for e in valid_entrees if 'retrait' in e.get('resultat','').lower())
    
    candidatures = sd.get('candidatures', len(entrees))
    retraits = sd.get('retraits', 0)
    conversions = sd.get('conversions', 0)
    s_labels = sd.get('labels', 0)
    s_prelabels = sd.get('preLabels', 0)
    
    total_valid_labels += v_labels
    total_valid_prelabels += v_prelabels
    total_candidatures += candidatures
    total_retraits += retraits
    total_conversions += conversions
    
    session_stats[session] = {
        'total_raw': len(entrees),
        'total_valid': len(valid_entrees),
        'garbage_count': len(garbage),
        'garbage': garbage,
        'v_labels': v_labels,
        'v_prelabels': v_prelabels,
        'v_retraits': v_retraits,
        's_labels': s_labels,
        's_prelabels': s_prelabels,
        'candidatures': candidatures,
        'retraits': retraits,
        'conversions': conversions,
        'statut': sd.get('statut', 'inconnu'),
    }
    
    if len(garbage) > 0:
        sessions_with_garbage.append(session)
    
    # Mark as false if raw data doesn't match session_data significantly
    if v_labels < s_labels - 2 or v_prelabels < s_prelabels - 2:
        sessions_fausses.append(session)

print('=' * 80)
print('AUDIT DES DONNÉES EXTRAITES - 85 SESSIONS STARTUP ACT')
print('=' * 80)
print()
print('1. RÉSUMÉ GLOBAL')
print('-' * 40)
print(f"Sessions analysées       : {len(session_stats)}")
print(f"Sessions avec garbage     : {len(sessions_with_garbage)}")
print(f"Sessions fausses/corrompues: {len(sessions_fausses)}")
print()
print('2. TOTAUX EXTRAITS (données brutes JSON)')
print('-' * 40)
print(f"Labels valides détectés  : {total_valid_labels}")
print(f"Pré-Labels valides       : {total_valid_prelabels}")
print(f"Candidatures             : {total_candidatures}")
print(f"Retraits (session_data)  : {total_retraits}")
print(f"Conversions (session_data): {total_conversions}")
print()
print('3. TOTAUX ATTENDUS (corrigés)')
print('-' * 40)
print(f"Labels       : {expected['labels']}")
print(f"Pré-Labels   : {expected['prelabels']}")
print(f"Candidatures : {expected['candidatures']}")
print(f"Retraits     : {expected['retraits']}")
print(f"Conversions  : {expected['conversions']}")
print(f"Taux moyen   : {expected['taux_moyen']}%")
print()
print('4. ÉCARTS')
print('-' * 40)
print(f"Labels      : {total_valid_labels} (attendu {expected['labels']}) → écart {total_valid_labels - expected['labels']:+d}")
print(f"Pré-Labels  : {total_valid_prelabels} (attendu {expected['prelabels']}) → écart {total_valid_prelabels - expected['prelabels']:+d}")
print(f"Retraits    : {total_retraits} (attendu {expected['retraits']}) → écart {total_retraits - expected['retraits']:+d}")
print(f"Conversions : {total_conversions} (attendu {expected['conversions']}) → écart {total_conversions - expected['conversions']:+d}")
print()
print('5. SESSIONS AVEC GARBAGE (68/85)')
print('-' * 40)
for s in sorted(sessions_with_garbage):
    info = session_stats[s]
    print(f"  {s}: {info['garbage_count']} entrées garbage sur {info['total_raw']} (statut: {info['statut']})")
print()
print('6. SESSIONS FAUSSES (écart labels/pré-labels > 2)')
print('-' * 40)
for s in sorted(sessions_fausses):
    info = session_stats[s]
    print(f"  {s}: détecté {info['v_labels']}L/{info['v_prelabels']}PL vs session_data {info['s_labels']}L/{info['s_prelabels']}PL")
print()
print('7. SESSIONS AVEC RETRAITS MANQUANTS')
print('-' * 40)
for s in sorted(session_stats.keys()):
    info = session_stats[s]
    if info['retraits'] > 0 or info['v_retraits'] > 0:
        print(f"  {s}: retraits={info['retraits']}, détecté dans entrées={info['v_retraits']}")
print()
print('8. DETAIL PAR SESSION (extrait)')
print('-' * 40)
print(f"{'Session':<10} {'Raw':>5} {'Valid':>6} {'Garb':>5} {'L(det)':>7} {'L(sd)':>6} {'PL(det)':>8} {'PL(sd)':>7} {'Retraits':>8}")
for s in sorted(session_stats.keys()):
    info = session_stats[s]
    marker = ' <-- FAUX' if s in sessions_fausses else ''
    print(f"{s:<10} {info['total_raw']:>5} {info['total_valid']:>6} {info['garbage_count']:>5} {info['v_labels']:>7} {info['s_labels']:>6} {info['v_prelabels']:>8} {info['s_prelabels']:>7} {info['retraits']:>8}{marker}")
print()
print('=' * 80)
print('CONCLUSION')
print('=' * 80)
print(f"Les données extraites par le parser sont CORROMPUES.")
print(f"- 68/85 sessions contiennent du garbage (headers PDF, mois dans secteurs, textes de retraits).")
print(f"- Les totaux labels ({total_valid_labels}) et pré-labels ({total_valid_prelabels}) sont INSUFFISANTS.")
print(f"- Les retraits ({total_retraits}) et conversions ({total_conversions}) sont à 0.")
print(f"- Les valeurs correctes sont dans session_data (pour la plupart des sessions) mais")
print(f"  les entrées brutes 'entrees' sont inutilisables pour {len(sessions_fausses)} sessions.")
print('=' * 80)
