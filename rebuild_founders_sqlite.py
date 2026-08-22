from pathlib import Path
import csv, sqlite3, shutil
root=Path('/home/ubuntu/vic-2026-startup-act-4339943')
data=root/'public/data/reextraction_validee_88'
out=root/'public/data/founders_database.sqlite'
canonical=data/'founders_database_reextrait_valide.sqlite'

def rows(name):
    with (data/name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))

sessions=rows('database_sessions_reextrait.csv')
companies=rows('database_companies_reextrait.csv')
founders=rows('database_founders_reextrait.csv')
relations=rows('database_company_founders_reextrait.csv')
decisions=rows('database_entrees_reextrait.csv')
if len(sessions)!=88 or len(decisions)!=3528:
    raise SystemExit(f'Unexpected canonical sizes: sessions={len(sessions)} decisions={len(decisions)}')
# Build in a temporary database so an interrupted run never leaves a partial SQLite file.
tmp=out.with_suffix('.tmp.sqlite')
if tmp.exists(): tmp.unlink()
con=sqlite3.connect(tmp)
con.execute('PRAGMA foreign_keys=ON')
con.executescript('''
CREATE TABLE sessions (session_id TEXT PRIMARY KEY, session TEXT NOT NULL, candidatures INTEGER NOT NULL, entries INTEGER NOT NULL, labels INTEGER NOT NULL, prelabels INTEGER NOT NULL, conversions INTEGER NOT NULL, retraits INTEGER NOT NULL, reportes INTEGER NOT NULL, new_labels INTEGER NOT NULL, taux_pct REAL, candidatures_definition TEXT);
CREATE TABLE companies (company_id TEXT PRIMARY KEY, name TEXT NOT NULL, sector TEXT, sessions TEXT);
CREATE TABLE founders (founder_id TEXT PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE company_founders (company_id TEXT NOT NULL, founder_id TEXT NOT NULL, session_id TEXT NOT NULL, founder_raw TEXT, quality TEXT, PRIMARY KEY(company_id, founder_id, session_id));
CREATE TABLE decisions (decision_id TEXT PRIMARY KEY, session_id TEXT NOT NULL, session TEXT NOT NULL, line INTEGER, source_pdf TEXT, section_pdf TEXT, societe TEXT, projet TEXT, fondateurs TEXT, secteur TEXT, decision TEXT, resultat_normalise TEXT, type_label TEXT, tour_moment TEXT, apres_pitching TEXT, session_obtention_retrait TEXT, commentaires TEXT, controle_qualite TEXT);
CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
''')
con.executemany('INSERT INTO sessions VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', [
    (f'S{i}',r['session'],int(r['candidatures']),int(r['entries']),int(r['labels']),int(r['preLabels']),int(r['conversions']),int(r['retraits']),int(r['reportes']),int(r['newLabels']),float(r['tauxPct']) if r['tauxPct'] else None,r['candidatures_definition']) for i,r in enumerate(sessions)
])
con.executemany('INSERT INTO companies VALUES (?,?,?,?)', [(r['company_id'],r['name'],r['sector'],r['sessions']) for r in companies])
con.executemany('INSERT INTO founders VALUES (?,?)', [(r['founder_id'],r['name']) for r in founders])
seen=set(); rel_rows=[]
for r in relations:
    key=(r['company_id'],r['founder_id'],r['session_id'])
    if key in seen: continue
    seen.add(key); rel_rows.append((r['company_id'],r['founder_id'],r['session_id'],r['founder_raw'],r['quality']))
con.executemany('INSERT INTO company_founders VALUES (?,?,?,?,?)', rel_rows)
con.executemany('INSERT INTO decisions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', [
    (r['decision_id'],r['session_id'],r['session'],int(r['line']) if r['line'] else None,r['source_pdf'],r['section_pdf'],r['societe'],r['projet'],r['fondateurs'],r['secteur'],r['decision'],r['resultat_normalise'],r['type_label'],r['tour_moment'],r['apres_pitching'],r['session_obtention_retrait'],r['commentaires'],r['controle_qualite']) for r in decisions
])
meta={
    'scope':'88 sessions S0-S87; source CSV reextraction_validee_88',
    'official_candidatures':str(sum(int(r['candidatures']) for r in sessions)),
    'official_labels':str(sum(int(r['labels']) for r in sessions)),
    'official_prelabels':str(sum(int(r['preLabels']) for r in sessions)),
    'detailed_entries':str(sum(int(r['entries']) for r in sessions)),
    'official_withdrawals':str(sum(int(r['retraits']) for r in sessions)),
    'confirmed_reportes':str(sum(int(r['reportes']) for r in sessions)),
    'raw_relationship_rows':str(len(relations)),
    'duplicate_relationship_rows_removed':str(len(relations)-len(rel_rows)),
}
con.executemany('INSERT INTO metadata VALUES (?,?)', meta.items())
con.commit()
checks={
    'sessions':con.execute('select count(*) from sessions').fetchone()[0],
    'companies':con.execute('select count(*) from companies').fetchone()[0],
    'founders':con.execute('select count(*) from founders').fetchone()[0],
    'company_founders':con.execute('select count(*) from company_founders').fetchone()[0],
    'decisions':con.execute('select count(*) from decisions').fetchone()[0],
    'decision_ids_distinct':con.execute('select count(distinct decision_id) from decisions').fetchone()[0],
    'official_candidatures':con.execute("select value from metadata where key='official_candidatures'").fetchone()[0],
}
con.close()
if checks['sessions']!=88 or checks['decisions']!=3528 or checks['decisions']!=checks['decision_ids_distinct'] or checks['official_candidatures']!='3079':
    raise SystemExit(f'SQLite validation failed: {checks}')
shutil.copy2(tmp, out)
shutil.copy2(tmp, canonical)
tmp.unlink()
print(checks)
print('canonical_sqlite',out)
