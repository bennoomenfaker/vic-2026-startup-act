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

## Écart documenté — Session 01/2026 (31 officiel vs 30 CR)

- `sessions.json` (source officielle) annonce **31 candidatures** pour la Session 82 (01/2026) avec le commentaire « 03 Labels et 06 Prélabels à Labels ».
- Le Compte-Rendu officiel (vérité de terrain, `public/data/manual_sessions/2026_01.json`) liste **30 dossiers** (24 page 1 + 6 page 2) : 3 labels accordés, 7 prélabels accordés, 6 labels refusés, 13 prélabels refusés, 1 irrecevable (BNJMO Studios).
- Vérification PDF brut : les 30 lignes existent bien dans le PDF de la session ; il n'y a **aucune** mention « ajourné » dans le texte PDF janvier. Le PDF seul ne permet pas d'identifier la 31e candidature manquante.
- Décision : on **garde les 30 lignes** du CR (vérité de terrain) ; l'écart « 30 CR vs 31 officiel » est documenté dans `corrections.json` (entrée 01/2026, labels corrigés 9→10) et dans le `meta.ecart_a_documenter` de `2026_01.json`. **Attention** : ne pas recalculer le taux officiel 01/2026 (10/31 = 32,3 %) sur la base de 30 candidatures sans avoir identifié la ligne manquante.
- Les 10 labels officiels (3 labels + 7 conversions) et les 7 prélabels sont **confirmés** par le CR. Le commentaire officiel « 06 Prélabels à Labels » est **erroné** : 7 conversions réelles (Rhizome, Compta Smart Solutions, DIA Industries, Dash Master, ERPY, Park & Charge, Ligalo), mais le total labels 10 = 3 + 7 reste cohérent.
- Sessions 06/2025 (36 candidatures / 12 labels / 8 prélabels) : **cohérence totale** avec le PDF, aucune correction requise (fichier `manual_sessions/2025_06.json` créé à titre de vérification).

## Page « StartupBlink » (source externe — veille AE1)

- Page `startupblink` dans `streamlit-app/public/index.html` = **veille comparative internationale** (données EXTERNES), jamais à confondre avec les données officielles corrigées ci-dessus.
- Données : `public/data/startupblink_tunisia.json`. Rapport officiel **Global Startup Ecosystem Index 2026** consulté en ligne sur `lp.startupblink.com/report/` (copie locale archivée, **non versionnée** — les 3 PDFs StartupBlink/GSER sont dans `.gitignore`).
- Vérifié le 11/08/2026 contre 5 sources : page web `/top-startups/tunisia`, API interne `/_next/data/.../startup-ecosystem/tunisia.json`, API fiche startup (`/startup/gomycode.json`), API `leaderboards?leaderboard_type=Cities|Countries&year=2026`, et le rapport PDF (p. 344–346). Tunisie #84 mondial, +36,6 %, #2 Afrique du Nord ; Tunis #330, Sousse #1074.
- Les API StartupBlink sont bloquées par Cloudflare en curl direct : passer par Firecrawl pour les relire.
- Règle : toute donnée ajoutée depuis StartupBlink doit afficher son lien de source (voir `sources` dans le JSON + carte de sources rendue par `renderStartupBlink`).
- **Bloc « Financement 2025 »** ajouté le 11/08/2026 (clé `funding2025` du JSON) : Tunisie **#9 Afrique, 37 M USD levés en 2025**, **#7** en startups financées ≥ $100k (Africa: The Big Deal, 13/01/2026) + 31 investisseurs équité (+24 % YoY, Partech 2025). Sources liées dans le bloc. Ces données sont EXTERNES et indépendantes du Startup Act.
- **PDFs vérifiés, non intégrés** (aucune donnée Tunisie) : `startupblinkcorporate-report-2025.pdf` (0 mention TN), `startupgenomegser-2026_9607.pdf` (1 mention TN, liste).
- **Autres sources de données réelles identifiées** (veille à suivre) : Africa: The Big Deal, Partech Africa Report, Crunchbase (filtre TN), Dealroom, rapports ANAVA – Smart Capital / Startup Tunisia.

## 🤖 Méthodologie d'extraction Firecrawl & Pipeline de Données

- **Utilisation de Firecrawl** : Le tool `firecrawl parse` (`npx -y firecrawl-cli@latest parse <pdf>`) est utilisé pour convertir les comptes-rendus PDF des 85 sessions en documents Markdown structurés avec restitution fidèle des tableaux (`| Société | Fondateurs | Secteur | ... |`).
- **Pipeline de fichiers** :
  - **PDFs sources** : `public/data/session-pdfs/session_XXXX_XX.pdf`
  - **Sortie Markdown & JSON Firecrawl** : `public/data/agy/firecrawl_pdf_json/` (contient 85 fichiers `.md` + 85 fichiers `.json` + `summary.json`).
  - **Gestion du Rate Limit** : Exécution séquentielle avec temporisation (5-7 secondes entre requêtes) pour respecter le quota API distant sans échec.

## 🛠️ Méthodologie complémentaire PyMuPDF / Buffy (Freebuff)

- **Extraction PyMuPDF (`fitz`)** :
  - **83 sessions textuelles** extraites instantanément via la couche texte native du PDF (`doc = fitz.open(...)` / `page.get_text()`).
  - **2 sessions image** (`2020_12` et `2021_01`) : complétées directement avec le texte du Compte-Rendu officiel fourni et formattées sous forme de vrais tableaux Markdown.
  - **Session `2020_07`** : texte partiel (mixte FR/AR).
- **Stockage Freebuff & Scripts** :
  - **Fichiers Markdown** : `/tmp/freebuff/md/` (85 fichiers `.md`).
  - **Fichiers JSON** : `/tmp/buffy_pdf_texts/` (85 fichiers `.json` + `summary.json`).
  - **Rapport d'analyse** : `/tmp/RAPPORT_BUFFY_OPENCODE_MARKDOWN.md`.
  - **Scripts racine** : `extract_all_md.py`, `fill_image_sessions_md.py`, `extract_pdfs_to_json.py`, `compare_extractions.py`.

## Projet

- Tableau de bord Streamlit (statique, `streamlit-app/`), serveur local `python3 server.py <port>`, données dans `public/data/`.
- Livrables du mémoire dans `livrables/memoire/`.
- Branch : `main`. Commits/push sur GitHub (`bennoomenfaker/vic-2026-startup-act`) uniquement sur demande explicite.


