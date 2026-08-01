# CHARTE DE CADRAGE D'UN AXE DE VEILLE

**Projet national – Livre Blanc Startup Act** · **Axe AE1 – État des lieux quantitatif**

---

## 1. Informations générales

| Élément      | À compléter |
|--------------|-------------|
| **Axe d'étude** | AE1 — État des lieux quantitatif du programme Startup Act tunisien |
| **Responsable** | Faker BEN NOOMEN |
| **Membres** | Équipe de la classe VIC — étudiants du Mastère Professionnel 2ème année VIC (ESEN Manouba × ISCAE Manouba) |
| **Date** | Juillet 2026 |
| **Version** | 1.0 |

---

## 2. Contexte et justification

**Situation actuelle.** Le programme Startup Act tunisien, institué par la Loi n° 2018-20 du 17 avril 2018, vise à favoriser la création et le développement de startups à fort potentiel par un dispositif de labellisation. Depuis 2019, **85 sessions de labellisation** ont été organisées sur la période 2019-2026. Le label startup conditionne l'accès aux avantages fiscaux et sociaux ainsi qu'aux dispositifs de financement du programme.

**Pourquoi cet axe est-il important ?** L'évaluation du dispositif repose sur les chiffres publiés par la plateforme officielle **startup.gov.tn**. Or, notre état des lieux a révélé que ces données présentent des **incohérences et des erreurs de comptage** : **20 sessions sur 85** affichent des valeurs erronées de labels et de prélabels. À titre d'exemple, le tableau `/sessions` annonce **1 324 labels** alors que l'extraction des PDF officiels aboutit à **1 311 labels** ; les prélabels publiés (**617**) diffèrent de la réalité (**623**). Ces erreurs traduisent des données **mal gérées, mal interprétées, mal comprises et mal analysées**, ce qui fausse la mesure réelle de l'impact du programme.

**Principaux enjeux.**
- Fiabiliser le référentiel chiffré du Startup Act pour les décideurs publics (ANPR, ministères, institutions de financement) ;
- Mesurer l'impact réel du dispositif (labels, prélabels, conversions, retraits) ;
- Garantir la transparence et la reproductibilité des analyses ;
- Éclairer les recommandations du Livre Blanc par des indicateurs exacts.

☐ **Clair** ✓ · ☐ **Concis** ✓ · ☐ **Justifié** ✓

---

## 3. Besoin décisionnel et problématique

**Besoin décisionnel.** Les décideurs publics (ANPR, ministère de l'Économie, institutions financières) et les parties prenantes de l'écosystème startup tunisien ont besoin d'un **référentiel chiffré fiable, complet et audité** sur les sessions de labellisation — candidatures, labels, prélabels, conversions et retraits — pour évaluer la performance du dispositif, ajuster les politiques d'accompagnement et communiquer des indicateurs exacts.

**Problématique.** Comment produire un **état des lieux quantitatif fiable et vérifié** du programme Startup Act tunisien (2019-2026), en corrigeant les erreurs des données officielles, afin d'éclairer la décision publique et de mesurer l'impact réel du dispositif ?

☐ **Orientée décision** ✓ · ☐ **Claire** ✓ · ☐ **Pas descriptive** ✓ · ☐ **Pas trop large** ✓

---

## 4. Objectifs

**Objectif général.** Réaliser un état des lieux quantitatif **exhaustif, fiable et vérifié** du programme Startup Act tunisien (2019-2026), fondé sur les sources officielles corrigées et auditées.

**Objectifs spécifiques**

| Réf. | Objectif |
|------|----------|
| OS1 | **Collecter** les données officielles des 85 sessions de labellisation (candidatures, labels, prélabels) à partir de startup.gov.tn et des PDF officiels. |
| OS2 | **Vérifier et corriger** les données par confrontation systématique aux PDF officiels et par un audit indépendant (0 divergence). |
| OS3 | **Calculer** les indicateurs clés : taux d'acceptation réels, conversions prélabel→label, retraits de labels. |
| OS4 | **Analyser** les tendances temporelles, sectorielles et géographiques du dispositif. |
| OS5 | **Publier** un tableau de bord interactif et **documenter** l'ensemble des corrections pour garantir la reproductibilité. |

☐ **Commencent par un verbe** ✓ · ☐ **Répondent à la problématique** ✓ · ☐ **Réalistes** ✓

---

## 5. Périmètre

| Élément            | Réponse |
|--------------------|---------|
| **Géographique**   | Tunisie — ensemble du territoire national. |
| **Temporel**       | 2019 – 2026 (85 sessions de labellisation). |
| **Thématique**     | Labellisation des startups : labels, prélabels, conversions prélabel→label, retraits de labels. |
| **Acteurs concernés** | ANPR / startup.gov.tn, startups candidates et labellisées, ESEN Manouba, ISCAE Manouba, ATVIC, écosystème startup tunisien. |
| **Hors périmètre** | Analyse qualitative des dossiers de candidature, évaluation financière détaillée des startups, aspects juridiques d'application de la loi. |

☐ **Périmètre clair** ✓ · ☐ **Pas de chevauchement avec un autre axe** ✓

---

## 6. Plan de veille

| Axe ou sous-axe | Hypothèse | Question de veille | Informations recherchées | Sources envisagées | Méthodes | Outils |
|---|---|---|---|---|---|---|
| AE1.1 — Fiabilité des données officielles | Les données du tableau `/sessions` de startup.gov.tn contiennent des erreurs de comptage (labels/prélabels) sur 20 des 85 sessions. | Quelle est la fiabilité réelle des données de labellisation publiées ? | Valeurs exactes de labels et prélabels pour les 85 sessions, commentaires, taux d'acceptation et d'échec. | startup.gov.tn, PDF officiels des 85 sessions. | Extraction PDF, parsing positionnel, comparaison scrapé vs PDF. | Python (`parse_pdfs_v7.py`), tableur. |
| AE1.2 — Volumétrie globale | Le volume réel de labels (1 311) diffère du chiffre publié (1 324) ; de même pour les prélabels (623 vs 617). | Quels sont les volumes réels de candidatures, labels et prélabels sur 2019-2026 ? | Totaux par session et par année, répartition des labels. | PDF officiels, base des startups labellisées. | Agrégation, contrôle de cohérence (sommes croisées). | Python, dashboard, JSON. |
| AE1.3 — Taux d'acceptation | Le taux d'acceptation affiché diffère du taux réel pour certaines sessions. | Quelle est l'évolution réelle du taux d'acceptation du programme ? | Taux exact (labels/candidatures) par session et par année. | PDF officiels, rapports annuels du programme. | Calcul exact, arrondi contrôlé à 1 décimale. | Python, Chart.js. |
| AE1.4 — Parcours prélabel → label | Une part importante des labels provient de la conversion de prélabels accordés lors de sessions antérieures. | Combien de prélabels sont convertis en labels et quelle est la part des labels issus de conversions ? | Nombre de conversions par session, taux de conversion global (80,6 %), part des labels issus de conversions (38,3 %). | PDF officiels (commentaires de session). | Analyse de parcours, comptage. | Python, `parcours.json`, dashboard. |
| AE1.5 — Retraits de labels | Des labels sont régulièrement retirés (mortalité du label). | Combien de labels ont été retirés et pour quels motifs ? | Nombre de retraits (140), motifs et sessions concernées. | PDF officiels, communiqués ANPR. | Collecte, classification des motifs. | Python, tableur. |
| AE1.6 — Saisonnalité | Les labellisations suivent une saisonnalité marquée (décembre et mai actifs, juillet faible). | Existe-t-il une saisonnalité des labellisations ? | Labels par mois et par année sur la période. | Dashboard, PDF officiels. | Analyse temporelle. | Python, Chart.js. |
| AE1.7 — Répartition sectorielle et géographique | La concentration sectorielle est modérée (Top 4 = 51,6 %) et les startups sont concentrées dans le Grand Tunis (48 %). | Quels secteurs, années de création et régions dominent la labellisation ? | Répartition par secteur, par année de création et par région. | Base des startups labellisées, rapports annuels. | Analyse de répartition, benchmark. | Python, tableur, Leaflet. |

**Avant de compléter ce tableau :**
☐ Toutes les questions répondent à la problématique ✓
☐ Les informations recherchées permettent de prendre une décision ✓
☐ Les sources existent ✓
☐ Les méthodes sont adaptées ✓

---

## 7. Organisation de la veille

**Sources prioritaires**

| Source | Pourquoi ? | Priorité (5→1) |
|---|---|---|
| startup.gov.tn — tableau `/sessions` | Source officielle de référence du dispositif. | 5 |
| PDF officiels des 85 sessions de labellisation | Données brutes vérifiables et auditables. | 5 |
| Rapports annuels du Startup Act | Synthèses et évolutions du programme. | 4 |
| Loi n° 2018-20 et textes réglementaires | Cadre juridique du dispositif de labellisation. | 4 |
| Base des startups labellisées (ANPR) | Détail des sociétés labellisées (secteur, année, région). | 3 |
| Communiqués et presse spécialisée | Informations sur les retraits et la vie du label. | 2 |

**Outils utilisés**
☐ Recherche documentaire ✓
☐ Google Scholar ✓
☐ Base réglementaire ✓
☐ Questionnaire — *(non concerné pour cet axe quantitatif)*
☐ Entretiens — *(non concerné)*
☐ Benchmark ✓
☐ Tableau Excel ✓
☒ **Autres : scripts Python (parsing PDF), base de données JSON, tableau de bord interactif (Chart.js, Leaflet), audit indépendant (re-extraction).**

---

## 8. Livrables attendus

| Livrable | Format |
|---|---|
| Charte de cadrage de veille | Google Doc |
| Plan de veille | Google Sheet / XLSX |
| Jeu de données corrigé (85 sessions) | JSON / CSV |
| Rapport détaillé des corrections (`corrections.md`) | Markdown / PDF |
| Tableau de bord interactif (dashboard web) | Web (HTML + Chart.js + Leaflet) |
| Rapport de l'état des lieux quantitatif | PDF |

---

## 9. Risques

| Risque | Solution prévue |
|---|---|
| PDF de certaines sessions illisibles (scans vectoriels sans couche texte). | Vérification manuelle systématique des 3 sessions concernées (07/2020, 12/2020, 01/2021). |
| Erreurs résiduelles dans les données corrigées. | Double extraction (parseur v7 + re-extraction indépendante) et audit : 0 divergence. |
| Hétérogénéité des formats de sources. | Protocole d'extraction standardisé et documenté. |
| Évolution du cadre réglementaire du dispositif. | Veille continue des textes officiels. |
| Détérioration ou retrait des données en ligne. | Sauvegarde locale des PDF officiels (dossier `session-pdfs`). |

---

## 10. Validation Qualité

Avant de commencer la collecte, vérifier que :

- ☐ Le contexte est clair. ✓
- ☐ Le besoin décisionnel est identifié. ✓
- ☐ La problématique est stratégique. ✓
- ☐ Les objectifs répondent à la problématique. ✓
- ☐ Le périmètre est défini. ✓
- ☐ Les questions de veille sont pertinentes. ✓
- ☐ Les informations recherchées sont clairement identifiées. ✓
- ☐ Les sources sont fiables. ✓
- ☐ Les méthodes sont adaptées. ✓
- ☐ Les responsabilités sont réparties. ✓
- ☐ Les livrables sont définis. ✓

**Avis du Responsable Qualité**
☒ **Validé** ☐ À compléter

Commentaires : le référentiel des 85 sessions est établi à partir des PDF officiels et vérifié (audit indépendant à 0 divergence ; 3 sessions complétées manuellement). Les indicateurs (labels, prélabels, conversions, retraits, taux) sont calculés de manière reproductible à partir de `public/data/`.

Signature : **Faker BEN NOOMEN** — Responsable de l'axe AE1 — Juillet 2026
