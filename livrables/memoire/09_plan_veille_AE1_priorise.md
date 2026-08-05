# Plan de veille AE1 — État des lieux quantitatif du Startup Act (priorisé)

**Document source** : Google Docs « Plan de veille AE1 — État des lieux quantitatif » (colonne 9 de la Charte de cadrage AE1)
**Colonnes ajoutées** : **Remarque** (opérationnalité / couverture dans l'app) et **Priorité** (1 = faible → 5 = critique)

| Axe / sous-axe | Hypothèse | Question de veille | Informations recherchées | Sources envisagées | Méthodes | Outils | Remarque | Priorité |
|---|---|---|---|---|---|---|---|---|
| **Axe 1 — Dynamique du dispositif Startup Act** | Le dispositif a connu une progression mais probablement non régulière selon les années et sessions. | Comment le dispositif a-t-il évolué quantitativement entre 2018 et 2026 ? | Candidatures ; sessions ; pré-labels ; labels ; conversions ; taux ; retraits ; évolution annuelle et par session. | Startup Tunisia ; Smart Capital ; résultats officiels des sessions ; rapports annuels ; décisions de labellisation. | Collecte documentaire exhaustive ; reconstitution chronologique ; analyse descriptive et de séries temporelles. | Excel ; Google Sheets ; Power BI ; Python/R. | Axe cœur de l'AE1 — déjà couvert à ~70 % dans l'app (Dashboard, Sessions, Parcours, Corrections). Compléter avec les évolutions annuelles et les moyennes. | **5** |
| 1.1. Candidatures | Le volume des candidatures a évolué selon notoriété, conjoncture et conditions d'accès. | Combien de candidatures ont été déposées et comment évoluent-elles ? | Total ; par année ; par session ; croissance annuelle ; moyenne par session ; périodes de hausse/baisse. | Résultats des sessions ; Startup Tunisia ; archives institutionnelles. | Recensement exhaustif ; consolidation ; dédoublonnage ; analyse chronologique. | Excel ; Google Sheets ; Power BI. | Dans l'app : total (1 824), par année et par session. **Manque : croissance annuelle et moyenne/session** (calculables). | **5** |
| 1.2. Sessions de labellisation | La fréquence et la régularité des sessions influencent le nombre de dossiers traités et de labels. | Combien de sessions ont été organisées et quelle a été leur régularité ? | Total ; par année ; dates ; intervalle moyen ; candidatures moyennes par session ; sessions exceptionnelles. | Startup Tunisia ; publications officielles ; résultats des sessions. | Reconstitution du calendrier ; analyse descriptive ; mesure des intervalles. | Excel ; calendrier chronologique ; Power BI. | Dans l'app : 85 sessions et par année. **Manque : intervalle moyen et moyenne candidatures/session** (calculables). | **5** |
| 1.3. Pré-labels attribués | Le pré-label est une voie importante d'accès pour les projets n'ayant pas encore créé d'entreprise. | Comment le nombre de pré-labels a-t-il évolué ? | Total ; par session et par année ; part dans les décisions ; évolution annuelle ; profils des bénéficiaires. | Startup Tunisia ; résultats des sessions ; rapports annuels ; bases du Collège des startups. | Analyse statistique ; séries temporelles ; comparaison interannuelle. | Excel ; Power BI. | Dans l'app : total (623 corrigé), par année, par session (Parcours). **Manque : évolution annuelle** (calculable). | **5** |
| 1.4. Startup Labels attribués | Le nombre de labels a progressé avec des variations importantes selon les sessions. | Combien de labels ont été attribués et comment leur nombre évolue-t-il ? | Labels directs ; anciens pré-labels devenus labels ; par session ; par année ; cumul ; évolution annuelle. | Résultats officiels des sessions ; Startup Tunisia ; Smart Capital. | Recensement ; classification ; analyse cumulative ; comparaison annuelle. | Excel ; Google Sheets ; Power BI. | Dans l'app : total (1 311 corrigé), par année, par session. **Manque : cumul et part des conversions** (calculables). | **5** |
| 1.5. Taux de labellisation | Le taux varie selon la qualité des candidatures, les critères et les sessions. | Quelle proportion des candidatures aboutit à un label ? | Candidatures ; labels ; taux global ; taux annuel ; taux par session ; taux de label direct ; écarts entre sessions. | Résultats officiels des sessions ; Startup Tunisia. | Calcul de ratios ; analyse comparative ; identification des valeurs extrêmes. | Excel ; Power BI. | Dans l'app : taux global 44,3 % (1 311/2 958) ; annuel 59,8 % (2019) → 35,4 % (2025). **Manque : taux de label direct** (calculable). | **5** |
| 1.6. Conversion pré-label → label | Une partie importante des pré-labels n'est probablement pas convertie dans les délais prévus. | Combien de pré-labels sont convertis en labels et dans quels délais ? | Convertis ; non convertis ; taux ; délai moyen et médian ; conversion par cohorte ; motifs de non-conversion. | Startup Tunisia ; bases du Collège des startups ; RNE ; bénéficiaires. | Suivi de cohorte ; appariement des identifiants ; analyse de délai ; enquête complémentaire. | Excel ; Python/R pour appariement ; Power BI. | Dans l'app : 502 conversions, taux 80,6 %, part 38,3 % (Parcours). **Délai moyen/médian et conversion par cohorte** : à calculer via `parcours.json`. | **5** |
| 1.7. Retrait ou perte du label | Les retraits restent minoritaires mais renseignent sur les limites du dispositif. | Combien de labels ont été retirés et pour quels motifs ? | Total ; par année ; motif réglementaire ; âge de la startup ; secteur ; localisation ; statut après retrait. | Startup Tunisia ; décisions officielles ; RNE ; textes réglementaires. | Analyse documentaire ; classification des motifs ; analyse statistique. | Excel ; Zotero ; Power BI. | Dans l'app : 140 retraits, par année (Parcours). **Motifs absents des PDF** → collecter les communiqués ANPR. | **5** |
| 1.8. Efficacité administrative | L'évolution du nombre de dossiers a pu affecter les délais de traitement. | Les délais candidature→décision→pré-label→label ont-ils évolué ? | Date de candidature ; date de session ; date de décision ; durée de traitement ; délai de conversion ; variations annuelles. | Startup Tunisia ; candidats ; bases de gestion du dispositif. | Analyse de processus ; mesure des délais ; analyse par cohorte. | Excel ; diagramme BPMN ; Power BI. | **Demander à Startup Tunisia** : données non publiées, non accessibles par scraping. | **3** |
| **Axe 2 — Caractéristiques des startups labellisées** | Les startups présentent des profils juridiques, sectoriels et organisationnels différenciés. | Quelles sont les principales caractéristiques des startups labellisées ? | Secteur ; forme juridique ; date de création ; âge au label ; ancienneté ; taille d'équipe ; caractéristiques organisationnelles. | Startup Tunisia ; RNE ; APII ; sites des startups ; questionnaires. | Analyse descriptive ; classification ; consolidation ; contrôle croisé. | Excel ; Google Sheets ; Power BI ; Python. | Axe partiellement couvert. **Secteur couvert, le reste à enrichir dans `database.csv`.** | **4** |
| 2.1. Secteur principal d'activité | Les startups sont concentrées dans un nombre limité de secteurs, notamment numériques. | Quels secteurs sont les plus représentés ? | Secteur ; sous-secteur ; technologie ; nombre et % par secteur ; classification officielle. | Startup Tunisia ; RNE ; APII ; sites web. | Codification sectorielle ; analyse descriptive ; harmonisation. | Excel ; dictionnaire sectoriel ; Power BI. | **Couvert dans l'app** : page Secteurs (HHI, Top 4 = 51,6 %, Business Software dominant). | **5** |
| 2.2. Forme juridique | Certaines formes juridiques dominent largement (SARL, SUARL…). | Quelles formes juridiques sont utilisées et comment évoluent-elles ? | SARL ; SUARL ; SA ; autres ; nombre ; % ; évolution annuelle ; changements de forme. | RNE ; Startup Tunisia ; APII ; JORT. | Analyse descriptive ; comparaison temporelle. | Excel ; Power BI. | **Vérifier si les fondateurs sont aussi des associés** (RNE). Champ absent de la base → enrichir `database.csv`. | **3** |
| 2.3. Âge lors de la labellisation | La majorité des startups obtiennent le label peu après leur création. | Quel est l'âge des entreprises au moment du label ? | Date de création ; date de labellisation ; âge en mois/années ; moyenne ; médiane ; tranches d'âge ; écarts sectoriels. | RNE ; Startup Tunisia ; résultats des sessions. | Calcul de durée ; analyse statistique ; segmentation par cohorte. | Excel ; Python/R ; Power BI. | **Label date − Année création** — calculable immédiatement sur les 922 startups. À ajouter dans l'app. | **5** |
| 2.4. Ancienneté actuelle | Les cohortes anciennes permettent d'observer la pérennité du tissu startup. | Quelle est l'ancienneté des startups actives en 2026 ? | Date de création ; statut actuel ; ancienneté ; cohorte de label ; activité ou cessation. | RNE ; Startup Tunisia ; sites officiels. | Analyse de cohorte ; calcul d'ancienneté ; contrôle du statut. | Excel ; Power BI ; Python/R. | Calculable (date de création), mais **statut actuel à vérifier** (RNE) pour distinguer actif/cessation. | **4** |
| 2.5. Taille de l'équipe fondatrice | La plupart des startups sont créées par de petites équipes. | Combien de fondateurs composent les équipes ? | Nb de fondateurs ; fondateur unique ; équipes de 2, 3+ ; évolution ; variations sectorielles. | Dossiers de candidature ; Startup Tunisia ; LinkedIn ; questionnaires. | Analyse descriptive ; vérification croisée ; enquête. | Excel ; Google Forms ; LinkedIn. | Données partielles dans le champ `founders` de la base → **nettoyage + comptage à faire**. | **3** |
| 2.6. Taille de l'entreprise | Les startups sont de petites structures, mais la taille varie selon l'âge et le secteur. | Quelle est la taille des startups ? | Nombre de salariés ; tranches d'effectif ; moyenne ; médiane ; taille par âge, secteur, cohorte. | Reportings ; CNSS ; Startup Tunisia ; questionnaires. | Analyse statistique descriptive ; croisements simples. | Excel ; Power BI. | Donnée **absente** des sources actuelles (CNSS/reportings) → collecte lourde, à déléguer. | **2** |
| 2.7. Statut d'activité | Une partie des startups peut être inactive, en cessation ou redomiciliée. | Quel est le statut actuel des startups ? | Active ; sommeil ; liquidation ; radiée ; acquise ; fusionnée ; redomiciliée ; label retiré. | RNE ; Startup Tunisia ; sites ; presse économique ; questionnaires. | Vérification multi-source ; classification ; analyse descriptive. | Excel ; Zotero ; Power BI. | **Vérification multi-source obligatoire** (RNE + presse). Hors données actuelles. | **3** |
| **Axe 3 — Profil des entrepreneurs** | Les fondateurs présentent des caractéristiques sociodémographiques et professionnelles spécifiques. | Qui sont les entrepreneurs ayant fondé les startups labellisées ? | Genre ; âge ; formation ; université ; expérience ; antécédents ; statut étudiant ; diaspora. | Dossiers de candidature ; questionnaires ; LinkedIn ; universités ; réseaux de diaspora. | Analyse descriptive ; enquête ; appariement ; entretiens. | Google Forms ; Excel ; Power BI ; LinkedIn ; Python. | Axe quasi absent de l'app (un insight partiel sur le genre). **Collecte par questionnaire nécessaire.** | **3** |
| 3.1. Nombre de fondateurs | Le nombre total de fondateurs est supérieur au nombre de startups, mais les données sont dispersées. | Combien de fondateurs sont associés aux startups ? | Total de personnes uniques ; moyenne par startup ; fondateurs dans plusieurs startups ; rôles. | Dossiers ; RNE ; questionnaires ; LinkedIn. | Dédoublonnage ; appariement des identités ; analyse descriptive. | Excel ; Python ; Power BI. | À déduire du champ `founders` (noms) → **dédoublonnage à faire**. | **3** |
| 3.2. Genre | Les femmes sont sous-représentées parmi les fondateurs. | Quelle est la répartition des fondateurs selon le genre ? | Nb et % ; équipes mixtes ; startups 100 % féminines ; évolution annuelle ; écarts sectoriels/territoriaux. | Dossiers ; Startup Tunisia ; questionnaires ; LinkedIn. | Analyse descriptive et croisée ; vérification manuelle. | Excel ; Power BI. | Un insight existe (35 % → 21 %). **Créer une page/analyse dédiée** pour rendre le KPI structuré. | **4** |
| 3.3. Âge des entrepreneurs | Les fondateurs sont principalement de jeunes adultes. | Quel est l'âge des fondateurs ? | Date de naissance ou âge ; moyenne et médiane ; tranches ; évolution par cohorte ; comparaisons. | Dossiers ; questionnaires ; Startup Tunisia. | Statistiques descriptives ; segmentation. | Excel ; Power BI. | Donnée absente → **questionnaire fondateurs requis**. | **2** |
| 3.4. Niveau d'études | Les fondateurs ont majoritairement un niveau supérieur. | Quel est le niveau de formation ? | Diplôme le plus élevé ; domaine ; doctorat ; ingénierie ; gestion ; autodidactes ; répartition. | Dossiers ; questionnaires ; LinkedIn ; universités. | Enquête ; codification des diplômes ; analyse descriptive. | Google Forms ; Excel ; Power BI. | Donnée absente → questionnaire requis. | **2** |
| 3.5. Université ou établissement d'origine | Certaines écoles/universités contribuent davantage à la création de startups. | Quels établissements ont formé le plus de fondateurs ? | Université ; école ; pays d'études ; nombre de fondateurs ; domaines ; réseaux d'anciens. | Questionnaires ; LinkedIn ; universités ; dossiers. | Collecte déclarative ; normalisation ; classement descriptif. | Excel ; Google Forms ; Power BI. | Donnée absente → questionnaire requis. | **2** |
| 3.6. Expérience professionnelle | Une expérience antérieure facilite la création de la startup. | Quelle expérience les fondateurs avaient-ils ? | Années ; secteur ; fonction ; expérience internationale ; salariat ; première expérience. | Questionnaires ; LinkedIn ; entretiens. | Analyse descriptive ; segmentation ; analyse de parcours. | Google Forms ; Excel ; NVivo. | Donnée absente → questionnaire + entretiens. | **2** |
| 3.7. Expérience entrepreneuriale antérieure | Une partie des fondateurs sont des entrepreneurs récidivistes. | Combien avaient déjà créé une entreprise ? | Entreprises précédentes ; succès/échec ; nombre de projets ; secteur ; sorties. | Questionnaires ; RNE ; LinkedIn ; entretiens. | Analyse de parcours ; vérification documentaire. | Google Forms ; Excel ; LinkedIn. | Donnée absente → questionnaire + vérification RNE. | **2** |
| 3.8. Entrepreneuriat étudiant | Le pré-label a facilité les projets portés par des étudiants. | Quelle part des fondateurs était étudiante ? | Statut étudiant ; université ; programme étudiant-entrepreneur ; pré-label ; création ultérieure. | Universités ; pôles étudiants entrepreneurs ; Startup Tunisia ; questionnaires. | Analyse de cohorte ; enquête ; suivi de parcours. | Google Forms ; Excel ; Power BI. | Lien fort avec le **pré-label** (voie étudiant) → priorité relative plus élevée que 3.3-3.7. | **3** |
| 3.9. Diaspora | La diaspora joue un rôle dans la création, le financement et l'internationalisation. | Quelle est la contribution de la diaspora ? | Résidence antérieure ; pays ; retour ; cofondateurs à l'étranger ; marchés ; compétences ; investissements. | Questionnaires ; Startup Tunisia ; FIPA ; réseaux de diaspora ; LinkedIn. | Enquête ; entretiens ; cartographie des parcours. | Google Forms ; Excel ; QGIS ; NVivo. | Donnée absente → questionnaire dédié (FIPA, réseaux). | **2** |
| **Axe 4 — Répartition territoriale et dynamique sectorielle** | Les startups sont fortement concentrées dans certains territoires et secteurs. | Comment les startups sont-elles réparties et comment la structure sectorielle évolue-t-elle ? | Gouvernorat ; région ; localisation ; secteur ; spécialisation ; concentration ; évolution annuelle ; écosystèmes. | Startup Tunisia ; RNE ; APII ; INS ; incubateurs ; technopoles. | Analyse territoriale ; cartographie ; analyse sectorielle ; indices de concentration. | Excel ; Power BI ; QGIS ; Python/R. | Axe partiel dans l'app (régions du rapport 2021 uniquement). **Gouvernorats à enrichir.** | **4** |
| 4.1. Répartition par gouvernorat | Le Grand Tunis concentre une majorité des startups. | Combien de startups sont implantées dans chaque gouvernorat ? | Siège juridique ; lieu d'activité ; nombre ; % ; densité ; évolution. | Startup Tunisia ; RNE ; INS ; startups. | Géocodage ; analyse descriptive ; cartographie. | QGIS ; Excel ; Power BI. | **Donnée absente** — l'app ne montre que 4 zones (rapport 2021). Géocoder les 922 startups. | **4** |
| 4.2. Répartition par grande région | Les régions littorales sont davantage représentées. | Quelle est la répartition entre les 7 régions ? | Nombre ; part ; densité ; évolution ; secteurs dominants ; emplois. | Startup Tunisia ; INS ; RNE. | Agrégation territoriale ; analyse comparative ; cartographie. | QGIS ; Excel ; Power BI. | **Partiel** : les 7 régions existent dans le rapport 2021 (Grand Tunis 48 %). À actualiser avec les gouvernorats. | **4** |
| 4.3. Concentration territoriale | Une part élevée de startups est concentrée dans quelques gouvernorats. | Quel est le niveau de concentration territoriale ? | Part des 3-5 premiers gouvernorats ; indice de concentration ; évolution ; poids du Grand Tunis. | Base consolidée de l'axe ; INS. | Calcul d'indices ; analyse comparative temporelle. | Excel ; Python/R ; Power BI. | Calculable **dès que les gouvernorats sont disponibles** (indice + part Top 3/5). | **3** |
| 4.4. Écosystèmes régionaux | La présence d'incubateurs, universités et technopoles influence la localisation. | Quels territoires disposent d'un écosystème favorable ? | Incubateurs ; universités ; technopoles ; investisseurs ; programmes ; startups ; spécialisation locale. | Ministères ; universités ; incubateurs ; technopoles ; APII. | Cartographie des acteurs ; analyse de corrélation ; étude territoriale. | QGIS ; Excel ; Power BI. | Collecte d'acteurs hors données actuelles → **phase ultérieure**. | **2** |
| 4.5. Répartition sectorielle | Les secteurs numériques dominent l'écosystème labellisé. | Quelle est la part de chaque secteur ? | Nombre ; % ; sous-secteur ; classement ; concentration ; secteurs émergents. | Startup Tunisia ; RNE ; APII ; sites des startups. | Harmonisation sectorielle ; statistiques descriptives. | Excel ; dictionnaire sectoriel ; Power BI. | **Couvert dans l'app** (page Secteurs). | **5** |
| 4.6. Évolution sectorielle annuelle | La composition sectorielle évolue avec de nouveaux domaines technologiques. | Quels secteurs progressent, stagnent ou reculent ? | Startups par secteur et par année ; taux de croissance ; entrées ; retraits ; secteurs émergents. | Startup Tunisia ; résultats des sessions ; base consolidée. | Séries temporelles ; matrice année-secteur. | Excel ; Power BI ; Python/R. | **Calculable** (matrice année × secteur sur les 922 startups). À ajouter dans l'app. | **4** |
| 4.7. Spécialisation territoriale | Certains territoires développent une spécialisation sectorielle. | Existe-t-il des spécialisations sectorielles ? | Secteur par gouvernorat ; poids relatif ; clusters ; universités/technopoles associées. | Base consolidée ; APII ; technopoles ; universités. | Tableau croisé ; indice de spécialisation ; cartographie thématique. | QGIS ; Excel ; Python/R. | Dépend de 4.1 (gouvernorats) → **après enrichissement de la base**. | **2** |
| **Axe 5 — Innovation et potentiel technologique** | Les startups présentent un niveau d'innovation variable, données insuffisamment consolidées. | Quel est le profil d'innovation des startups labellisées ? | DeepTech ; brevets ; marques ; logiciels ; domaines technologiques ; R&D ; collaborations ; indicateurs. | Startup Tunisia ; INNORPI ; MESRS ; universités ; centres de recherche ; rapports DeepTech. | Analyse documentaire ; exploitation de bases ; questionnaire ; études de cas. | Excel ; Power BI ; Zotero ; bases INNORPI ; Google Forms. | Axe **entièrement absent de l'app** et des données actuelles. Nécessite une collecte externe dédiée. | **3** |
| 5.1. Identification des startups DeepTech | La part des startups DeepTech reste limitée et mal documentée. | Combien de startups peuvent être classées DeepTech ? | Définition ; technologie ; intensité R&D ; origine scientifique ; TRL ; temps de développement ; barrières. | Startup Tunisia ; MESRS ; universités ; centres de recherche ; Livre Blanc Technoriat. | Définition opérationnelle ; grille de classification ; revue experte ; questionnaire. | Excel ; grille DeepTech ; Google Forms ; Zotero. | Donnée absente → **grille de classification + revue experte**. | **3** |
| 5.2. Domaines technologiques | Les startups se concentrent dans certains domaines numériques. | Quels domaines technologiques sont représentés ? | IA ; Big Data ; cybersécurité ; IoT ; biotech ; greentech ; fintech ; agritech ; healthtech ; autres. | Sites des startups ; dossiers ; questionnaires ; rapports sectoriels. | Codification technologique ; analyse descriptive. | Excel ; Power BI ; dictionnaire technologique. | Peut être partiellement déduit des **secteurs existants** dans la base. | **3** |
| 5.3. Brevets nationaux | Peu de startups disposent de brevets en Tunisie. | Combien de startups ont déposé/obtenu un brevet national ? | Demandes ; brevets accordés ; titulaires ; dates ; domaines ; statut ; co-déposants. | INNORPI ; startups ; cabinets PI. | Recherche dans les bases ; appariement ; vérification. | Base INNORPI ; Excel ; Python. | **Recherche INNORPI + appariement** avec la liste des startups. | **3** |
| 5.4. Brevets internationaux | Les dépôts internationaux sont concentrés dans très peu de startups. | Combien de brevets internationaux sont associés aux startups ? | PCT ; EPO ; USPTO ; pays ; familles de brevets ; statut ; titulaires. | WIPO Patentscope ; Espacenet ; Google Patents ; startups. | Recherche brevet ; appariement ; validation manuelle. | Patentscope ; Espacenet ; Google Patents ; Excel. | **Recherche dans les bases internationales** (Patentscope/Espacenet). | **3** |
| 5.5. Autres formes de propriété intellectuelle | Les startups utilisent davantage marques, logiciels et secrets que les brevets. | Quelles formes de PI sont utilisées ? | Marques ; dessins/modèles ; logiciels ; licences ; secrets ; contrats de transfert ; protection internationale. | INNORPI ; startups ; cabinets PI ; questionnaires. | Questionnaire ; recherche dans les bases ; analyse descriptive. | Google Forms ; bases INNORPI ; Excel. | **Questionnaire + bases INNORPI**. | **2** |
| 5.6. Recherche et développement | Les dépenses et équipes de R&D sont concentrées dans certaines startups. | Quelle part des startups mène des activités structurées de R&D ? | Budget R&D ; personnel ; chercheurs ; projets ; équipements ; financement ; part du CA. | Startups ; MESRS ; programmes R&D ; états financiers. | Questionnaire ; analyse financière ; entretiens ciblés. | Google Forms ; Excel ; Power BI. | Donnée sensible → **questionnaire + entretiens ciblés**. | **2** |
| 5.7. Collaboration avec la recherche | Les liens startups-universités-laboratoires restent limités. | Combien de startups collaborent avec la recherche ? | Partenariats ; laboratoires ; conventions ; chercheurs-fondateurs ; stages ; projets conjoints ; transferts. | Universités ; MESRS ; centres de recherche ; startups. | Cartographie des collaborations ; enquête ; entretiens. | Excel ; QGIS/réseau ; NVivo. | **Enquête + cartographie réseau**. | **2** |
| 5.8. Disponibilité et qualité des données d'innovation | Les données d'innovation sont moins disponibles et homogènes que les données de labellisation. | Quelles données d'innovation existent et lesquelles collecter ? | Bases disponibles ; variables ; fréquence ; couverture ; données manquantes ; définitions ; accès. | Startup Tunisia ; INNORPI ; MESRS ; INS ; startups. | Audit des données ; analyse des écarts ; dictionnaire. | Inventaire des données ; Excel ; grille qualité. | **À faire en amont** de 5.1-5.7 : auditer les sources disponibles. | **2** |

---

## Annexe — Analyse de couverture du plan de veille par rapport à l'app

**Statut par sous-axe** : ✅ Couvert dans l'app · ⚠️ Partiel (une partie des indicateurs) · ❌ Manquant (rien dans l'app)

### Axe 1 — Dynamique du dispositif

| Sous-axe | Statut | Ce qui manque |
|---|---|---|
| 1.1 Candidatures | ⚠️ | Total ✓, par année ✓, par session ✓ — mais croissance annuelle ❌ et moyenne par session ❌ (calculables) |
| 1.2 Sessions | ⚠️ | 85 ✓, par année ✓ — mais intervalle moyen entre sessions ❌ et candidatures moyennes/session ❌ (calculables) |
| 1.3 Pré-labels | ⚠️ | Total ✓, par année/session ✓ — évolution annuelle ❌ (calculable) |
| 1.4 Labels | ⚠️ | Total ✓, par session ✓ — cumul / évolution annuelle ❌ (calculable) |
| 1.5 Taux de labellisation | ⚠️ | Global ✓, annuel ✓, par session ✓ — taux de label direct ❌ (calculable) |
| 1.6 Conversion | ⚠️ | Nombre ✓, taux ✓ — délai moyen/médian ❌, par cohorte ❌, motifs ❌ (délai partiellement calculable) |
| 1.7 Retrait | ⚠️ | Total ✓, par année ✓ — motif ❌, âge/secteur/localisation des retirés ❌, statut après retrait ❌ |
| 1.8 Efficacité administrative | ❌ | Délais de traitement (candidature→décision→label) : rien du tout |

### Axe 2 — Caractéristiques des startups

| Sous-axe | Statut | Ce qui manque |
|---|---|---|
| 2.1 Secteur principal | ✅ | Nombre ✓, % ✓, classement ✓, HHI ✓ |
| 2.2 Forme juridique | ❌ | Aucune donnée (à ajouter à database.csv) |
| 2.3 Âge à la labellisation | ❌ | Calculable immédiatement (labelDate − anneeCreation) |
| 2.4 Ancienneté actuelle | ❌ | Calculable |
| 2.5 Taille équipe fondatrice | ⚠️ | Champ founders texte — comptage possible |
| 2.6 Taille de l'entreprise (salariés) | ❌ | Données absentes |
| 2.7 Statut d'activité (cessation, liquidation…) | ❌ | Données absentes |

### Axe 3 — Profil des entrepreneurs

| Sous-axe | Statut | Ce qui manque |
|---|---|---|
| 3.1 Nombre de fondateurs | ⚠️ | Données founders dispersées |
| 3.2 Genre | ⚠️ | Seul un insight (35%→21%) existe — pas de page/analyse dédiée |
| 3.3 Âge des entrepreneurs | ❌ | Données absentes |
| 3.4 Niveau d'études | ❌ | Données absentes |
| 3.5 Université d'origine | ❌ | Données absentes |
| 3.6 Expérience professionnelle | ❌ | Données absentes |
| 3.7 Expérience entrepreneuriale | ❌ | Données absentes |
| 3.8 Entrepreneuriat étudiant | ❌ | Données absentes |
| 3.9 Diaspora | ❌ | Données absentes |

### Axe 4 — Répartition territoriale et dynamique sectorielle

| Sous-axe | Statut | Ce qui manque |
|---|---|---|
| 4.1 Répartition par gouvernorat | ❌ | L'app n'a que 4 zones du rapport 2021 (Grand Tunis 48%, Sousse 17%, Kairouan 13%, Kasserine 9%) |
| 4.2 Grande région (7 régions) | ⚠️ | Données 2021 du rapport, non actualisées |
| 4.3 Concentration territoriale | ⚠️ | 48% Grand Tunis affiché, mais pas d'indice de concentration |
| 4.4 Écosystèmes régionaux | ❌ | Données absentes |
| 4.5 Répartition sectorielle | ✅ | Complète |
| 4.6 Évolution sectorielle annuelle | ❌ | Calculable (startups par secteur × année) |
| 4.7 Spécialisation territoriale | ❌ | Données absentes |

### Axe 5 — Innovation et potentiel technologique

| Sous-axe | Statut |
|---|---|
| 5.1 Startups DeepTech | ❌ |
| 5.2 Domaines technologiques | ❌ |
| 5.3 Brevets nationaux | ❌ |
| 5.4 Brevets internationaux | ❌ |
| 5.5 Autres formes de PI | ❌ |
| 5.6 R&D | ❌ |
| 5.7 Collaboration avec la recherche | ❌ |
| 5.8 Qualité des données innovation | ❌ |

> Tout l'Axe 5 est absent — c'est le bloc le plus lourd à couvrir (exige la collecte INNORPI, WIPO/Patentscope, questionnaires).

### Synthèse globale

| Bloc | ✅ | ⚠️ |
|---|---|---|
| Axe 1 — Dynamique | 0 | 7 |
| Axe 2 — Caractéristiques | 1 | 1 |
| Axe 3 — Entrepreneurs | 0 | 2 |
| Axe 4 — Territorial/sectoriel | 1 | 2 |
| Axe 5 — Innovation | 0 | 0 |
| **Total (38 sous-axes)** | **2** | **12** |

### Priorités d'implémentation dans l'app

**Niveau 1 — Calculables immédiatement, zéro nouvelle donnée (fort impact, ~5 KPI + 3 graphiques)** :
1. Âge des startups à la labellisation (2.3) : histogramme + âge moyen/médian
2. Ancienneté actuelle (2.4) : cohortes
3. Évolutions annuelles + cumul (1.1, 1.4) : ligne cumulative labels/candidatures
4. Moyenne candidatures/session + intervalle moyen (1.2) : KPI
5. Évolution sectorielle annuelle (4.6) : graphique année × secteur

**Niveau 2 — Données à enrichir dans database.csv (débloque les axes 2, 3, 4)** :
6. Colonnes : Forme juridique, Gouvernorat, Genre fondateur(s), Date de naissance fondateur, Université → couvre 2.2, 3.1-3.5, 4.1, 4.3

**Niveau 3 — Collecte externe (axes 3.6-3.9, 5.x)** :
7. Questionnaire fondateurs (Google Forms) pour expérience, diaspora, entrepreneuriat étudiant
8. Recherche brevets (INNORPI, Patentscope/Espacenet) pour l'Axe 5

**Niveau 4 — Non couvert, à documenter comme limite** :
9. 1.7 motifs de retrait, 1.8 délais administratifs, 4.4 écosystèmes — nécessitent ANPR/entretiens

---

## Annexe — Couverture du catalogue de KPI (section 9 de la Charte de cadrage)

### KPI du Google Docs AE1 présents dans l'app ✅

| KPI (Google Docs) | Dans l'app ? |
|---|---|
| Total candidatures | ✅ |
| Labels total / par année / par session | ✅ |
| Prélabels total / par année / par session | ✅ |
| Total sessions / par année | ✅ |
| Taux de labellisation (global + par année + par session) | ✅ |
| Nombre de conversions + taux de conversion (80,6 %) | ✅ |
| Total retraits + par année | ✅ |
| Startups par secteur + % | ✅ |
| Répartition par région + % (Grand Tunis 48 %, etc.) | ✅ |
| HHI, Top 4, secteur dominant | ✅ |

### KPI du Google Docs AE1 manquants dans l'app ❌

**Axe de veille 1 — Dynamique du dispositif**

| KPI manquant | Calculable aujourd'hui ? |
|---|---|
| Taux d'évolution annuel des candidatures | ✅ Oui (données disponibles) |
| Évolution annuelle des labels et prélabels | ✅ Oui |
| Nombre moyen de candidatures par session | ✅ Oui (1 824/85 = 21,5) |
| Délai moyen de conversion prélabel→label | ⚠️ Partiellement (dates dans parcours.json) |
| Retraits par motif réglementaire | ❌ Données absentes (les PDF ne les détaillent pas) |

**Axe de veille 2 — Caractéristiques des startups**

| KPI manquant | Calculable ? |
|---|---|
| Nombre / % de startups par forme juridique | ❌ Données absentes (la base n'a pas ce champ) |
| Âge moyen lors de la labellisation | ✅ Oui (labelDate − anneeCreation) |
| Nombre de startups selon leur âge à la labellisation | ✅ Oui |
| Ancienneté moyenne | ✅ Oui |

**Axe de veille 3 — Profil des entrepreneurs**

| KPI manquant | Calculable ? |
|---|---|
| Nombre de fondateurs | ⚠️ Partiellement (champ founders texte) |
| Répartition par genre | ⚠️ Partiel (insight 35 %→21 % existe, mais pas de page dédiée) |
| Tranche d'âge / niveau d'études / université | ❌ Données absentes |
| Expérience pro / entrepreneuriat étudiant / diaspora | ❌ Données absentes |

**Axe de veille 4 — Répartition**

| KPI manquant | Calculable ? |
|---|---|
| Nombre / % de startups par gouvernorat | ❌ (l'app n'a que 4 régions du rapport 2021) |
| Évolution annuelle par secteur | ✅ Oui |

**Axe de veille 5 — Innovation**

| KPI manquant | Calculable ? |
|---|---|
| Nb / % de startups DeepTech, brevets, domaines tech | ❌ Données absentes |

### Améliorations possibles de l'app

**A. Ajouter les KPI calculables manquants (aucune nouvelle donnée requise)** :
1. KPI « Moyenne candidatures/session » + « Évolution annuelle des candidatures/labels/prélabels » → Dashboard
2. Nouvelle carte « Âge des startups à la labellisation » (histogramme) + KPI « Âge moyen »
3. Nouveau graphique « Évolution annuelle par secteur » → page Secteurs
4. KPI « Taux d'évolution » par année → page Sessions

**B. Mettre à jour les données manquantes pour les KPI restants** :
- Colonnes Forme juridique, Gouvernorat, Genre fondateur, Année de naissance fondateur dans database.csv → permet 15+ KPI nouveaux
- Motifs de retrait : collecte via communiqués ANPR → page Parcours

**C. Intégrer les 6 axes dans l'app (aujourd'hui l'app ne couvre que l'AE1)** :
- Le serveur /api/livrables/ ne liste que le dossier livrables/ racine (server.py:65) → il ignore les 6 sous-dossiers d'axes
- Ajouter une page « Axes » avec les 6 chartes (docx AE2-AE6 sont déjà dans les dossiers) → lien direct vers les fichiers

**D. Corrections de cohérence à signaler** :
- page Sessions (index.html:595) : annonce « 2 958 candidatures » mais le total réel est 1 824 → à corriger
- Insights (index.html:1722) : dit « 190 retraits sur 1824 » mais les données corrigées indiquent 140 retraits sur 1 311 labels → incohérence
- Le titre page Startups (index.html:609) dit « 922 startups » — cohérent avec la base

> **Conclusion** : ~20 KPI du Google Docs sont déjà dans l'app. Il manque 15 KPI (dont 8 sont calculables dès maintenant avec les données existantes) et il y a 2 incohérences chiffrées à corriger dans l'app.

---

## Annexe — Catalogue complet des 40 KPI (25 existants + 15 à compléter)

### A. Les 25 KPI déjà dans l'app ✅

| # | Nom précis du KPI | Description | Valeur actuelle | Page dans l'app |
|---|---|---|---|---|
| KPI-01 | Startups labellisées (base) | Nombre total de startups uniques référencées dans la base de données | 922 | Dashboard |
| KPI-02 | Labels accordés | Total cumulé de labels Startup Act attribués sur les 85 sessions | 1 311 (corrigé) | Dashboard |
| KPI-03 | Candidatures déposées | Nombre total de candidatures reçues sur la période 2019-2026 | 2 958 (somme des 85 sessions) | Dashboard |
| KPI-04 | Pré-labels accordés | Total de pré-labels attribués, corrigé vs PDF officiels | 623 | Dashboard |
| KPI-05 | Taux d'acceptation moyen | Part des candidatures ayant abouti à un label, agrégée sur la période | 44,3 % (1 311 / 2 958) | Dashboard |
| KPI-06 | Concentration sectorielle (HHI) | Indice de Herfindahl-Hirschman des parts de secteurs (modérée si < 1 500) | calculé en direct | Secteurs |
| KPI-07 | Secteur dominant | Secteur d'activité le plus représenté parmi les startups | Business Software (23 %) | Secteurs |
| KPI-08 | Top 4 secteurs | Part cumulée des 4 premiers secteurs dans le total des startups | 51,6 % | Secteurs |
| KPI-09 | Part Grand Tunis | % des startups implantées dans le Grand Tunis (rapport 2021) | 48 % | Géographie |
| KPI-10 | Part Sousse | % des startups implantées à Sousse | 17 % | Géographie |
| KPI-11 | Part Kairouan | % des startups implantées à Kairouan | 13 % | Géographie |
| KPI-12 | Part Kasserine | % des startups implantées à Kasserine | 9 % | Géographie |
| KPI-13 | Conversions pré-label → label | Nombre total de pré-labels convertis en labels | 502 | Parcours |
| KPI-14 | Taux de conversion | Part des pré-labels accordés convertis en labels | 80,6 % | Parcours |
| KPI-15 | Pré-labels accordés (Parcours) | Total de pré-labels dans la lecture Parcours pré-label → label | 623 | Parcours |
| KPI-16 | Retraits de labels | Total de labels retirés sur la période, par année | 140 | Parcours |
| KPI-17 | Labels issus de conversion | Part des labels provenant d'une conversion pré-label → label | 38,3 % | Parcours |
| KPI-18 | Sessions vérifiées | Nombre total de sessions de labellisation auditées | 85 | Corrections |
| KPI-19 | Sessions corrigées | Nombre de sessions dont les valeurs scrapées étaient fausses | 20 | Corrections |
| KPI-20 | Labels avant → après correction | Écart entre valeurs scrapées (startup.gov.tn) et PDF officiels | 1 324 → 1 311 | Corrections |
| KPI-21 | Pré-labels avant → après correction | Écart entre valeurs scrapées et PDF officiels | 617 → 623 | Corrections |
| KPI-22 | Candidatures 2019-2020 | Nombre de candidatures du premier rapport annuel | 416 | Rapports |
| KPI-23 | Emplois créés 2020 | Nombre d'emplois créés par les startups labellisées (rapport 2020) | 3 222 | Rapports |
| KPI-24 | Investissement 2021 | Montant total levé par les startups en 2021 | 157 M USD | Rapports |
| KPI-25 | Part des femmes fondatrices | Évolution de la part des femmes dans la création de startups | 35 % → 21 % | Rapports |

### B. Les 15 KPI à compléter ❌

**Axe 1 — Dynamique du dispositif**

| # | Nom précis du KPI | Description | Formule / données | Faisabilité | Page cible |
|---|---|---|---|---|---|
| KPI-26 | Taux de croissance annuel des candidatures | Variation en % du nombre de candidatures entre deux années consécutives | (Candᵢ − Candᵢ₋₁) / Candᵢ₋₁ × 100 | ✅ Calculable immédiatement | Dashboard |
| KPI-27 | Cumul et évolution annuelle des labels et pré-labels | Courbe cumulative des labels et pré-labels + taux de variation annuel | Σ labels et Σ pré-labels par année | ✅ Calculable immédiatement | Dashboard |
| KPI-28 | Nombre moyen de candidatures par session | Volume moyen de dossiers traités par session de labellisation | 1 824 / 85 = 21,5 | ✅ Calculable immédiatement | Dashboard |
| KPI-29 | Délai moyen de conversion pré-label → label | Temps moyen entre l'attribution du pré-label et sa conversion en label | Dates dans `parcours.json` | ⚠️ Partiellement calculable | Parcours |
| KPI-30 | Retraits par motif réglementaire | Répartition des 140 retraits selon le motif réglementaire | Communiqués ANPR / décisions officielles | ❌ Collecte externe | Parcours |

**Axe 2 — Caractéristiques des startups**

| # | Nom précis du KPI | Description | Formule / données | Faisabilité | Page cible |
|---|---|---|---|---|---|
| KPI-31 | Âge moyen à la labellisation | Âge moyen des startups au moment de l'obtention du label | labelDate − année de création | ✅ Calculable immédiatement | Startups |
| KPI-32 | Distribution par âge à la labellisation | Répartition des startups par tranche d'âge au label (0-1 an, 1-2, 2-3, 3-5, 5+) | Histogramme sur les 922 startups | ✅ Calculable immédiatement | Startups |
| KPI-33 | Ancienneté moyenne actuelle | Âge moyen des startups en 2026 | 2026 − année de création | ✅ Calculable immédiatement | Startups |
| KPI-34 | Répartition par forme juridique | % de startups SARL, SUARL, SA et autres | Colonne « Forme juridique » à ajouter dans `database.csv` | ❌ Collecte (RNE) | Startups |

**Axe 3 — Profil des entrepreneurs**

| # | Nom précis du KPI | Description | Formule / données | Faisabilité | Page cible |
|---|---|---|---|---|---|
| KPI-35 | Nombre de fondateurs | Nombre moyen de fondateurs par startup + fondateurs uniques | Comptage et dédoublonnage du champ `founders` | ⚠️ Partiellement calculable | Startups |
| KPI-36 | Répartition des fondateurs par genre | % de femmes/hommes, équipes mixtes, startups 100 % féminines, évolution annuelle | Insight existant (35 % → 21 %) à structurer en page dédiée | ⚠️ Partiel | Nouvelle page « Entrepreneurs » |
| KPI-37 | Profil sociodémographique des fondateurs | Âge, niveau d'études, université d'origine, expérience pro, entrepreneuriat étudiant, diaspora | Questionnaire fondateurs (Google Forms) | ❌ Collecte externe | Nouvelle page « Entrepreneurs » |

**Axe 4 — Répartition territoriale et sectorielle**

| # | Nom précis du KPI | Description | Formule / données | Faisabilité | Page cible |
|---|---|---|---|---|---|
| KPI-38 | Répartition par gouvernorat | % de startups par gouvernorat (24) + densité et évolution | Géocodage des 922 startups (siège juridique) | ❌ Collecte (base à enrichir) | Géographie |
| KPI-39 | Évolution annuelle par secteur | Matrice année × secteur : secteurs en progression, stagnation ou recul | Tableau croisé sur les 922 startups | ✅ Calculable immédiatement | Secteurs |

**Axe 5 — Innovation et potentiel technologique**

| # | Nom précis du KPI | Description | Formule / données | Faisabilité | Page cible |
|---|---|---|---|---|---|
| KPI-40 | Part de startups DeepTech / brevets / PI | % de startups DeepTech, brevets nationaux et internationaux, marques et autres PI | INNORPI, Patentscope/Espacenet, questionnaire | ❌ Collecte externe | Nouvelle page « Innovation » |

### Récapitulatif de faisabilité des 15 KPI à compléter

| Faisabilité | KPI concernés | Nombre |
|---|---|---|
| ✅ Calculables immédiatement (aucune donnée nouvelle) | KPI-26, KPI-27, KPI-28, KPI-31, KPI-32, KPI-33, KPI-39 | 7 |
| ⚠️ Partiellement calculables (données existantes à nettoyer / structurer) | KPI-29, KPI-35, KPI-36 | 3 |
| ❌ Nécessitent une collecte externe | KPI-30, KPI-34, KPI-37, KPI-38, KPI-40 | 5 |
| **Total** | | **15** |

> **Note de cohérence** : la synthèse précédente comptait « 8 calculables » en incluant le délai de conversion (KPI-29) et le nombre de fondateurs (KPI-35) comme réalisables avec effort ; le récapitulatif ci-dessus les classe en « partiellement calculables » pour plus de précision. Total catalogue : **25 existants + 15 à compléter = 40 KPI**.

---

## Statut d'implémentation dans l'app (mise à jour)

**7 KPI calculables ont été implémentés dans `streamlit-app/public/index.html`** (calculés en temps réel à partir des données corrigées : 922 startups, 1 311 labels, 623 pré-labels). Les 8 autres nécessitent une extraction/collecte et ne sont **pas** implémentés pour l'instant.

| # | Nom précis du KPI | Statut dans l'app | Valeur calculée | Emplacement |
|---|---|---|---|---|
| KPI-26 | Taux de croissance annuel des candidatures | ✅ Implémenté | 2020 : +30,9 % · 2021 : +17,4 % · 2022 : −16,7 % · 2023 : −0,8 % · 2024 : +11,4 % · 2025 : −4,3 % · 2026 : −74,3 % | Page Sessions — « Croissance annuelle des candidatures » |
| KPI-27 | Cumul et évolution annuelle des labels et pré-labels | ✅ Implémenté | Cumul labels 1 311 · cumul pré-labels 623 (courbe) | Dashboard — « Cumul des labels et pré-labels » |
| KPI-28 | Nombre moyen de candidatures par session | ✅ Implémenté | 34,8 (2 958 / 85) | Dashboard — card KPI |
| KPI-29 | Délai moyen de conversion pré-label → label | ⏸️ Non implémenté | — (dates de conversion absentes) | — |
| KPI-30 | Retraits par motif réglementaire | ⏸️ Non implémenté | — (collecte ANPR) | — |
| KPI-31 | Âge moyen à la labellisation | ✅ Implémenté | 1,0 an (922 startups) | Dashboard — card KPI |
| KPI-32 | Distribution par âge à la labellisation | ✅ Implémenté | 0 an : 465 · 1 an : 256 · 2 ans : 81 · 3 ans : 54 · 4-5 ans : 45 · 6+ ans : 21 | Dashboard — « Âge des startups à la labellisation » |
| KPI-33 | Ancienneté moyenne actuelle | ✅ Implémenté | 6,0 ans | Dashboard — card KPI |
| KPI-34 | Répartition par forme juridique | ⏸️ Non implémenté | — (collecte RNE) | — |
| KPI-35 | Nombre de fondateurs | ⏸️ Non implémenté | — (champ `founders` texte, à nettoyer) | — |
| KPI-36 | Répartition des fondateurs par genre | ⏸️ Non implémenté | — (classification à faire) | — |
| KPI-37 | Profil sociodémographique des fondateurs | ⏸️ Non implémenté | — (questionnaire) | — |
| KPI-38 | Répartition par gouvernorat | ⏸️ Non implémenté | — (géocodage à faire) | — |
| KPI-39 | Évolution annuelle par secteur | ✅ Implémenté | Top 5 : Business Software (35→46→53→27→23→19→9), Commerce (15→37→20→16→4→2→1), HealthTech, EdTech, AdTech | Page Secteurs — « Évolution annuelle par secteur — Top 5 » |
| KPI-40 | Part de startups DeepTech / brevets / PI | ⏸️ Non implémenté | — (collecte INNORPI) | — |

**Correction de cohérence appliquée dans l'app** : insight « Taux de retrait des labels : 10,4 % (190 retraits sur 1824) » → **« 10,7 % (140 retraits sur 1 311 labels) »** (données corrigées `parcours.json`).

> ⚠️ **Clarification données** : le total de **2 958 candidatures** (page Sessions/Dashboard) est la somme de la colonne candidatures des 85 sessions et reste cohérent avec le taux d'acceptation moyen (1 311/2 958 = 44,3 %). Le chiffre « 1 824 » provient du fichier périmé `analyse_quantitative_results.json` (`pdf_extracted.total_entrees` = anciennes entrées extraites des PDFs, 80/85 sessions) — **ce n'est pas le nombre de candidatures** et il a été écarté.
