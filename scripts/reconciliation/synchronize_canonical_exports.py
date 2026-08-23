from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
import csv
import json
import re
import shutil
import sqlite3
import unicodedata

REPO = Path('/home/ubuntu/vic-2026-startup-act-4339943')
DATA = REPO / 'public' / 'data'
PACKAGE = Path('/home/ubuntu/startup_act_final_delivery_88/canonical_package')
CANONICAL_PATH = DATA / 'reextraction_88_canonical.json'
BACKUP = Path('/home/ubuntu/backups_before_export_resync_2026-08-23')
BACKUP.mkdir(parents=True, exist_ok=True)

canonical = json.loads(CANONICAL_PATH.read_text(encoding='utf-8'))
meta = canonical['meta']
sessions = canonical['sessions']
entries = canonical['entries']
entries_by_id = {e['decision_id']: e for e in entries}
entries_by_session = defaultdict(list)
# Ajournés signalés dans les commentaires officiels mais absents des lignes PDF nommées.
AJOURNES_HORS_PDF = {'03/2019': 2, '06/2019': 1}
for e in entries:
    entries_by_session[e['session']].append(e)
for es in entries_by_session.values():
    es.sort(key=lambda e: (int(e.get('line') or 0), str(e.get('decision_id') or '')))


def read_csv(path, delimiter=';'):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=delimiter))


def write_csv(path, headers, rows, delimiter=';'):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=headers, delimiter=delimiter, extrasaction='ignore', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def norm(value):
    text = unicodedata.normalize('NFKD', str(value or '').lower())
    text = ''.join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r'[^a-z0-9]+', '', text)


def json_dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sql_quote(value):
    if value is None or value == '':
        return 'NULL'
    return "'" + str(value).replace("'", "''") + "'"

# Back up only files that this script will replace.
source_csvs = {
    'sessions': PACKAGE / 'database_sessions_reextrait.csv',
    'entries': PACKAGE / 'database_entrees_reextrait.csv',
    'companies': PACKAGE / 'database_companies_reextrait.csv',
    'founders': PACKAGE / 'database_founders_reextrait.csv',
    'relationships': PACKAGE / 'database_company_founders_reextrait.csv',
}
managed = [
    DATA / 'sessions_88.json', DATA / 'startup_act_88_sessions.json', DATA / 'startup_act_database_normalized.json',
    DATA / 'founder_db.json', DATA / 'founder_db_88.json', DATA / 'database_startups_88.json',
    DATA / 'sessions_table.json', DATA / 'database_88.csv', DATA / 'database_entrees_brutes_88.csv', DATA / 'database_entrees_brutes.csv',
    DATA / 'database_sessions_88.csv', DATA / 'database_sessions.csv', DATA / 'database_founders_88.csv', DATA / 'database_founders.csv',
    DATA / 'database_startup_founders_88.csv', DATA / 'database_startup_founders.csv', DATA / 'dual_candidate_counts_88.csv',
    DATA / 'database_sessions_reextrait_88_corrige.csv', DATA / 'database_entrees_reextrait_88_corrige.csv',
    DATA / 'database_companies_reextrait_88_corrige.csv', DATA / 'database_founders_reextrait_88_corrige.csv',
    DATA / 'database_company_founders_reextrait_88_corrige.csv', DATA / 'founders_database.sqlite',
    DATA / 'reextraction_88_canonical.sql', DATA / 'startup_act_database.sql', DATA / 'startup_act_database_88.sql',
    DATA / 'startup_act_database_reextrait_corrige_2026-08-23.sql',
]
for p in managed:
    if p.exists():
        target = BACKUP / p.name
        if not target.exists():
            shutil.copy2(p, target)

# Use the checked canonical CSVs as relational source tables.
company_rows = read_csv(source_csvs['companies'])
founder_rows = read_csv(source_csvs['founders'])
relationship_rows = read_csv(source_csvs['relationships'])
company_by_key = {(r['company_name'], r['session']): r['company_id'] for r in company_rows}
founder_by_name = {r['founder_name']: r['founder_id'] for r in founder_rows}
founders_by_decision = defaultdict(list)
for r in relationship_rows:
    founders_by_decision[r['decision_id']].append(r)

# Session-table JSON: official counters and detail-derived auxiliary series stay explicit.
old_sessions_table = {}
if (DATA / 'sessions_table.json').exists():
    old_sessions_table = json.loads((DATA / 'sessions_table.json').read_text(encoding='utf-8'))
old_by_session = {r.get('session'): r for r in old_sessions_table.get('sessions', [])}
conv_total = sum(int(s.get('conversions') or 0) for s in sessions)
ret_total = sum(int(s.get('retraits') or 0) for s in sessions)
report_total = sum(int(s.get('reportes') or 0) for s in sessions)
aux_rows = []
for s in sessions:
    old = old_by_session.get(s['session'], {})
    # Validated ajournés: 03/2019 (2) and 06/2019 (1).
    # The historical raw comment counter is not inherited because it exposed an unvalidated 04/2019 entry.
    ajournes = AJOURNES_HORS_PDF.get(s['session'], 0)
    ajournes_hors_pdf = AJOURNES_HORS_PDF.get(s['session'], 0)
    pdf_calc = int(s['entries']) - int(s.get('conversions') or 0) - int(s.get('retraits') or 0) - int(s.get('reportes') or 0)
    row = dict(s)
    row.update({
        'ajournes': ajournes,
        'candidatures_officielles': int(s['candidatures']),
        'candidatures_pdf_calculees': pdf_calc,
        'ecart_candidatures_pdf_officiel': pdf_calc - int(s['candidatures']),
        'formule_candidatures_pdf': 'lignes_pdf − conversions − retraits − reportes (indicateur auxiliaire; ne remplace pas le compteur officiel)',
        'candidatures_reexamen_pdf': int(s['entries']),
        'ajournes_hors_lignes_reexamen': ajournes,
        'ajournes_hors_pdf': ajournes_hors_pdf,
        'candidatures_corrigees': int(s['entries']) + ajournes_hors_pdf,
    })
    aux_rows.append(row)
sessions_table = {
    'meta': {
        'source': 'reextraction_88_canonical.json',
        'nbSessions': len(sessions),
        'sessionsCorrigees': len(sessions),
        'totalCandidatures': sum(int(s['candidatures']) for s in sessions),
        'totalCandidaturesPdfCalculees': sum(int(r['candidatures_pdf_calculees']) for r in aux_rows),
        'totalCandidaturesReexamenPdf': len(entries),
        'totalCandidaturesCorrigees': len(entries) + sum(AJOURNES_HORS_PDF.values()),
        'ajournesHorsPdf': sum(AJOURNES_HORS_PDF.values()),
        'ecartTotalPdfMoinsOfficiel': len(entries) - sum(int(s['candidatures']) for s in sessions),
        'totalLabels': sum(int(s['labels']) for s in sessions),
        'totalPreLabels': sum(int(s['preLabels']) for s in sessions),
        'totalConversions': conv_total,
        'totalRetraits': ret_total,
        'totalReportes': report_total,
        'totalAjournes': sum(int(r['ajournes']) for r in aux_rows),
        'preLabelsRestants': sum(int(s['preLabels']) for s in sessions) - conv_total,
        'tauxMoyenPct': round(sum(int(s['labels']) for s in sessions) / sum(int(s['candidatures']) for s in sessions) * 100, 2),
        'candidatureMethods': 'Officiel = compteur Startup Tunisia; PDF détaillé = lignes documentaires; calcul auxiliaire = lignes − conversions − retraits − reportes.',
        'definitionCandidaturesReexamenPdf': 'Nombre de lignes documentaires du PDF, distinct du compteur officiel et non dédoublonné.',
    },
    'sessions': aux_rows,
}
json_dump(DATA / 'sessions_table.json', sessions_table)

# Detailed startup rows for legacy JSON endpoints.
startups = []
for idx, e in enumerate(entries, start=1):
    rels = founders_by_decision.get(e['decision_id'], [])
    names = [r['founder_name'] for r in rels]
    flags = []
    if not str(e.get('fondateurs') or '').strip(): flags.append('fondateurs_absents')
    if not str(e.get('secteur') or '').strip(): flags.append('secteur_absent')
    if not str(e.get('resultat_normalise') or '').strip(): flags.append('decision_inconnue')
    _, year = e['session'].split('/')
    startups.append({
        'id': idx,
        'decision_id': e['decision_id'],
        'session_id': e['session_id'],
        'session': e['session'],
        'nom': e.get('societe') or 'Non renseigné',
        'societe': e.get('societe') or 'Non renseigné',
        'projet': e.get('projet') or 'Non renseigné',
        'secteur': e.get('secteur') or 'Non renseigné',
        'anneeCreation': year,
        'labelDate': e['session'] if e.get('resultat_normalise') == 'Label accordé' else '',
        'siteWeb': '', 'resume': e.get('projet') or '', 'email': '', 'telephone': '',
        'source': f"PDF détaillé — {e.get('source_pdf')}",
        'decision': e.get('resultat_normalise') or 'Décision non précisée',
        'flags': ';'.join(flags),
        'founders': names,
    })

# Rich normalized bundle with all 3,555 detailed rows.
def build_sessions_bundle():
    old = {}
    p = DATA / 'sessions_88.json'
    if p.exists(): old = json.loads(p.read_text(encoding='utf-8'))
    old_meta = dict(old.get('metadata') or {})
    old_gender_macro = old.get('gender_macro')
    old_gender_yearly = old.get('gender_yearly')
    old_new_gender = old.get('new_gender_status')
    periods = {'01':'Janvier','02':'Février','03':'Mars','04':'Avril','05':'Mai','06':'Juin','07':'Juillet','08':'Août','09':'Septembre','10':'Octobre','11':'Novembre','12':'Décembre'}
    session_list = []
    for s in sessions:
        month, year = s['session'].split('/')
        session_list.append({
            'session_id': s['session_id'], 'period': f"{periods.get(month, month)} {year}", 'entries': int(s['entries']),
            'official': {'period': f"{periods.get(month, month)} {year}", 'labels': int(s['labels']), 'prelabels': int(s['preLabels']), 'total': int(s['labels']) + int(s['preLabels']), 'withdrawals': int(s['retraits'])},
            'candidatures_officielles': int(s['candidatures']), 'entries_detaillees': int(s['entries']), 'ajournes_hors_pdf': AJOURNES_HORS_PDF.get(s['session'], 0), 'candidatures_corrigees': int(s['entries']) + AJOURNES_HORS_PDF.get(s['session'], 0),
            'conversions': int(s['conversions']), 'document_withdrawals': int(s['retraits']), 'reports': int(s.get('reportes') or 0),
        })
    decision_list = []
    for e in entries:
        company_id = company_by_key.get((e.get('societe'), e.get('session')), '')
        decision_list.append({
            'decision_id': e['decision_id'], 'session_id': e['session_id'], 'company_id': company_id,
            'source_file': e.get('source_pdf'), 'section': e.get('section_pdf'), 'project': e.get('projet'), 'founders_raw': e.get('fondateurs'),
            'decision_raw': e.get('decision'), 'resultat_normalise': e.get('resultat_normalise'), 'type_decision': e.get('type_label'),
            'status_requested': e.get('type_label'), 'sector': e.get('secteur'), 'tour': e.get('tour_moment'),
            'after_pitching': e.get('apres_pitching'), 'award_or_withdrawal': e.get('session_obtention_retrait'),
            'comments': e.get('commentaires'), 'quality_control': e.get('controle_qualite'),
        })
    company_list = [{'company_id': r['company_id'], 'name': r['company_name'], 'sector': r['sector'], 'session': r['session'], 'project': ''} for r in company_rows]
    founder_list = [{'founder_id': r['founder_id'], 'name': r['founder_name']} for r in founder_rows]
    relation_list = []
    for r in relationship_rows:
        relation_list.append({'decision_id': r['decision_id'], 'company_id': company_by_key.get((r['company_name'], r['session']), ''), 'founder_id': founder_by_name.get(r['founder_name'], ''), 'session_id': next((e['session_id'] for e in entries if e['session'] == r['session']), ''), 'founder_raw': r['founder_name'], 'quality': 'Extrait PDF/JSON'})
    flags = []
    for e in entries:
        if not str(e.get('fondateurs') or '').strip():
            flags.append({'record_id': e['decision_id'], 'session_id': e['session_id'], 'company': e.get('societe'), 'issue': 'Fondateur manquant', 'detail': 'Non renseigné'})
    metadata = dict(old_meta)
    metadata.update({
        'scope': '88 sessions S0-S87; corpus canonique réextrait', 'sessions': len(sessions), 'official_candidatures': sum(int(s['candidatures']) for s in sessions),
        'official_labels': sum(int(s['labels']) for s in sessions), 'official_prelabels': sum(int(s['preLabels']) for s in sessions),
        'detailed_entries': len(entries), 'corrected_candidatures': len(entries) + sum(AJOURNES_HORS_PDF.values()), 'ajournes_hors_pdf': sum(AJOURNES_HORS_PDF.values()), 'official_withdrawals': ret_total, 'confirmed_reportes': report_total,
        'note': 'Les compteurs officiels (3 079), les 3 555 lignes détaillées PDF et les 3 ajournés hors PDF (3 558 corrigées) sont trois périmètres distincts.',
    })
    out = {'metadata': metadata, 'sessions': session_list, 'decisions': decision_list, 'companies': company_list, 'founders': founder_list, 'company_founders': relation_list, 'quality_flags': flags}
    if old_gender_macro is not None: out['gender_macro'] = old_gender_macro
    if old_gender_yearly is not None: out['gender_yearly'] = old_gender_yearly
    if old_new_gender is not None: out['new_gender_status'] = old_new_gender
    return out

bundle = build_sessions_bundle()
json_dump(DATA / 'sessions_88.json', bundle)
json_dump(DATA / 'startup_act_88_sessions.json', bundle)

normalized = {
    'metadata': {'scope': '88 sessions', 'official_candidatures': sum(int(s['candidatures']) for s in sessions), 'official_labels': sum(int(s['labels']) for s in sessions), 'official_prelabels': sum(int(s['preLabels']) for s in sessions), 'detailed_entries': len(entries), 'source': 'reextraction_88_canonical.json'},
    'sessions': [{'session_id': s['session_id'], 'session_key': s['session'], 'candidatures': s['candidatures'], 'labels': s['labels'], 'preLabels': s['preLabels'], 'retraits': s['retraits'], 'conversions': s['conversions'], 'rows': s['entries'], 'reportes': s.get('reportes', 0)} for s in sessions],
    'companies': [{'company_id': r['company_id'], 'company_name': r['company_name'], 'sector': r['sector'], 'session': r['session']} for r in company_rows],
    'founders': [{'founder_id': r['founder_id'], 'founder_name': r['founder_name']} for r in founder_rows],
    'company_founders': [{'decision_id': r['decision_id'], 'company_id': company_by_key.get((r['company_name'], r['session']), ''), 'founder_id': founder_by_name.get(r['founder_name'], ''), 'session': r['session']} for r in relationship_rows],
    'decisions': [{'decision_id': e['decision_id'], 'session_id': e['session_id'], 'company_id': company_by_key.get((e.get('societe'), e.get('session')), ''), 'company_name': e.get('societe'), 'founder_names': e.get('fondateurs'), 'decision': e.get('resultat_normalise'), 'sector': e.get('secteur'), 'source_pdf': e.get('source_pdf')} for e in entries],
}
json_dump(DATA / 'startup_act_database_normalized.json', normalized)
json_dump(DATA / 'database_startups_88.json', startups)
founder_db = {
    'meta': {'nb_sessions': len(sessions), 'nb_startups': len(startups), 'nb_founders': len(founder_rows), 'nb_liens': len(relationship_rows), 'nb_qa': len(bundle['quality_flags']), 'generated': 'corpus canonique PDF 88 sessions — compteurs officiels conservés séparément'},
    'sessions': [{'session': s['session'], 'candidatures': s['candidatures'], 'labels': s['labels'], 'preLabels': s['preLabels'], 'retraits': s['retraits'], 'conversions': s['conversions'], 'entries': s['entries'], 'reportes': s.get('reportes', 0)} for s in sessions],
    'startups': startups,
    'founders': [{'founder_id': r['founder_id'], 'name': r['founder_name']} for r in founder_rows],
    'quality_flags': bundle['quality_flags'],
}
json_dump(DATA / 'founder_db.json', founder_db)
json_dump(DATA / 'founder_db_88.json', founder_db)

# CSV exports: canonical names and legacy-compatible names.
entry_headers = ['decision_id','session_id','session','entreprise','source_file','section','projet','fondateurs','decision_brute','resultat_normalise','type_decision','statut_demande','secteur','tour','apres_pitching','obtention_retrait','commentaires','controle_qualite']
entry_csv_rows = []
for e in entries:
    entry_csv_rows.append({'decision_id': e['decision_id'], 'session_id': e['session_id'], 'session': e['session'], 'entreprise': e.get('societe'), 'source_file': e.get('source_pdf'), 'section': e.get('section_pdf'), 'projet': e.get('projet'), 'fondateurs': e.get('fondateurs'), 'decision_brute': e.get('decision'), 'resultat_normalise': e.get('resultat_normalise'), 'type_decision': e.get('type_label'), 'statut_demande': e.get('type_label'), 'secteur': e.get('secteur'), 'tour': e.get('tour_moment'), 'apres_pitching': e.get('apres_pitching'), 'obtention_retrait': e.get('session_obtention_retrait'), 'commentaires': e.get('commentaires'), 'controle_qualite': e.get('controle_qualite')})
for filename in ['database_88.csv','database_entrees_brutes_88.csv','database_entrees_brutes.csv']:
    write_csv(DATA / filename, entry_headers, entry_csv_rows, delimiter=',')

session_legacy_headers = ['session','candidatures','labels','preLabels','retraits','conversions','newLabels','taux_acceptation_pct','statut','entries','reportes']
session_legacy_rows = [{**{k: s.get(k) for k in ['session','candidatures','labels','preLabels','retraits','conversions','newLabels']}, 'taux_acceptation_pct': s.get('tauxPct'), 'statut': s.get('statut'), 'entries': s.get('entries'), 'reportes': s.get('reportes', 0)} for s in sessions]
write_csv(DATA / 'database_sessions_88.csv', session_legacy_headers, session_legacy_rows)

founder_legacy_headers = ['id','nom','nom_normalise']
founder_legacy_rows = [{'id': r['founder_id'], 'nom': r['founder_name'], 'nom_normalise': norm(r['founder_name'])} for r in founder_rows]
write_csv(DATA / 'database_founders_88.csv', founder_legacy_headers, founder_legacy_rows)
write_csv(DATA / 'database_founders.csv', ['founder_id','name'], [{'founder_id': r['founder_id'], 'name': r['founder_name']} for r in founder_rows])

rel_legacy_headers = ['startup_id','founder_id','session','societe','fondateur']
rel_legacy_rows = [{'startup_id': company_by_key.get((r['company_name'], r['session']), ''), 'founder_id': founder_by_name.get(r['founder_name'], ''), 'session': r['session'], 'societe': r['company_name'], 'fondateur': r['founder_name']} for r in relationship_rows]
write_csv(DATA / 'database_startup_founders_88.csv', rel_legacy_headers, rel_legacy_rows, delimiter=',')
write_csv(DATA / 'database_startup_founders.csv', ['company_id','founder_id','session_id','founder_raw','quality'], [{'company_id': company_by_key.get((r['company_name'], r['session']), ''), 'founder_id': founder_by_name.get(r['founder_name'], ''), 'session_id': next((e['session_id'] for e in entries if e['session'] == r['session']), ''), 'founder_raw': r['founder_name'], 'quality': 'Extrait PDF/JSON'} for r in relationship_rows])

# Copy checked canonical CSVs to explicit 88 corrected names.
for src_key, target_name in [('sessions','database_sessions_reextrait_88_corrige.csv'), ('entries','database_entrees_reextrait_88_corrige.csv'), ('companies','database_companies_reextrait_88_corrige.csv'), ('founders','database_founders_reextrait_88_corrige.csv'), ('relationships','database_company_founders_reextrait_88_corrige.csv')]:
    shutil.copy2(source_csvs[src_key], DATA / target_name)

# Dual-method CSV from canonical sessions.
dual_headers = ['session_id','session','candidatures_officielles','lignes_pdf','conversions','retraits','reportes','candidatures_pdf','ecart_pdf_moins_officiel','decision_non_precisee','ajournes','ajournes_hors_pdf','candidatures_corrigees','candidatures_reexamen_pdf','ajournes_hors_lignes_reexamen']
dual_rows = []
for row in aux_rows:
    es = entries_by_session[row['session']]
    c = Counter(e.get('resultat_normalise') for e in es)
    dual_rows.append({'session_id': row['session_id'], 'session': row['session'], 'candidatures_officielles': row['candidatures'], 'lignes_pdf': row['entries'], 'conversions': row['conversions'], 'retraits': row['retraits'], 'reportes': row.get('reportes', 0), 'candidatures_pdf': row['candidatures_pdf_calculees'], 'ecart_pdf_moins_officiel': row['ecart_candidatures_pdf_officiel'], 'decision_non_precisee': c.get('Décision non précisée — motif administratif', 0), 'ajournes': row['ajournes'], 'ajournes_hors_pdf': row['ajournes_hors_pdf'], 'candidatures_corrigees': row['candidatures_corrigees'], 'candidatures_reexamen_pdf': row['candidatures_reexamen_pdf'], 'ajournes_hors_lignes_reexamen': row['ajournes_hors_lignes_reexamen']})
write_csv(DATA / 'dual_candidate_counts_88.csv', dual_headers, dual_rows)

# Canonical SQL with all 3,555 decisions and relational row counts matching the checked CSVs.
company_by_id = {r['company_id']: r for r in company_rows}
session_id_by_period = {s['session']: s['session_id'] for s in sessions}
founder_by_id = {r['founder_id']: r for r in founder_rows}
sql = []
sql.append('-- Startup Act Civic Ledger — SQL canonique 88 sessions, généré le 23/08/2026')
sql.append('PRAGMA foreign_keys = ON;')
sql.append('DROP VIEW IF EXISTS session_official_counts;')
for t in ['company_founders','decisions','founders','companies','sessions','metadata']:
    sql.append(f'DROP TABLE IF EXISTS {t};')
sql += [
    'CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);',
    'CREATE TABLE sessions (session_id TEXT PRIMARY KEY, session TEXT NOT NULL, official_candidatures INTEGER NOT NULL, detailed_entries INTEGER NOT NULL, corrected_candidatures INTEGER NOT NULL, ajournes_hors_pdf INTEGER NOT NULL, official_labels INTEGER NOT NULL, official_prelabels INTEGER NOT NULL, official_conversions INTEGER NOT NULL, official_withdrawals INTEGER NOT NULL, detailed_reportes INTEGER NOT NULL);',
    'CREATE VIEW session_official_counts AS SELECT session_id, session, official_candidatures AS candidatures, detailed_entries AS entries, corrected_candidatures AS candidatures_corrigees, ajournes_hors_pdf, official_labels AS labels, official_prelabels AS preLabels, official_conversions AS conversions, official_withdrawals AS retraits, detailed_reportes AS reportes FROM sessions;',
    'CREATE TABLE companies (company_id TEXT PRIMARY KEY, name TEXT NOT NULL, sector TEXT, session TEXT);',
    'CREATE TABLE founders (founder_id TEXT PRIMARY KEY, name TEXT NOT NULL);',
    'CREATE TABLE decisions (decision_id TEXT PRIMARY KEY, session_id TEXT NOT NULL, company_id TEXT, source_file TEXT, section TEXT, project TEXT, founders_raw TEXT, decision_raw TEXT, result_normalized TEXT, sector TEXT, tour TEXT, after_pitching TEXT, award_or_withdrawal TEXT, comments TEXT, quality_control TEXT);',
    'CREATE TABLE company_founders (decision_id TEXT NOT NULL, company_id TEXT, founder_id TEXT, session_id TEXT, founder_raw TEXT, quality TEXT, PRIMARY KEY(decision_id, founder_id));',
]
for key, value in {
    'scope':'88 sessions S0-S87; source reextraction_88_canonical.json',
    'official_candidatures':sum(int(s['candidatures']) for s in sessions), 'corrected_candidatures':len(entries) + sum(AJOURNES_HORS_PDF.values()), 'ajournes_hors_pdf':sum(AJOURNES_HORS_PDF.values()), 'official_labels':sum(int(s['labels']) for s in sessions),
    'official_prelabels':sum(int(s['preLabels']) for s in sessions), 'detailed_entries':len(entries), 'official_withdrawals':ret_total, 'confirmed_reportes':report_total,
}.items():
    sql.append(f'INSERT INTO metadata(key,value) VALUES ({sql_quote(key)},{sql_quote(value)});')
for s in sessions:
    ah = AJOURNES_HORS_PDF.get(s['session'], 0)
    sql.append('INSERT INTO sessions VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);' % tuple(sql_quote(v) for v in [s['session_id'],s['session'],s['candidatures'],s['entries'],s['entries'] + ah,ah,s['labels'],s['preLabels'],s['conversions'],s['retraits'],s.get('reportes',0)]))
for r in company_rows:
    sql.append('INSERT INTO companies VALUES (%s,%s,%s,%s);' % tuple(sql_quote(r[k]) for k in ['company_id','company_name','sector','session']))
for r in founder_rows:
    sql.append('INSERT INTO founders VALUES (%s,%s);' % tuple(sql_quote(r[k]) for k in ['founder_id','founder_name']))
for e in entries:
    company_id = company_by_key.get((e.get('societe'), e.get('session')), '')
    vals = [e['decision_id'],e['session_id'],company_id,e.get('source_pdf'),e.get('section_pdf'),e.get('projet'),e.get('fondateurs'),e.get('decision'),e.get('resultat_normalise'),e.get('secteur'),e.get('tour_moment'),e.get('apres_pitching'),e.get('session_obtention_retrait'),e.get('commentaires'),e.get('controle_qualite')]
    sql.append('INSERT INTO decisions VALUES (%s);' % ','.join(sql_quote(v) for v in vals))
for r in relationship_rows:
    company_id = company_by_key.get((r['company_name'], r['session']), '')
    founder_id = founder_by_name.get(r['founder_name'], '')
    session_id = session_id_by_period.get(r['session'], '')
    sql.append('INSERT INTO company_founders VALUES (%s);' % ','.join(sql_quote(v) for v in [r['decision_id'],company_id,founder_id,session_id,r['founder_name'],'Extrait PDF/JSON']))
sql_text = '\n'.join(sql) + '\n'
for p in [DATA/'reextraction_88_canonical.sql', DATA/'startup_act_database.sql', DATA/'startup_act_database_88.sql', DATA/'startup_act_database_reextrait_corrige_2026-08-23.sql', PACKAGE/'startup_act_database_reextrait_valide.sql', PACKAGE/'startup_act_database_reextrait_corrige_2026-08-23.sql']:
    p.write_text(sql_text, encoding='utf-8')

# Generate matching SQLite files from the same SQL, then copy to both public and canonical package.
db = sqlite3.connect(':memory:')
db.executescript(sql_text)
for out in [DATA/'founders_database.sqlite', PACKAGE/'founders_database_reextrait_valide.sqlite']:
    if out.exists(): out.unlink()
    dest = sqlite3.connect(out)
    db.backup(dest)
    dest.close()
db.close()

# Keep dashboard authoritative meta and detailed payload synchronized without disturbing other chart sections.
dash_path = DATA / 'dashboard_data.json'
if dash_path.exists():
    dash = json.loads(dash_path.read_text(encoding='utf-8'))
    dash.setdefault('meta', {}).update({'totalCandidatures': sum(int(s['candidatures']) for s in sessions), 'correctedCandidatures': len(entries) + sum(AJOURNES_HORS_PDF.values()), 'ajournesHorsPdf': sum(AJOURNES_HORS_PDF.values()), 'totalLabels': sum(int(s['labels']) for s in sessions), 'totalPreLabels': sum(int(s['preLabels']) for s in sessions), 'totalSessions': len(sessions), 'detailedEntries': len(entries), 'totalCandidaturesCorrigees': len(entries) + sum(AJOURNES_HORS_PDF.values()), 'dataNote': '3 558 candidatures corrigées = 3 555 lignes PDF + 3 ajournés hors PDF ; 3 079 candidatures officielles conservées séparément.', 'lastUpdated': '2026-08-23T00:00:00+00:00'})
    dash['pdfExtracted'] = entries
    source = {s['session']: s for s in sessions}
    for row in dash.get('sessions', []):
        s = source.get(row.get('session'))
        if s:
            row['entries'] = s['entries']; row['detailedEntries'] = s['entries']; row['ajournesHorsPdf'] = AJOURNES_HORS_PDF.get(s['session'], 0); row['candidaturesCorrigees'] = s['entries'] + AJOURNES_HORS_PDF.get(s['session'], 0)
    json_dump(dash_path, dash)

print('SYNCHRONIZED')
print('sessions', len(sessions))
print('entries', len(entries))
print('companies', len(company_rows))
print('founders', len(founder_rows))
print('relationships', len(relationship_rows))
print('official_candidatures', sum(int(s['candidatures']) for s in sessions))
print('official_labels', sum(int(s['labels']) for s in sessions))
print('official_prelabels', sum(int(s['preLabels']) for s in sessions))
print('official_retraits', ret_total)
print('confirmed_reportes', report_total)
print('sql_statements', len(sql))
