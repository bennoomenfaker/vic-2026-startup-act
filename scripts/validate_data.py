#!/usr/bin/env python3
"""Validation d'intégrité des données du projet Startup Act Tunisie.

Vérifie la cohérence des jeux de données corrigés (dashboard / sessions /
parcours / corrections) avant chaque build CI. Retourne un code de sortie
non nul si une incohérence est détectée.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'public', 'data')

ERRORS = []


def load(name):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        ERRORS.append(f'Fichier manquant: {name}')
        return None
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        ERRORS.append(f'JSON invalide: {name} ({e})')
        return None


def check(cond, msg):
    if not cond:
        ERRORS.append(msg)


dashboard = load('dashboard_data.json')
sessions = load('sessions.json')
parcours = load('parcours.json')
corrections = load('corrections.json')

# --- dashboard & sessions : cohérence mutuelle ---
if dashboard is not None and sessions is not None:
    ds = dashboard.get('sessions', [])
    check(len(ds) == len(sessions), f"dashboard.sessions ({len(ds)}) != sessions.json ({len(sessions)})")
    for i, s in enumerate(sessions):
        if i < len(ds):
            for key in ('session', 'candidatures', 'labels', 'preLabels'):
                check(ds[i].get(key) == s.get(key),
                      f"Divergence {key} session {s.get('session')}: dashboard={ds[i].get(key)} json={s.get(key)}")

# --- taux arrondis corrects (exact -> 1 décimale) et tauxAcceptation + tauxEchec = 100 ---
if dashboard is not None:
    for s in dashboard.get('sessions', []):
        exact = s.get('tauxAcceptationExact')
        taux = s.get('tauxAcceptation')
        echec = s.get('tauxEchec')
        if exact is not None and taux is not None:
            check(str(round(exact, 1)) == str(taux),
                  f"Taux arrondi incohérent {s['session']}: {round(exact,1)} vs {taux}")
        if taux is not None and echec is not None:
            check(abs(float(taux) + float(echec) - 100.0) < 0.01,
                  f"{s['session']}: tauxAcceptation + tauxEchec != 100 ({taux}+{echec})")
    check(len(dashboard.get('sessions', [])) == 85, f"Attendu 85 sessions, trouvé {len(dashboard.get('sessions', []))}")
    raw = open(os.path.join(DATA, 'dashboard_data.json'), encoding='utf-8').read()
    check('"10/25"' not in raw, "Clé résiduelle '10/25' détectée (doit être 10/2025)")

# --- parcours : meta cohérente avec les sessions ---
if parcours is not None:
    meta = parcours.get('meta', {})
    ps = parcours.get('sessions', [])
    sum_new = sum(s.get('newLabels', 0) for s in ps)
    sum_pre = sum(s.get('preLabels', 0) for s in ps)
    sum_conv = sum(s.get('conversions', 0) for s in ps)
    sum_ret = sum(s.get('retraits', 0) for s in ps)
    sum_tot = sum(s.get('totalLabels', 0) for s in ps)
    check(sum_new == meta.get('totalNewLabels'), f"parcours: newLabels {sum_new} != meta {meta.get('totalNewLabels')}")
    check(sum_pre == meta.get('totalNewPreLabels'), f"parcours: preLabels {sum_pre} != meta {meta.get('totalNewPreLabels')}")
    check(sum_conv == meta.get('totalConversions'), f"parcours: conversions {sum_conv} != meta {meta.get('totalConversions')}")
    check(sum_ret == meta.get('totalRetraits'), f"parcours: retraits {sum_ret} != meta {meta.get('totalRetraits')}")
    check(sum_tot == meta.get('totalLabels'), f"parcours: totalLabels {sum_tot} != meta {meta.get('totalLabels')}")
    check(len(ps) == 85, f"parcours: {len(ps)} sessions (attendu 85)")
    for s in ps:
        check(s.get('totalLabels') == s.get('newLabels') + s.get('conversions'),
              f"parcours {s['session']}: totalLabels != newLabels + conversions")

# --- corrections : structure ---
if corrections is not None:
    check(len(corrections.get('corrections', [])) == 20, "corrections: attendu 20 corrections")
    check(corrections.get('meta', {}).get('totalsOld', {}).get('labels') == 1324, "corrections: totalsOld.labels != 1324")
    check(corrections.get('meta', {}).get('totalsNew', {}).get('labels') == 1311, "corrections: totalsNew.labels != 1311")
    check(corrections.get('meta', {}).get('totalsNew', {}).get('preLabels') == 623, "corrections: totalsNew.preLabels != 623")

# --- fichiers statiques essentiels ---
for f in ('images/faker.jpeg', 'images/esen.jpeg', 'images/iscae.jpeg', 'images/atvic.jpeg'):
    p = os.path.join(ROOT, 'streamlit-app', 'public', f)
    if not os.path.isfile(p):
        ERRORS.append(f'Image manquante: {f}')

if ERRORS:
    print(f'ÉCHEC — {len(ERRORS)} erreur(s):')
    for e in ERRORS:
        print('  -', e)
    sys.exit(1)
print('OK — toutes les données sont cohérentes (85 sessions, 1311 labels, 623 prélabels, 20 corrections).')
