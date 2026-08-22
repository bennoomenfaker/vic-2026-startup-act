from pathlib import Path
import csv, re, sqlite3
root=Path('/home/ubuntu/vic-2026-startup-act-4339943')
data=root/'public/data/reextraction_validee_88'
source=(data/'startup_act_database_reextrait_valide.sql').read_text(encoding='utf-8')
# Replace the NULL session primary keys using the authoritative S0..S87 order.
rows=list(csv.DictReader((data/'database_sessions_reextrait.csv').open(encoding='utf-8-sig'), delimiter=';'))
if len(rows)!=88: raise SystemExit(f'expected 88 sessions, got {len(rows)}')
for i,row in enumerate(rows):
    session=row['session']
    old=f"INSERT INTO session_official_counts VALUES (NULL,'{session}'"
    new=f"INSERT INTO session_official_counts VALUES ('S{i}','{session}'"
    if old not in source: raise SystemExit(f'missing official count for {session}')
    source=source.replace(old,new,1)
# Add the relationship table, which the source SQL schema defines but the source export omitted.
def q(v):
    return 'NULL' if v is None or v=='' else "'"+str(v).replace("'","''")+"'"
rels=[]
seen=set()
duplicate_relations=0
with (data/'database_company_founders_reextrait.csv').open(encoding='utf-8-sig', newline='') as f:
    for r in csv.DictReader(f, delimiter=';'):
        key=tuple(r[k] for k in ['company_id','founder_id','session_id'])
        if key in seen:
            duplicate_relations += 1
            continue
        seen.add(key)
        rels.append("INSERT OR IGNORE INTO company_founders (company_id,founder_id,session_id,founder_raw,quality) VALUES (%s,%s,%s,%s,%s);" % tuple(q(r[k]) for k in ['company_id','founder_id','session_id','founder_raw','quality']))
# Insert relations after the existing founder rows and before the final commit if present.
source += '\n-- Relations entreprise-fondateur extraites des 88 PDFs (clé composite).\n' + '\n'.join(rels) + '\n'
out=root/'public/data/startup_act_database.sql'
out.write_text(source,encoding='utf-8')
# Deterministic integrity check using SQLite in memory.
con=sqlite3.connect(':memory:')
con.executescript(source)
checks={
 'sessions':con.execute('select count(*) from session_official_counts').fetchone()[0],
 'decisions':con.execute('select count(*) from decisions').fetchone()[0],
 'decision_ids_distinct':con.execute('select count(distinct decision_id) from decisions').fetchone()[0],
 'companies':con.execute('select count(*) from companies').fetchone()[0],
 'founders':con.execute('select count(*) from founders').fetchone()[0],
 'company_founders':con.execute('select count(*) from company_founders').fetchone()[0],
 'official_candidatures':con.execute('select sum(official_candidatures) from session_official_counts').fetchone()[0],
 'official_labels':con.execute('select sum(official_labels) from session_official_counts').fetchone()[0],
 'official_prelabels':con.execute('select sum(official_prelabels) from session_official_counts').fetchone()[0],
 'detailed_entries':con.execute('select sum(detailed_entries) from session_official_counts').fetchone()[0],
 'reportes':con.execute('select sum(detailed_reportes) from session_official_counts').fetchone()[0],
}
checks['duplicate_relationship_rows_removed']=duplicate_relations
print(checks)
if checks['sessions']!=88 or checks['decisions']!=checks['decision_ids_distinct'] or checks['official_candidatures']!=3079 or checks['official_labels']!=1356 or checks['official_prelabels']!=641 or checks['detailed_entries']!=3528:
    raise SystemExit('canonical SQL integrity check failed')
