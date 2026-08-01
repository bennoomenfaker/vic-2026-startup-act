#!/usr/bin/env python3
"""Génère le Plan de veille AE1 (XLSX) — État des lieux quantitatif."""
import xlsxwriter

OUT = 'livrables/2_plan_de_veille_AE1_etat_des_lieux_quantitatif.xlsx'

HEADERS = ['Axe ou sous-axe', 'Hypothèse', 'Question de veille',
           'Informations recherchées', 'Sources envisagées', 'Méthodes', 'Outils']

ROWS = [
    ['AE1.1 — Fiabilité des données officielles',
     'Les données du tableau /sessions de startup.gov.tn contiennent des erreurs de comptage (labels/prélabels) sur 20 des 85 sessions.',
     'Quelle est la fiabilité réelle des données de labellisation publiées ?',
     'Valeurs exactes de labels et prélabels pour les 85 sessions, commentaires, taux d\'acceptation et d\'échec.',
     'startup.gov.tn ; PDF officiels des 85 sessions.',
     'Extraction PDF ; parsing positionnel ; comparaison scrapé vs PDF.',
     'Python (parse_pdfs_v7.py) ; tableur.'],
    ['AE1.2 — Volumétrie globale',
     'Le volume réel de labels (1 311) diffère du chiffre publié (1 324) ; de même pour les prélabels (623 vs 617).',
     'Quels sont les volumes réels de candidatures, labels et prélabels sur 2019-2026 ?',
     'Totaux par session et par année ; répartition des labels.',
     'PDF officiels ; base des startups labellisées.',
     'Agrégation ; contrôle de cohérence (sommes croisées).',
     'Python ; JSON ; dashboard.'],
    ['AE1.3 — Taux d\'acceptation',
     'Le taux d\'acceptation affiché diffère du taux réel pour certaines sessions.',
     'Quelle est l\'évolution réelle du taux d\'acceptation du programme ?',
     'Taux exact (labels/candidatures) par session et par année.',
     'PDF officiels ; rapports annuels du programme.',
     'Calcul exact ; arrondi contrôlé à 1 décimale.',
     'Python ; Chart.js.'],
    ['AE1.4 — Parcours prélabel → label',
     'Une part importante des labels provient de la conversion de prélabels accordés lors de sessions antérieures.',
     'Combien de prélabels sont convertis en labels et quelle est la part des labels issus de conversions ?',
     'Nombre de conversions par session ; taux de conversion global (80,6 %) ; part des labels issus de conversions (38,3 %).',
     'PDF officiels (commentaires de session).',
     'Analyse de parcours ; comptage.',
     'Python ; parcours.json ; dashboard.'],
    ['AE1.5 — Retraits de labels',
     'Des labels sont régulièrement retirés (mortalité du label).',
     'Combien de labels ont été retirés et pour quels motifs ?',
     'Nombre de retraits (140) ; motifs ; sessions concernées.',
     'PDF officiels ; communiqués ANPR.',
     'Collecte ; classification des motifs.',
     'Python ; tableur.'],
    ['AE1.6 — Saisonnalité',
     'Les labellisations suivent une saisonnalité marquée (décembre et mai actifs, juillet faible).',
     'Existe-t-il une saisonnalité des labellisations ?',
     'Labels par mois et par année sur la période.',
     'Dashboard ; PDF officiels.',
     'Analyse temporelle.',
     'Python ; Chart.js.'],
    ['AE1.7 — Répartition sectorielle et géographique',
     'La concentration sectorielle est modérée (Top 4 = 51,6 %) et les startups sont concentrées dans le Grand Tunis (48 %).',
     'Quels secteurs, années de création et régions dominent la labellisation ?',
     'Répartition par secteur, par année de création et par région.',
     'Base des startups labellisées ; rapports annuels.',
     'Analyse de répartition ; benchmark.',
     'Python ; tableur ; Leaflet.'],
]

wb = xlsxwriter.Workbook(OUT)
ws = wb.add_worksheet('Plan de veille')

ws.set_column('A:A', 34)
ws.set_column('B:B', 52)
ws.set_column('C:C', 50)
ws.set_column('D:D', 50)
ws.set_column('E:E', 40)
ws.set_column('F:F', 38)
ws.set_column('G:G', 32)

title = wb.add_format({'bold': True, 'font_size': 14, 'font_color': '#16213e'})
sub = wb.add_format({'italic': True, 'font_color': '#666666', 'font_size': 10, 'text_wrap': True})
header = wb.add_format({'bold': True, 'bg_color': '#16213e', 'font_color': 'white',
                        'text_wrap': True, 'valign': 'vcenter', 'border': 1})
cell = wb.add_format({'text_wrap': True, 'valign': 'top', 'border': 1})
cell_bold = wb.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'border': 1})

ws.merge_range('A1:G1', 'Axe 1 : État des lieux quantitatif du Startup Act', title)
ws.merge_range('A2:G2', 'Plan de veille AE1 — État des lieux quantitatif', sub)
ws.merge_range('A3:G3',
               'Projet national – Livre Blanc Startup Act · Responsable : Faker BEN NOOMEN · '
               'Équipe : classe VIC — MP 2ème année (ESEN × ISCAE Manouba) · Version 1.0 · Juillet 2026',
               sub)

for c, h in enumerate(HEADERS):
    ws.write(4, c, h, header)

for r, row in enumerate(ROWS, start=5):
    for c, val in enumerate(row):
        fmt = cell_bold if c == 0 else cell
        ws.write(r, c, val, fmt)

ws.set_row(4, 28)
wb.close()
print('XLSX généré :', OUT)
