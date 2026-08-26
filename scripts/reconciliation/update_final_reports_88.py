from pathlib import Path
import json

REPO = Path('/home/ubuntu/vic-2026-startup-act-python')
D = REPO / 'public' / 'data'

# Keep every Markdown report on the same final statistical contract.
mds = [
    D / 'rapport_academique_pdf_primaire_88_sessions.md',
    D / 'rapport_valeurs_pdf_primaire_88_sessions.md',
    D / 'rapport_academique_startup_act_88_sessions_2026-08-23.md',
    D / 'etude_quantitative' / 'rapport_academique_88_sessions_double_method.md',
    D / 'rapport_academique' / 'rapport_academique_88_sessions_double_method.md',
]

final_note = (
    '> **Périmètre statistique final.** L’étude distingue le compteur institutionnel de **3 079 candidatures officielles**, '
    'le corpus de **3 571 lignes détaillées PDF**, et le compteur corrigé de **3 574 candidatures** obtenu en ajoutant '
    '**3 ajournés hors PDF** signalés par des commentaires officiels (2 en 03/2019 et 1 en 06/2019). '
    'Le commentaire brut 04/2019 est conservé comme provenance mais n’est pas retenu dans le filtre validé faute de dossier confirmé. Ces trois mesures ne sont pas interchangeables. En 07/2019, le commentaire officiel indique « 14 Labels et 1 Prelabel (de la session de mai) » : le PDF compte 29 lignes documentaires, mais le compteur officiel reste 28 candidatures ; la ligne héritée de mai n’est pas une nouvelle candidature. Un dossier Reporté est compté une seule fois dans une série distincte lorsqu’un lien source → session suivante est confirmé, tandis que les deux apparitions restent dans le registre PDF pour documenter le parcours.\n\n'
)

for p in mds:
    if not p.exists():
        continue
    text = p.read_text(encoding='utf-8')
    # Preserve every occurrence that specifically means PDF lines, but correct labels that call them candidatures.
    text = text.replace('3 571 lignes/candidatures documentaires', '3 571 lignes PDF documentaires + 3 ajournés hors PDF = 3 574 candidatures corrigées')
    text = text.replace('3 571 lignes/candidatures', '3 571 lignes PDF + 3 ajournés hors PDF = 3 574 candidatures corrigées')
    text = text.replace('3 571 lignes documentaires retenues pour l’étude', '3 571 lignes PDF + 3 ajournés hors PDF = 3 574 candidatures corrigées')
    text = text.replace('Candidatures selon réexamen PDF | 3 571', 'Candidatures corrigées de l’étude | 3 574')
    text = text.replace('Candidatures corrigées PDF | 3 571', 'Candidatures corrigées de l’étude | 3 574')
    text = text.replace('Candidatures selon réexamen PDF | **3 571**', 'Candidatures corrigées de l’étude | **3 574**')
    text = text.replace('Candidatures selon le réexamen PDF | 3 571', 'Candidatures corrigées de l’étude | 3 574')
    text = text.replace('3 571 candidatures selon le réexamen PDF', '3 574 candidatures corrigées (3 571 lignes PDF + 3 ajournés hors PDF)')
    text = text.replace('3 571 dossiers/candidatures', '3 574 candidatures corrigées (3 571 lignes PDF + 3 ajournés hors PDF)')
    text = text.replace('Les deux séries ne sont pas fusionnées', 'Les trois périmètres ne sont pas fusionnés')
    text = text.replace('Les 4 Ajournés publiés par la page institutionnelle restent une catégorie distincte.', 'Les 3 ajournés validés (03/2019 : 2 ; 06/2019 : 1) restent une catégorie distincte ; le commentaire brut 04/2019 est conservé comme provenance mais n’est pas retenu dans le filtre validé.')
    if 'Périmètre statistique final.' not in text:
        lines = text.splitlines(keepends=True)
        insert_at = 1 if lines and lines[0].startswith('# ') else 0
        text = ''.join(lines[:insert_at]) + final_note + ''.join(lines[insert_at:])
    p.write_text(text, encoding='utf-8')

# Both academic metric manifests expose the same final contract.
for p in [D / 'etude_quantitative' / 'academic_metrics.json', D / 'rapport_academique' / 'academic_metrics.json']:
    if not p.exists():
        continue
    d = json.loads(p.read_text(encoding='utf-8'))
    d.update({
        'sessions': 88,
        'candidatures_officielles': 3079,
        'lignes_pdf_detaillees': 3571,
        'candidatures_reexamen_pdf': 3571,
        'candidatures_corrigees': 3574,
        'ajournes_hors_pdf': 3,
        'labels_officiels': 1356,
        'prelabels_officiels': 641,
        'retraits_officiels': 153,
        'reportes_confirmes': 5,
        'ecart_lignes_pdf_moins_officiel': 492,
        'ecart_candidatures_corrigees_moins_officiel': 495,
        'candidatures_definition': '3 574 corrigées = 3 571 lignes PDF détaillées + 3 ajournés hors PDF (03/2019: 2; 06/2019: 1); le commentaire 04/2019 n’est pas retenu dans le filtre validé ; 3 079 officiel = compteur institutionnel.',
    })
    d['decisions_detaillees_par_resultat'] = {
        'Label accordé': 1232,
        'Label non accordé': 653,
        'Prélabel accordé': 634,
        'Prélabel non accordé': 980,
        'Retrait Label': 46,
        'Reporté': 5,
        'Décision non précisée — motif administratif': 4,
        'Pitch décalé': 1,
    }
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

print('REPORTS_UPDATED', sum(p.exists() for p in mds), 'METRICS_UPDATED', 2)
