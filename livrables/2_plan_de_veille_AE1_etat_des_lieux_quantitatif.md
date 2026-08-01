# PLAN DE VEILLE — AE1 · ÉTAT DES LIEUX QUANTITATIF

**Projet national – Livre Blanc Startup Act** · **Responsable : Faker BEN NOOMEN**
**Équipe : classe VIC — MP 2ème année (ESEN × ISCAE Manouba)** · **Version 1.0 · Juillet 2026**

| Axe ou sous-axe | Hypothèse | Question de veille | Informations recherchées | Sources envisagées | Méthodes | Outils |
|---|---|---|---|---|---|---|
| **AE1.1 — Fiabilité des données officielles** | Les données du tableau `/sessions` de startup.gov.tn contiennent des erreurs de comptage (labels/prélabels) sur 20 des 85 sessions. | Quelle est la fiabilité réelle des données de labellisation publiées ? | Valeurs exactes de labels et prélabels pour les 85 sessions, commentaires, taux d'acceptation et d'échec. | startup.gov.tn ; PDF officiels des 85 sessions. | Extraction PDF ; parsing positionnel ; comparaison scrapé vs PDF. | Python (`parse_pdfs_v7.py`) ; tableur. |
| **AE1.2 — Volumétrie globale** | Le volume réel de labels (1 311) diffère du chiffre publié (1 324) ; de même pour les prélabels (623 vs 617). | Quels sont les volumes réels de candidatures, labels et prélabels sur 2019-2026 ? | Totaux par session et par année ; répartition des labels. | PDF officiels ; base des startups labellisées. | Agrégation ; contrôle de cohérence (sommes croisées). | Python ; JSON ; dashboard. |
| **AE1.3 — Taux d'acceptation** | Le taux d'acceptation affiché diffère du taux réel pour certaines sessions. | Quelle est l'évolution réelle du taux d'acceptation du programme ? | Taux exact (labels/candidatures) par session et par année. | PDF officiels ; rapports annuels du programme. | Calcul exact ; arrondi contrôlé à 1 décimale. | Python ; Chart.js. |
| **AE1.4 — Parcours prélabel → label** | Une part importante des labels provient de la conversion de prélabels accordés lors de sessions antérieures. | Combien de prélabels sont convertis en labels et quelle est la part des labels issus de conversions ? | Nombre de conversions par session ; taux de conversion global (80,6 %) ; part des labels issus de conversions (38,3 %). | PDF officiels (commentaires de session). | Analyse de parcours ; comptage. | Python ; `parcours.json` ; dashboard. |
| **AE1.5 — Retraits de labels** | Des labels sont régulièrement retirés (mortalité du label). | Combien de labels ont été retirés et pour quels motifs ? | Nombre de retraits (140) ; motifs ; sessions concernées. | PDF officiels ; communiqués ANPR. | Collecte ; classification des motifs. | Python ; tableur. |
| **AE1.6 — Saisonnalité** | Les labellisations suivent une saisonnalité marquée (décembre et mai actifs, juillet faible). | Existe-t-il une saisonnalité des labellisations ? | Labels par mois et par année sur la période. | Dashboard ; PDF officiels. | Analyse temporelle. | Python ; Chart.js. |
| **AE1.7 — Répartition sectorielle et géographique** | La concentration sectorielle est modérée (Top 4 = 51,6 %) et les startups sont concentrées dans le Grand Tunis (48 %). | Quels secteurs, années de création et régions dominent la labellisation ? | Répartition par secteur, par année de création et par région. | Base des startups labellisées ; rapports annuels. | Analyse de répartition ; benchmark. | Python ; tableur ; Leaflet. |

---

## Indicateurs de référence (issus du travail de collecte et de correction)

| Indicateur | Valeur |
|---|---|
| Sessions analysées | 85 |
| Candidatures | 1 824 |
| Labels (corrigés, PDF officiels) | **1 311** *(publié : 1 324)* |
| Prélabels (corrigés) | **623** *(publié : 617)* |
| Conversions prélabel → label | 502 |
| Taux de conversion des prélabels | **80,6 %** |
| Part des labels issus de conversions | **38,3 %** |
| Retraits de labels | **140** |
| Sessions corrigées / vérifiées | 20 / 85 · vérification 85/85 |
| Taux d'acceptation | 61,7 % (2019) → 36,3 % (2025) |
