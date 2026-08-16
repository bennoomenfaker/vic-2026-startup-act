#!/usr/bin/env python3
"""Construction de la base de données Startups & Fondateurs (version starter).

Entrée  : les 85 JSON de sessions (public/data/session-pdfs-json/) + les
          sources de vérité corrigées (sessions.json, parcours.json, corrections.json).
Sortie  :
  - public/data/founders_database.sqlite   (4 tables normalisées)
  - public/data/database_startups_sessions.csv
  - public/data/database_founders.csv
  - public/data/database_startup_founders.csv
  - public/data/founder_db_qa_report.json  (champs incertains → vérification manuelle)

⚠ Le parse PDF brut étant partiel/bruité, chaque ligne reçoit des drapeaux
  de qualité. Les lignes flaguées sont listées dans founder_db_qa_report.json,
  groupées par session, pour vérification manuelle.
"""
import csv
import json
import os
import re
import sqlite3
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'public', 'data')
JSON_DIR = os.path.join(DATA, 'session-pdfs-json')
MANUAL_DIR = os.path.join(DATA, 'manual_sessions')


def load_manual_sessions():
    """Vérité de terrain : Comptes-Rendus recopiés à la main (public/data/manual_sessions/).

    Une session listée ici remplace TOTALEMENT ses lignes parsées du PDF brut :
    chaque row = 1 candidature aux champs propres (aucun drapeau QA).
    """
    manual = {}
    if not os.path.isdir(MANUAL_DIR):
        return manual
    for fn in sorted(os.listdir(MANUAL_DIR)):
        if not fn.endswith('.json'):
            continue
        try:
            m = json.load(open(os.path.join(MANUAL_DIR, fn), encoding='utf-8'))
        except Exception:
            continue
        if m.get('session'):
            manual[m['session']] = m
    return manual


def norm(s):
    """Normalisation insensible aux accents/casse pour déduplication."""
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', s).strip().lower()


# --- Listes de référence ---------------------------------------------------
SECTORS = json.load(open(os.path.join(DATA, 'sectors.json'), encoding='utf-8'))
SECTOR_NAMES = sorted([s['name'] for s in SECTORS], key=len, reverse=True)
# variantes françaises / abrégées rencontrées dans les PDF
SECTOR_VARIANTS = [
    'business software and services', 'commerce and shopping', 'commerces & shopping',
    'healthtech', 'edtech', 'ad tech and creative tech', 'fintech', 'agritech',
    'agri tech', 'mobility', 'consumer products and services', 'advanced manufacturing',
    'environment', 'traveltech', 'foodtech', 'wellness', 'legaltech', 'iot', 'gaming',
    'biotech', 'e-commerce', 'e commerce', 'telecom', 'industrie robotique',
    'fin tech', 'pharmatech', 'fintech', 'real estate', 'real estate tech',
    'social business', 'pharma', 'digital health', 'vehicules electriques',
    'commerce and', 'business software and', 'ad tech and', 'consumer products and',
    'consumer', 'business', 'services', 'sante', 'medtech', 'construction',
]
SECTOR_NOISE = sorted(SECTOR_NAMES + SECTOR_VARIANTS, key=len, reverse=True)

DECISION_WORDS = [
    'label accord', 'prélabel accord', 'prelabel accord', 'label non accord',
    'prélabel non accord', 'prelabel non accord', 'retrait', 'retir', 'accord',
    'refus', 'irrecevable', 'report', 'dossier', 'non-indépendance',
]
NOISE_TOKENS = [
    'n.a', 'n/a', 'na', 'résultat', 'resultat', 'décision', 'decision', 'commentaires',
    'recevabilité', 'recevabilite', 'pitching', 'conflit', 'déclaré', 'declare',
    'absent', 'motif', 'valables', 'valable', 'conflits', 'intérêt', 'interet',
    'label', 'prélabel', 'prelabel', 'accordé', 'accord', 'accorde', 'non accord',
    'oui', 'non', 'tour', 'er tour', 'ème tour', 'eme tour', 'cr', 'page',
    'société', 'fondateurs', 'secteur', 'logo', 'undefined', 'null',
]
NOISE_SUBSTR = ['declaré', 'declare', 'déclaré', 'conflit', 'intérêt', 'absent',
                'motif', 'recevabilité', 'pitching', 'commentaires', 'compte-rendu',
                'startup act', 'société, fondateurs', 'label/prélabel', 'résultat', 'décision']
ORG_WORDS = ['sarl', 'ste ', 'ste.', 'corp', 'labs', 'solutions', 'technologies',
             'technology', 'services', 'company', 'group', 'digital', 'systems',
             'software', 'holding', 'tunisia', 'tunisie', 's.a', 's.a.r.l', 'apps',
             'gmbh', 'ltd', 'limited', 'n°', 'nº', 'sté']


def looks_noise(t):
    low = t.lower()
    if not t:
        return True
    if low in NOISE_TOKENS:
        return True
    return any(s in low for s in NOISE_SUBSTR)


def looks_decision(t):
    low = norm(t)
    if not low:
        return False
    return any(w in low for w in DECISION_WORDS) or low.startswith(('1er', '2ème', '2eme', '3ème', '3eme'))


def looks_sector(t):
    low = norm(t)
    for s in SECTOR_NOISE:
        if s and s in low:
            return True
    return False


def looks_person(t):
    low = norm(t)
    if not t or len(t) < 3 or len(low.split()) < 2 or len(low.split()) > 5:
        return False
    if looks_noise(t) or looks_decision(t) or looks_sector(t):
        return False
    if any(w in low for w in ORG_WORDS):
        return False
    if not t[0].isupper():
        return False
    # un nom de personne = pas d'initiale seule, pas de tout-majuscules acronyme
    words = t.split()
    if any(len(w) == 1 for w in words):
        return False
    if any(w.isupper() and len(w) > 1 for w in words):
        return False
    return True


def detect_decision(resultat, societe, fondateurs):
    text = ' '.join(x for x in (resultat, societe, fondateurs) if x).lower()
    text = text.replace('é', 'e').replace('è', 'e').replace('ê', 'e').replace('à', 'a')
    if 'retrait' in text or 'retir' in text:
        return 'retrait'
    if 'prelabel non accord' in text or 'pré-label non accord' in text:
        return 'prelabel_refuse'
    if 'label non accord' in text:
        return 'label_refuse'
    if 'age maximum' in text or '8 ans' in text or 'depasse' in text or 'non independance' in text:
        return 'label_refuse'
    if 'prelabel accord' in text:
        return 'prelabel_accorde'
    if 'label accord' in text:
        return 'label_accorde'
    if 'irrecevable' in text or 'non-independance' in text or 'non-indépendance' in text:
        return 'irrecevable'
    if 'report' in text:
        return 'reporte'
    return 'inconnu'


def extract_founders(fondateurs):
    """Scinde le champ fondateurs et ne retient que les tokens 'personne'."""
    tokens = [t.strip() for t in re.split(r'[;,]+', fondateurs or '') if t.strip()]
    people, uncertain = [], []
    for t in tokens:
        if looks_person(t):
            people.append(t)
        elif not looks_noise(t) and not looks_sector(t) and not looks_decision(t):
            uncertain.append(t)
    return people, uncertain


def extract_sector(secteur, fondateurs, societe):
    """Secteur : champ dédié s'il est plausible, sinon token secteur dans fondateurs."""
    for cand in (secteur, societe):
        if cand and looks_sector(cand):
            low = norm(cand)
            for s in SECTOR_NOISE:
                if s and s in low:
                    return s.title()
    if fondateurs:
        for t in re.split(r'[;,]+', fondateurs):
            t = t.strip()
            if t and looks_sector(t):
                return t
    return ''


def main():
    files = sorted(f for f in os.listdir(JSON_DIR) if re.match(r'session_\d{4}_\d{2}\.json$', f))
    sessions_src = json.load(open(os.path.join(DATA, 'sessions.json'), encoding='utf-8'))
    parc = json.load(open(os.path.join(DATA, 'parcours.json'), encoding='utf-8'))
    sessions_map = {s['session']: s for s in sessions_src}
    parc_map = {s['session']: s for s in parc['sessions']}

    conn = sqlite3.connect(os.path.join(DATA, 'founders_database.sqlite'))
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS startup_founders')
    cur.execute('DROP TABLE IF EXISTS founders')
    cur.execute('DROP TABLE IF EXISTS startups')
    cur.execute('DROP TABLE IF EXISTS sessions')
    cur.execute('''CREATE TABLE sessions(
        session TEXT PRIMARY KEY, candidatures INT, labels INT, preLabels INT,
        retraits INT, conversions INT, newLabels INT, tauxPct REAL, statut TEXT)''')
    cur.execute('''CREATE TABLE startups(
        id INTEGER PRIMARY KEY AUTOINCREMENT, session TEXT, societe TEXT,
        secteur TEXT, decision TEXT, source TEXT, flags TEXT)''')
    cur.execute('''CREATE TABLE founders(
        id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, nom_normalise TEXT)''')
    cur.execute('CREATE UNIQUE INDEX idx_founders_norm ON founders(nom_normalise)')
    cur.execute('''CREATE TABLE startup_founders(
        startup_id INTEGER, founder_id INTEGER, PRIMARY KEY(startup_id, founder_id))''')

    for key in sorted(sessions_map.keys(), key=lambda k: (int(k.split('/')[1]), int(k.split('/')[0]))):
        s = sessions_map[key]
        q = parc_map.get(key, {})
        taux = round(s['labels'] / s['candidatures'] * 100, 1) if s['candidatures'] else 0
        cur.execute('INSERT INTO sessions VALUES (?,?,?,?,?,?,?,?,?)',
                    (key, s['candidatures'], s['labels'], s['preLabels'],
                     q.get('retraits', 0), q.get('conversions', 0), q.get('newLabels', 0),
                     taux, 'corrigee' if s.get('statut') == 'corrigee' else 'conforme'))

    founder_ids = {}
    qa = []
    nb_startups = 0
    nb_founders = 0
    nb_manual = 0
    manual = load_manual_sessions()
    nb_manual_sessions = len(manual)

    for fp in files:
        d = json.load(open(os.path.join(JSON_DIR, fp), encoding='utf-8'))
        session = d['session']
        m = manual.get(session)

        if m:
            # --- Session relue à la main : on remplace le parse PDF bruité -------
            entries = []
            for i, row in enumerate(m.get('rows', []), 1):
                entries.append({
                    'idx': i,
                    'societe': (row.get('societe') or '').strip(),
                    'fondateurs': (row.get('fondateurs') or []),
                    'secteur': (row.get('secteur') or '').strip(),
                    'resultat': (row.get('resultat') or '').strip(),
                    'decision': row.get('decision') or 'inconnu',
                    'source': 'compte-rendu-manuel',
                })
            nb_manual += len(entries)
        else:
            entries = [{
                'idx': idx,
                'societe': (e.get('societe') or '').strip(),
                'fondateurs': (e.get('fondateurs') or '').strip(),
                'secteur': (e.get('secteur') or '').strip(),
                'resultat': (e.get('resultat') or '').strip(),
                'decision': None,
                'source': 'pdf-session',
            } for idx, e in enumerate(d.get('entrees', []), 1)]

        for e in entries:
            idx = e['idx']
            societe = e['societe']
            fondateurs = e['fondateurs']
            secteur = e['secteur']
            resultat = e['resultat']

            flags = []
            decision = e['decision']

            if e['source'] == 'compte-rendu-manuel':
                people = [p.strip() for p in fondateurs if p and p.strip()]
                secteur_clean = secteur
                societe_clean = societe
            else:
                if looks_noise(societe):
                    flags.append('societe_parasite')
                if not societe:
                    flags.append('societe_vide')
                if not fondateurs or fondateurs.lower().startswith('n.a'):
                    flags.append('fondateurs_absents')
                if not resultat:
                    flags.append('resultat_manquant')
                if not secteur or looks_decision(secteur) or secteur.lower() == 'valables':
                    flags.append('secteur_absent')

                decision = detect_decision(resultat, societe, fondateurs)
                if decision == 'inconnu':
                    flags.append('decision_inconnue')

                people, uncertain = extract_founders(fondateurs)
                if uncertain:
                    flags.append('fondateurs_ambigus')

                secteur_clean = extract_sector(secteur, fondateurs, societe)

                # reconstruction du nom de société quand la colonne est décalée
                societe_clean = societe
                if looks_noise(societe) or looks_decision(societe) or looks_sector(societe) or not societe:
                    if fondateurs:
                        for t in re.split(r'[;,]+', fondateurs):
                            t = t.strip()
                            if t and not looks_noise(t) and not looks_person(t) and not looks_decision(t) and not looks_sector(t):
                                societe_clean = t
                                flags.append('societe_reconstruite')
                                break
                if not societe_clean or looks_noise(societe_clean) or looks_sector(societe_clean):
                    flags.append('societe_non_identifiee')

                # on saute les vraies lignes parasites (en-têtes/footers)
                low = (societe + ' ' + fondateurs).lower()
                if not societe_clean or societe_clean.lower() in ('n.a', 'résultat', 'resultat', 'décision') \
                        or 'startup act' in low or 'compte-rendu' in low:
                    continue

            cur.execute('INSERT INTO startups(session, societe, secteur, decision, source, flags) VALUES (?,?,?,?,?,?)',
                        (session, societe_clean, secteur_clean, decision, e['source'], ';'.join(flags)))
            sid = cur.lastrowid
            nb_startups += 1

            for name in people:
                nn = norm(name)
                if nn not in founder_ids:
                    cur.execute('INSERT INTO founders(nom, nom_normalise) VALUES (?,?)', (name, nn))
                    founder_ids[nn] = cur.lastrowid
                    nb_founders += 1
                cur.execute('INSERT OR IGNORE INTO startup_founders VALUES (?,?)', (sid, founder_ids[nn]))

            if flags:
                qa.append({
                    'session': session, 'ligne': idx, 'societe': societe_clean,
                    'fondateurs': fondateurs, 'secteur': secteur, 'resultat': resultat,
                    'decision': decision, 'flags': flags,
                })

    conn.commit()

    # --- Exports CSV --------------------------------------------------------
    def dump_csv(name, sql, cols):
        rows = cur.execute(sql).fetchall()
        with open(os.path.join(DATA, name), 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f, delimiter=';')
            w.writerow(cols)
            w.writerows(rows)
        return len(rows)

    n1 = dump_csv('database_startups_sessions.csv',
                  'SELECT session, societe, secteur, decision, source, flags FROM startups ORDER BY session',
                  ['session', 'societe', 'secteur', 'decision', 'source', 'flags'])
    n2 = dump_csv('database_founders.csv',
                  'SELECT id, nom, nom_normalise FROM founders ORDER BY nom_normalise',
                  ['id', 'nom', 'nom_normalise'])
    n3 = dump_csv('database_startup_founders.csv',
                  'SELECT sf.startup_id, sf.founder_id, st.session, st.societe, fd.nom '
                  'FROM startup_founders sf JOIN startups st ON st.id=sf.startup_id '
                  'JOIN founders fd ON fd.id=sf.founder_id ORDER BY st.session',
                  ['startup_id', 'founder_id', 'session', 'societe', 'fondateur'])

    # --- Rapport QA ----------------------------------------------------------
    qa_by_session = {}
    for item in qa:
        qa_by_session.setdefault(item['session'], []).append(item)
    report = {
        'generated': True,
        'note': 'Lignes dont un ou plusieurs champs restent incertains (parse PDF brut). Vérification manuelle recommandée.',
        'nb_sessions_manuelles': nb_manual_sessions,
        'nb_lignes_manuelles': nb_manual,
        'total_lignes_qa': len(qa),
        'nb_sessions_qa': len(qa_by_session),
        'par_session': qa_by_session,
    }
    with open(os.path.join(DATA, 'founder_db_qa_report.json'), 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=1)

    # --- JSON consolidé pour l'application -----------------------------------
    founder_db = {
        'meta': {
            'nb_sessions': len(sessions_map),
            'nb_startups': nb_startups,
            'nb_founders': nb_founders,
            'nb_liens': n3,
            'nb_qa': len(qa),
            'nb_sessions_qa': len(qa_by_session),
            'nb_sessions_manuelles': nb_manual_sessions,
            'nb_lignes_manuelles': nb_manual,
            'generated': 'extraction PDF brute — décisions et secteurs indicatifs (chiffres officiels : sessions.json)',
        },
        'sessions': [
            {'session': k, 'candidatures': s['candidatures'], 'labels': s['labels'],
             'preLabels': s['preLabels'], 'retraits': parc_map.get(k, {}).get('retraits', 0),
             'conversions': parc_map.get(k, {}).get('conversions', 0), 'statut': s.get('statut')}
            for k, s in sorted(sessions_map.items(), key=lambda kv: (int(kv[0].split('/')[1]), int(kv[0].split('/')[0])))
        ],
        'startups': [],
    }
    cur2 = conn.cursor()
    cur3 = conn.cursor()
    for sid, session, societe, secteur, decision, flags in cur2.execute(
            'SELECT id, session, societe, secteur, decision, flags FROM startups ORDER BY session, id'):
        fds = [r[0] for r in cur3.execute(
            'SELECT fd.nom FROM startup_founders sf JOIN founders fd ON fd.id=sf.founder_id WHERE sf.startup_id=?',
            (sid,))]
        founder_db['startups'].append({
            'id': sid, 'session': session, 'societe': societe, 'secteur': secteur,
            'decision': decision, 'flags': flags, 'founders': fds,
        })
    with open(os.path.join(DATA, 'founder_db.json'), 'w', encoding='utf-8') as f:
        json.dump(founder_db, f, ensure_ascii=False)
    conn.close()
    print(f'sessions en base : {len(sessions_map)}  (dont {nb_manual_sessions} relues manuellement)')
    print(f'startups (candidats PDF) : {nb_startups}  → CSV {n1} lignes  (dont {nb_manual} lignes manuelles)')
    print(f'fondateurs uniques : {nb_founders}  → CSV {n2} lignes')
    print(f'liens startup↔fondateur : {n3}')
    print(f'rapport QA : {len(qa)} lignes incertaines dans {len(qa_by_session)} sessions')


if __name__ == '__main__':
    main()
