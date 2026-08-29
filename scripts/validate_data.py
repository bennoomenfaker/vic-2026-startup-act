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
    check(len(dashboard.get('sessions', [])) == 88, f"Attendu 88 sessions, trouvé {len(dashboard.get('sessions', []))}")
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
    check(len(ps) == 88, f"parcours: {len(ps)} sessions (attendu 88)")
    for s in ps:
        check(s.get('totalLabels') == s.get('newLabels') + s.get('conversions'),
              f"parcours {s['session']}: totalLabels != newLabels + conversions")

# --- corrections : structure ---
if corrections is not None:
    check(len(corrections.get('corrections', [])) == 21, "corrections: attendu 21 corrections")
    check(corrections.get('meta', {}).get('totalsOld', {}).get('labels') == 1324, "corrections: totalsOld.labels != 1324")
    check(corrections.get('meta', {}).get('totalsNew', {}).get('labels') == 1311, "corrections: totalsNew.labels != 1311")
    check(corrections.get('meta', {}).get('totalsNew', {}).get('preLabels') == 623, "corrections: totalsNew.preLabels != 623")

    rec88 = corrections.get('reconciliation88', [])
    if rec88:
        meta = corrections.get('meta', {})

        # Règle de cohérence globale : la somme des lignes PDF par session doit
        # égaler le total d'en-tête (3 571) et la somme des catégories doit l'égaler.
        sum_lignes = sum(r.get('pdf_detail', {}).get('lignes', 0) for r in rec88)
        pdf_manifest = meta.get('pdfDetailTotals88', {})
        check(sum_lignes == pdf_manifest.get('lignes'),
              f"reconciliation: sum(lignes) {sum_lignes} != meta.pdfDetailTotals88.lignes {pdf_manifest.get('lignes')}")
        check(pdf_manifest.get('lignes') == 3571,
              f"reconciliation: pdfDetailTotals88.lignes {pdf_manifest.get('lignes')} != 3571")
        cat_sum = sum(pdf_manifest.get('categories', {}).values())
        check(cat_sum == pdf_manifest.get('lignes'),
              f"pdfDetailTotals88.categories sum {cat_sum} != lignes {pdf_manifest.get('lignes')}")
        for r in rec88:
            pd = r.get('pdf_detail', {})
            check(sum(pd.get('categories', {}).values()) == pd.get('lignes'),
                  f"reconciliation {r.get('session')}: categories sum != lignes")

        # La somme des candidatures corrigées à l'en-tête (3 574), les labels
        # corrigés (1 343) et prélabels corrigés (647) doivent correspondre.
        sum_cand = sum(r.get('corrected_counter', {}).get('candidatures', 0) for r in rec88)
        sum_labels = sum(r.get('corrected_counter', {}).get('labels', 0) for r in rec88)
        sum_pre = sum(r.get('corrected_counter', {}).get('preLabels', 0) for r in rec88)
        cc = meta.get('correctedCounterTotals88', {})
        check(sum_cand == cc.get('candidatures'),
              f"reconciliation: sum(candidatures corrigées) {sum_cand} != {cc.get('candidatures')}")
        check(sum_labels == cc.get('labels'),
              f"reconciliation: sum(labels corrigés) {sum_labels} != {cc.get('labels')}")
        check(sum_pre == cc.get('preLabels'),
              f"reconciliation: sum(prélabels corrigés) {sum_pre} != {cc.get('preLabels')}")

        # Garde-fou direct contre le bug des lignes PDF : chaque ligne par session
        # doit égaler le nombre d'entrées du JSON de session source.
        session_json_dir = os.path.join(DATA, 'session-pdfs-json')
        for r in rec88:
            sess = r.get('session', '')
            try:
                month, year = sess.split('/')
            except ValueError:
                continue
            path = os.path.join(session_json_dir, f'session_{year}_{month}.json')
            if not os.path.exists(path):
                ERRORS.append(f'JSON de session source manquant pour reconciliation {sess}: {path}')
                continue
            try:
                with open(path, encoding='utf-8') as f:
                    n_lines = len(json.load(f).get('entrees', []))
            except Exception as e:
                ERRORS.append(f'JSON de session invalide {path}: {e}')
                continue
            check(r.get('pdf_detail', {}).get('lignes') == n_lines,
                  f"reconciliation {sess}: pdf_detail.lignes {r.get('pdf_detail', {}).get('lignes')} != entrees source {n_lines}")


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
print('OK — toutes les données sont cohérentes (88 sessions, 1343 labels, 647 prélabels, 21 corrections).')
