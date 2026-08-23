from pathlib import Path
import json

REPO=Path('/home/ubuntu/vic-2026-startup-act-4339943')
D=REPO/'public'/'data'
mds=[D/'etude_quantitative'/'rapport_academique_88_sessions_double_method.md',D/'rapport_academique'/'rapport_academique_88_sessions_double_method.md',D/'rapport_academique_startup_act_88_sessions_2026-08-23.md']
for p in mds:
    text=p.read_text(encoding='utf-8')
    text=text.replace('3 531 dossiers/candidatures selon le réexamen PDF de l’étude','3 555 lignes détaillées selon le corpus PDF réextrait')
    text=text.replace('3 531 dossiers selon le réexamen PDF de l’étude','3 555 lignes détaillées selon le corpus PDF réextrait')
    text=text.replace('3 531 dossiers','3 555 lignes détaillées')
    text=text.replace('3 531','3 555')
    text=text.replace('3 528 décisions','3 555 décisions détaillées')
    text=text.replace('3 528 lignes','3 555 lignes')
    text=text.replace('3 528','3 555')
    text=text.replace('4 Reporté','5 Reporté')
    text=text.replace('4 retraits, 4 Reporté','4 retraits, 5 Reporté')
    text=text.replace('1 201 Labels accordés, 659 Labels non accordés, 636 Prélabels accordés, 982 Prélabels non accordés, 45 retraits, 4 Reporté et 1 Pitch décalé','1 232 Labels accordés, 653 Labels non accordés, 634 Prélabels accordés, 980 Prélabels non accordés, 46 retraits, 5 Reporté, 4 décisions administratives non précisées et 1 Pitch décalé')
    text=text.replace('3 555 lignes documentaires documentaires','3 555 lignes documentaires')
    p.write_text(text,encoding='utf-8')

for p in [D/'etude_quantitative'/'academic_metrics.json',D/'rapport_academique'/'academic_metrics.json']:
    d=json.loads(p.read_text(encoding='utf-8'))
    d['sessions']=88
    d['candidatures_officielles']=3079
    d['candidatures_reexamen_pdf']=3555
    d['lignes_pdf_detaillees']=3555
    d['labels_officiels']=1356
    d['prelabels_officiels']=641
    d['retraits_officiels']=153
    d['reportes_confirmes']=5
    d['decisions_detaillees_par_resultat']={'Label accordé':1232,'Label non accordé':653,'Prélabel accordé':634,'Prélabel non accordé':980,'Retrait Label':46,'Reporté':5,'Décision non précisée — motif administratif':4,'Pitch décalé':1}
    d['ecart_lignes_pdf_moins_officiel']=476
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('REPORTS_UPDATED',len(mds),'METRICS_UPDATED',2)
