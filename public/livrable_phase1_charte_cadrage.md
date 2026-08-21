# CHARTE DE CADRAGE D'UN AXE DE VEILLE
## Projet national – Livre Blanc Startup Act

---

## 1. Informations générales

| Élément | Réponse |
|---------|---------|
| **Axe d'étude** | **Axe 1 — État des lieux quantitatif du Startup Act** |
| **Responsable** | [Faker BEN NOOMEN] |
| **Membres** | [Équipe Axe 1] |
| **Date** | Juillet 2026 |
| **Version** | V1 |

---

## 2. Contexte et justification

### Situation actuelle
Le Startup Act tunisien, lancé en avril 2019, a permis la labellisation de **922 startups uniques** à travers **85 sessions** (2019-2026). Avec **2 958 candidatures** reçues, **1 324 labels** et **617 pré-labels** accordés, le dispositif a généré une masse considérable de données qui n'a jamais été consolidée ni analysée de manière systématique dans un tableau de bord public et interactif.

### Pourquoi cet axe est important
Huit ans après son lancement, aucune photographie complète et consolidée de l'écosystème n'existe publiquement. Les données sont dispersées entre :
- Les rapports annuels (2019-2020, 2020, 2021) — partiels et non mis à jour
- Les PDFs de sessions (85 fichiers) — non structurés
- La base de données startups (database.csv) — brute, sans analyse
- Le site web startup.gov.tn — données dynamiques non exportables

### Principaux enjeux
1. **Visibilité** : Offrir une vision claire et actualisée de l'écosystème startup tunisien
2. **Aide à la décision** : Fournir aux décideurs (ATVIC, ministères, investisseurs) des indicateurs fiables
3. **Transparence** : Rendre publiques les données du Startup Act
4. **Évaluation** : Mesurer l'atteinte des objectifs initiaux du dispositif
5. **Benchmark** : Permettre la comparaison avec d'autres écosystèmes

---

## 3. Besoin décisionnel et problématique

### Besoin décisionnel
Les décideurs (ATVIC, Ministère des Technologies, investisseurs, partenaires internationaux) ont besoin de **données quantitatives fiables, actualisées et agrégées** pour :
- Évaluer la performance du Startup Act
- Identifier les déséquilibres territoriaux et sectoriels
- Guider les décisions d'investissement et d'accompagnement
- Justifier les demandes de financement auprès des bailleurs (UE, Banque Mondiale, GIZ)
- Préparer les réformes du dispositif (phase 2 du Startup Act)

### Problématique
**Quels sont les résultats quantitatifs du Startup Act tunisien après 7 ans d'activité (2019-2026), et comment ces données peuvent-elles éclairer les décisions stratégiques pour améliorer le dispositif ?**

☐ Orientée décision ✓
☐ Claire ✓
☐ Pas descriptive ✓
☐ Pas trop large ✓

---

## 4. Objectifs

### Objectif général
**Établir un état des lieux quantitatif exhaustif, actualisé et interactif du Startup Act tunisien** couvrant l'ensemble des sessions de labellisation, des startups labellisées et des indicateurs clés de performance.

### Objectifs spécifiques

| # | Objectif | Verbe | Répond à la problématique | Réaliste |
|---|----------|-------|--------------------------|----------|
| OS1 | **Analyser** l'évolution temporelle des 85 sessions de labellisation (2019-2026) | ✓ | ✓ | ✓ |
| OS2 | **Cartographier** les 922 startups labellisées par secteur, région, année et genre | ✓ | ✓ | ✓ |
| OS3 | **Mesurer** les taux de conversion Pré-Label → Label, de rétention et de retrait | ✓ | ✓ | ✓ |
| OS4 | **Identifier** les disparités territoriales et sectorielles dans l'accès au label | ✓ | ✓ | ✓ |
| OS5 | **Produire** un tableau de bord interactif (dashboard) avec les KPIs clés | ✓ | ✓ | ✓ |

---

## 5. Périmètre

| Élément | Réponse |
|---------|---------|
| **Géographique** | Tunisie (24 gouvernorats, 6 régions) |
| **Temporel** | Avril 2019 → Mars 2026 (85 sessions, 7 ans) |
| **Thématique** | Sessions de labellisation, startups labellisées, données démographiques (secteur, région, genre, année), indicateurs de performance du dispositif |
| **Acteurs concernés** | Startups labellisées, ATVIC, Ministère des Technologies, bailleurs (UE, BM, GIZ), structures d'accompagnement, investisseurs |
| **Hors périmètre** | Analyse qualitative des startups, évaluation d'impact détaillée (Axe 5), benchmark international (Axe 6), analyse juridique (Axe 2), analyse des mécanismes de financement (Axe 3) |

☐ Périmètre clair ✓
☐ Pas de chevauchement avec un autre axe ✓

---

## 6. Plan de veille

### Sous-axes identifiés

| Sous-axe | Description |
|----------|-------------|
| SA1.1 | Analyse des sessions : évolution des candidatures, labels, pré-labels, taux d'acceptation |
| SA1.2 | Profil des startups : secteurs, gouvernorats, années de création |
| SA1.3 | Dynamique temporelle : labels par mois, saisonnalité, tendances |
| SA1.4 | Genre et diversité : répartition hommes/femmes fondateurs |
| SA1.5 | Cycle de vie des labels : actifs, expirés, retirés, taux de conversion |

### Tableau de veille

| Sous-axe | Hypothèse | Question de veille | Infos recherchées | Sources envisagées | Méthodes | Outils |
|----------|-----------|-------------------|-------------------|--------------------|----------|--------|
| SA1.1 | Le taux d'acceptation baisse avec la maturité du dispositif | Comment évolue le taux d'acceptation des candidatures depuis 2019 ? | Candidatures/labels/pré-labels par session et par an | `dashboard_data.json` (sessions, yearly), `startup.gov.tn.fr.results`, site startup.gov.tn | Analyse statistique, régression temporelle | Python (Pandas), Excel, Google Sheets |
| SA1.1 | Le nombre de sessions s'est stabilisé à 12/an | Y a-t-il une saisonnalité dans les sessions ? | Dates des 85 sessions, mois avec le + de labels | `dashboard_data.json` (byLabelMonth), PDFs sessions | Analyse de fréquence mensuelle | Python, Chart.js |
| SA1.2 | Le Grand Tunis concentre la majorité des startups | Quelle est la répartition géographique des startups labellisées ? | Startups par gouvernorat, région, % Grand Tunis vs régions | `database.csv` (colonne gouvernorat), `database_startups.json` | Cartographie, analyse de concentration | Leaflet.js, Python (GeoPandas), QGIS |
| SA1.2 | Le secteur "Business Software" domine largement | Quels sont les secteurs d'activité les plus représentés ? | Répartition sectorielle, évolution par année | `dashboard_data.json` (sectors), `database.csv` | Analyse de distribution, Pareto | Python, Chart.js (pie/bar) |
| SA1.3 | Le pic de créations était en 2020 | Quelle est la distribution des startups par année de création ? | Année de création des 922 startups | `dashboard_data.json` (byCreationYear) | Histogramme, analyse de tendance | Python, Chart.js |
| SA1.4 | La proportion de femmes fondatrices reste faible | Quelle est la part des femmes dans les équipes fondatrices ? | Genre des fondateurs (2021: 21%, 2019: 35%) | Rapports annuels PDF (2019-2020, 2020, 2021), enquêtes | Analyse de genre, évolution temporelle | Python (texte), Google Scholar |
| SA1.5 | Beaucoup de startups perdent leur label après 2-3 ans | Quel est le taux de rétention et de retrait des labels ? | Labels actifs/expirés/retirés, durée de vie moyenne | `dashboard_data.json` (pdfExtracted: 190 retraits) | Analyse de survie, cohorte | Python (lifelines), Excel |

---

## 7. Organisation de la veille

### Sources prioritaires

| Source | Pourquoi ? | Priorité (5→1) |
|--------|------------|:--------------:|
| `dashboard_data.json` | Données agrégées complètes (sessions, yearly, sectors, byCreationYear, byLabelMonth, pdfExtracted) | 5 |
| `database.csv` / `database_startups.json` | Base brute des 922 startups avec détails (nom, secteur, année, fondateurs, contact) | 5 |
| `sessions.json` | Détail des 85 sessions avec statuts, commentaires | 4 |
| PDFs session-pdfs/ (85 fichiers) | Rapports officiels de chaque session avec liste nominative | 4 |
| Rapports annuels (2019-2020, 2020, 2021) | Données historiques, enquêtes, analyses qualitatives | 4 |
| `annual_reports_parsed.json` | Métriques extraites automatiquement des 3 rapports | 3 |
| startup.gov.tn (site officiel) | Source primaire, données les plus récentes (2026) | 5 |
| Google Scholar / Cairn | Littérature académique sur le Startup Act | 2 |
| Banque Mondiale / EU / GIZ | Rapports des partenaires internationaux | 2 |

### Outils

| Outil | Utilisation |
|-------|-------------|
| ☐ **Recherche documentaire** | Analyse des PDFs et rapports |
| ☐ **Google Scholar** | Recherche académique |
| ☐ **Base réglementaire** | Textes de loi, décrets |
| ☐ **Questionnaire** | Enquête auprès des startups (Phase 2) |
| ☐ **Entretiens** | Entretiens avec acteurs clés (Phase 3) |
| ☐ **Benchmark** | Comparaison internationale (Axe 6) |
| ☐ **Tableau Excel / Google Sheets** | Consolidation et suivi |
| ☒ **Python (Pandas, )** | Analyse de données, extraction PDF |
| ☒ **JavaScript (Chart.js, Leaflet)** | Visualisation interactive |
| ☐ **Google Data Studio / Power BI** | Dashboard complémentaire |

---

## 8. Livrables attendus

| Livrable | Format | Échéance |
|----------|--------|----------|
| Charte de Cadrage de l'Axe 1 | Google Doc / Markdown | Phase 1 (10/08) |
| Plan de veille détaillé | Google Sheet | Phase 1 (10/08) |
| Base de données consolidée et nettoyée | CSV / JSON | Phase 3 (20/09) |
| Analyse statistique descriptive | Rapport PDF | Phase 4 (19/10) |
| Tableau de bord interactif (dashboard) | Application Web | Phase 4 (19/10) |
| Cartographie interactive des startups | Carte Leaflet | Phase 4 (19/10) |
| Section quantitative du Livre Blanc | Chapitre | Phase 5 (02/11) |

---

## 9. Risques

| Risque | Solution prévue |
|--------|----------------|
| Données incomplètes (certains champs CSV manquants) | Croisement avec les PDFs de sessions et les rapports annuels |
| PDFs sessions non extractibles (scannés) | OCR avec Tesseract ou transcription manuelle |
| Évolution du site startup.gov.tn (changement API) | Utiliser les données déjà collectées comme base stable |
| Doublons dans la base startups (ex: "xgol") | Dédoublonnage par nom normalisé et vérification manuelle |
| Informations obsolètes (site web, email) | Indiquer la date de collecte, prévoir mise à jour |
| Hétérogénéité des données entre sources CSV/JSON/PDF | Établir une matrice de correspondance et prioriser les sources officielles |

---

## 10. Validation Qualité

☐ Le contexte est clair. ✓
☐ Le besoin décisionnel est identifié. ✓
☐ La problématique est stratégique. ✓
☐ Les objectifs répondent à la problématique. ✓
☐ Le périmètre est défini. ✓
☐ Les questions de veille sont pertinentes. ✓
☐ Les informations recherchées sont clairement identifiées. ✓
☐ Les sources sont fiables. ✓
☐ Les méthodes sont adaptées. ✓
☐ Les responsabilités sont réparties. ✓ (À confirmer)
☐ Les livrables sont définis. ✓

### Avis du Responsable Qualité

☐ Validé
☐ À compléter

**Commentaires :**
- Données quantitatives disponibles et vérifiées : 85 sessions, 922 startups, 1324 labels, 617 pré-labels
- Sources officielles confirmées (startup.gov.tn)
- Base de travail solide pour passer à la Phase 2 (conception du dispositif de collecte)

**Signature :**
[Nom du Responsable Qualité]

---

## Données clés disponibles pour l'Axe 1

### Sessions (2019-2026)

| Année | Sessions | Candidatures | Labels | Pré-Labels | Taux d'acceptation |
|-------|:--------:|:------------:|:------:|:----------:|:------------------:|
| 2019 | 10 | 311 | 192 | 59 | 61,7% |
| 2020 | 12 | 407 | 209 | 108 | 51,4% |
| 2021 | 12 | 478 | 243 | 103 | 50,8% |
| 2022 | 12 | 398 | 175 | 90 | 44,0% |
| 2023 | 12 | 395 | 165 | 79 | 41,8% |
| 2024 | 12 | 440 | 144 | 74 | 32,7% |
| 2025 | 12 | 421 | 153 | 87 | 36,3% |
| 2026 | 3 | 108 | 43 | 17 | 39,8% |
| **Total** | **85** | **2 958** | **1 324** | **617** | **44,8%** |

### Top secteurs

| Secteur | Startups | % |
|---------|:--------:|:-:|
| Business Software & Services | 212 | 23,0% |
| Commerce & Shopping | 95 | 10,3% |
| HealthTech | 86 | 9,3% |
| EdTech | 83 | 9,0% |
| Ad Tech & Creative Tech | 82 | 8,9% |
| Fintech | 54 | 5,9% |
| Agritech | 49 | 5,3% |
| Mobility | 49 | 5,3% |
| Autres (10 secteurs) | 212 | 23,0% |

### Répartition temporelle (création des startups)

| Année | Startups créées |
|:-----:|:--------------:|
| 2011 | 1 |
| 2012 | 5 |
| 2013 | 6 |
| 2014 | 13 |
| 2015 | 16 |
| 2016 | 31 |
| 2017 | 42 |
| 2018 | 65 |
| 2019 | 144 |
| 2020 | 214 |
| 2021 | 160 |
| 2022 | 103 |
| 2023 | 73 |
| 2024 | 33 |
| 2025 | 16 |

### Données Rapports Annuels (extraites)

| Indicateur | 2019-2020 | 2020 | 2021 |
|-----------|:---------:|:----:|:----:|
| Pages du rapport | 44 | 82 | 159 |
| Candidatures | 416 | 718 | — |
| Emplois créés | — | 3 222 | — |
| Femmes fondatrices | 35% | — | 21% |
| Investissements | — | 2,1 mTND | 157 M USD |
| Startups B2B | 70% | — | 65% |
| Startups à l'international | — | — | 45% |
| Grand Tunis | — | — | 48% |
