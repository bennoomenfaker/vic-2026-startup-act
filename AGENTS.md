# Mémoire projet — VIC Startup Act (AE1)

## ⚠️ Règle CRITIQUE — Données corrigées (ne jamais oublier)

- **Les données du tableau `/sessions` du site startup.gov.tn sont FAUSSES** (labels/prélabels erronés sur 20 sessions / 85).
- **Source de vérité = PDF officiels des sessions** ré-extraits et recalculés par l'utilisateur, documentés dans la **page « Corrections » de l'app** (ancien tableau faux vs nouveau tableau corrigé).
- **Valeurs corrigées à utiliser** : **1 311 labels** (pas 1 324) · **623 pré-labels** (pas 617) · **140 retraits** (pas 190) · **2 958 candidatures** (somme 85 sessions) · **502 conversions / 80,6 %** · **taux moyen 44,3 %** (1 311/2 958, pas 44,8 %).
- **Fichiers de référence** : `public/data/dashboard_data.json`, `public/data/parcours.json`, `public/data/corrections.json`, `public/data/database_startups.json`.
- **Fichier PÉRIMÉ, ne pas utiliser** : `public/data/analyse_quantitative_results.json` (1 324 / 617 / 190 / « 1 824 entrées PDF »).
- Les 7 KPI calculables (KPI-26, 27, 28, 31, 32, 33, 39) sont implémentés dans `streamlit-app/public/index.html` ; les autres (29, 30, 34, 35, 36, 37, 38, 40) nécessitent extraction/collecte — ne pas les prétendre calculables.
- Chiffre « 1 824 » = anciennes entrées extraites des PDFs (fichier périmé), **pas** le nombre de candidatures.

## Écart documenté — Session 04/2019 (« 1 ajourné »)

- `sessions.json` (source officielle) annonce **51 candidatures** avec le commentaire « 1 ajourné à la session suivante ».
- Le Compte-Rendu officiel (vérité de terrain, `public/data/manual_sessions/2019_04.json`) liste **52 décisions** : 33 labels accordés (chiffre officiel **exact**), 14 refus, 5 dossiers irrecevables.
- Vérification PDF brut : les 52 lignes existent bien dans le PDF de la session (aucune erreur de saisie manuelle) ; il n'y a **aucune** mention « ajourné » dans le texte PDF avril.
- Hypothèse retenue : 1 des 52 lignes du CR correspond au dossier ajourné (examiné en mai 2019, d'où « 29 candidats + 1 candidat de la session d'avril » = 30 candidatures en 05/2019). La ligne ajournée **n'est pas identifiable par recoupement de noms** : le seul nom commun trouvé (Sawssen Bellaj) est un **faux positif** (Issam Bellaj ≠ Sawssen Bellaj, personnes différentes).
- Décision : on **garde les 52 lignes** du CR (vérité de terrain) ; l'écart « 52 CR vs 51 officiel » est documenté dans `corrections.json` (entrée 04/2019, labels inchangés) et dans le `meta.ecart_a_documenter` de `2019_04.json`. **Attention** : ne pas recalculer le taux officiel 04/2019 (33/51 = 64,7 %) sur la base de 52 candidatures sans avoir identifié la ligne ajournée.
- Validation croisée (16/08/2026) : 6/7 sessions relues manuellement sont exactement cohérentes avec `sessions.json` et le tableau corrigé ; le seul écart est cette candidature 04/2019. Les 33 labels 04/2019 sont confirmés.

## Page « StartupBlink » (source externe — veille AE1)

- Page `startupblink` dans `streamlit-app/public/index.html` = **veille comparative internationale** (données EXTERNES), jamais à confondre avec les données officielles corrigées ci-dessus.
- Données : `public/data/startupblink_tunisia.json`. Rapport officiel **Global Startup Ecosystem Index 2026** consulté en ligne sur `lp.startupblink.com/report/` (copie locale archivée, **non versionnée** — les 3 PDFs StartupBlink/GSER sont dans `.gitignore`).
- Vérifié le 11/08/2026 contre 5 sources : page web `/top-startups/tunisia`, API interne `/_next/data/.../startup-ecosystem/tunisia.json`, API fiche startup (`/startup/gomycode.json`), API `leaderboards?leaderboard_type=Cities|Countries&year=2026`, et le rapport PDF (p. 344–346). Tunisie #84 mondial, +36,6 %, #2 Afrique du Nord ; Tunis #330, Sousse #1074.
- Les API StartupBlink sont bloquées par Cloudflare en curl direct : passer par Firecrawl pour les relire.
- Règle : toute donnée ajoutée depuis StartupBlink doit afficher son lien de source (voir `sources` dans le JSON + carte de sources rendue par `renderStartupBlink`).
- **Bloc « Financement 2025 »** ajouté le 11/08/2026 (clé `funding2025` du JSON) : Tunisie **#9 Afrique, 37 M USD levés en 2025**, **#7** en startups financées ≥ $100k (Africa: The Big Deal, 13/01/2026) + 31 investisseurs équité (+24 % YoY, Partech 2025). Sources liées dans le bloc. Ces données sont EXTERNES et indépendantes du Startup Act.
- **PDFs vérifiés, non intégrés** (aucune donnée Tunisie) : `startupblinkcorporate-report-2025.pdf` (0 mention TN), `startupgenomegser-2026_9607.pdf` (1 mention TN, liste).
- **Autres sources de données réelles identifiées** (veille à suivre) : Africa: The Big Deal, Partech Africa Report, Crunchbase (filtre TN), Dealroom, rapports ANAVA – Smart Capital / Startup Tunisia.

## Projet

- Tableau de bord Streamlit (statique, `streamlit-app/`), serveur local `python3 server.py <port>`, données dans `public/data/`.
- Livrables du mémoire dans `livrables/memoire/`.
- Branch : `main`. Commits/push sur GitHub (`bennoomenfaker/vic-2026-startup-act`) uniquement sur demande explicite.
