# Startup Act Tunisie — Étude Quantitative

> **Projet open source & gratuit** — Projet **académique universitaire** créé par
> **[Faker BEN NOOMEN](https://github.com/bennoomenfaker)** dans le cadre du
> **Master Professionnel en Veille et Intelligence Compétitive (VIC)**, en
> **collaboration entre l'ESEN Manouba et l'ISCAE Manouba**.

[![CI — Validate & Test](https://github.com/bennoomenfaker/vic-2026-startup-act/actions/workflows/ci.yml/badge.svg)](https://github.com/bennoomenfaker/vic-2026-startup-act/actions)

🔗 **Code source** : https://github.com/bennoomenfaker/vic-2026-startup-act
##
🔗 **URL website** : https://vic-esen-iscae-2026-startup-act.onrender.com

---

## 📖 À propos du projet

Ce projet réalise une **étude quantitative du programme Startup Act tunisien**
(Loi 2018-20) sur la période **2019-2026**. Il analyse l'ensemble des
**85 sessions de labellisation** publiées sur [startup.gov.tn](https://startup.gov.tn)
ainsi que les **rapports annuels** du programme.

Le livrable est une **application web interactive** (dashboard) qui rend compte :
- du volume de candidatures, labels et prélabels par session ;
- du taux d'acceptation et son évolution dans le temps ;
- de la répartition sectorielle, géographique et par année de création ;
- du **parcours prélabel → label** (conversions et retraits de labels) ;
- des corrections de données opérées (scrapé officiel vs PDF officiels) ;
- d'une **veille comparative internationale** de l'écosystème tunisien
  (page *StartupBlink*) à partir de sources externes vérifiées.

### 🔑 Chiffres clés (données vérifiées)

| Indicateur | Valeur |
|---|---|
| Sessions analysées | 85 |
| Candidatures | 1 824 |
| Labels accordés | 1 311 |
| Prélabels accordés | 623 |
| Conversions prélabel → label | 502 (80,6 % des prélabels) |
| Retraits de labels | 140 |
| Taux d'acceptation | 61,7 % (2019) → 36,3 % (2025) |

---

## 🗺️ Structure du projet

```
vic-2026-startup-act/
├── streamlit-app/
│   ├── server.py              # Serveur HTTP (Python)
│   ├── server.js              # Serveur HTTP (Node.js/Express)
│   └── public/
│       ├── index.html         # Application web (SPA, Chart.js + Leaflet)
│       └── images/            # Logos et photo de l'auteur
├── public/
│   └── data/
│       ├── dashboard_data.json       # Données corrigées des 85 sessions
│       ├── sessions.json             # Sessions (miroir dashboard)
│       ├── parcours.json             # Prélabel → label : conversions & retraits
│       ├── corrections.json          # 20 corrections avec raisons
│       ├── database_startups.json    # Startups labellisées
│       ├── annual_reports_parsed.json# Rapports annuels parsés
│       ├── startupblink_tunisia.json # Veille StartupBlink (données EXTERNES vérifiées)
│       └── session-pdfs/             # PDF officiels des 85 sessions
├── public/                           # (PDFs externes en archivage local uniquement, non versionnés)
├── scripts/
│   └── validate_data.py      # Validation d'intégrité des données (CI)
├── .github/workflows/
│   └── ci.yml                # Pipeline GitHub Actions CI/CD
├── corrections.md            # Rapport détaillé des corrections (85/85 vérifiées)
├── tableau_sessions.md       # Tableau des 85 sessions
├── prompt_freebuff.md        # Prompt d'audit indépendant (freebuff)
└── comparaison_sessions.html # Comparaison scrapé vs PDF
```

---

## 🚀 Lancer l'application

### Option 1 — Serveur Python

```bash
python3 streamlit-app/server.py 8082
# → http://localhost:8082
```

### Option 2 — Serveur Node.js

```bash
cd streamlit-app && npm install express && node server.js
# → http://localhost:8082
```

L'application est également configurée pour le déploiement sur
[Render](https://render.com) (`render.yaml`).

---

## ✅ CI/CD — GitHub Actions

Le pipeline `.github/workflows/ci.yml` s'exécute à chaque push sur `main` et
chaque pull request. Il valide :

1. la **syntaxe Python** (`server.py`, `scripts/validate_data.py`) ;
2. **l'intégrité des données** (`scripts/validate_data.py`) :
   - cohérence `dashboard_data.json` ↔ `sessions.json` (85 sessions),
   - taux arrondis corrects (`tauxAcceptation + tauxEchec = 100`),
   - absence de clé résiduelle `10/25` (bug corrigé en `10/2025`),
   - cohérence des totaux du parcours prélabel → label (502 conversions, 140 retraits…),
   - structure du fichier `corrections.json` (20 corrections) ;
3. la **syntaxe Node.js** (`server.js` + JS embarqué de `index.html`) ;
4. la présence des **assets statiques** (images) ;
5. le **parsing de tous les JSON** de `public/data/`.

---

## 🧪 Méthodologie & qualité des données

- **Source** : PDF officiels de labellisation de `startup.gov.tn` (85 sessions)
  + rapports annuels.
- **Extraction** : parseur positionnel Python (`parse_pdfs_v7.py`).
- **Corrections** : **20 sessions sur 85** présentaient des valeurs erronées
  dans le tableau `/sessions` de `startup.gov.tn` (labels/prélabels mal comptés).
  Toutes ont été corrigées à partir des PDF officiels.
- **Vérification** : **85/85 sessions vérifiées** — audit indépendant
  (0 divergence) + relecture manuelle des 3 scans vectoriels illisibles par OCR
  (07/2020, 12/2020, 01/2021).
- Détails dans [`corrections.md`](corrections.md).

---

## 🌍 Sources de données (veille AE1)

L'application s'appuie sur deux périmètres de données, **toujours affichés
séparément** (jamais fusionnés) :

### 1. Données officielles corrigées (Startup Act tunisien)

| Source | Usage |
|---|---|
| [startup.gov.tn](https://startup.gov.tn) — `/sessions` | Scraping initial (85 sessions) |
| PDF officiels de labellisation (85 sessions) | **Source de vérité** — re-extraction et correction des valeurs |
| Rapports annuels du programme (2019–2021) | Contexte qualitatif |

> ⚠️ Le tableau `/sessions` du site contient **20 valeurs erronées sur 85**
> (labels/prélabels mal comptés). Toutes ont été corrigées depuis les PDF
> officiels — voir la page **« Corrections »** de l'app.

### 2. Données externes de veille — StartupBlink (page *StartupBlink*)

Page de **veille comparative internationale** de l'écosystème tunisien, basée
sur des données **externes** (StartupBlink — Global Startup Ecosystem Index
2026) et **vérifiées le 11/08/2026** contre 5 sources croisées :

- page web `startupblink.com/top-startups/tunisia` ;
- API interne `/_next/data/.../startup-ecosystem/tunisia.json` (156 startups TN) ;
- API fiche startup `/startup/gomycode.json` (SB Score 476, $9,7 M levés) ;
- API `leaderboards?leaderboard_type=Cities|Countries&year=2026`
  (Tunis #330, Sousse #1074 ; Tunisie #84 mondial, +36,6 %, #2 Afrique du Nord) ;
- rapport officiel **Global Startup Ecosystem Index 2026** (p. 344–346),
  consulté sur [lp.startupblink.com/report](https://lp.startupblink.com/report/)
  (copie locale en archivage, **non versionnée**).

Données : `public/data/startupblink_tunisia.json`. Chaque valeur affichée
porte son **lien de source** (voir la carte *Sources* de la page).

### 3. PDFs téléchargés et vérifiés (non intégrés, archivés localement)

| Fichier | Contenu | Verdict |
|---|---|---|
| `startupblinkcorporate-report-2025.pdf` | Corporate Startup Activity Index 2025 | **0 mention Tunisie** → non exploitable |
| `startupgenomegser-2026_9607.pdf` | Startup Genome GSER 2026 (368 p.) | **1 seule mention Tunisie** (liste) → non exploitable |
| `startupblinkecosystemreport2026.pdf` | Global Startup Ecosystem Index 2026 (source du bloc StartupBlink) | Intégré via les **liens externes** ; PDF local non versionné |

> Ces rapports sont conservés **en local** (dans `.gitignore`, non poussés sur
> GitHub) pour archivage/documentation ; seules les données vérifiées et leurs
> liens de source nourrissent l'application.

### 4. Autres sources identifiées (extraction à venir)

Le suivi des volumes annuels et de la levée de fonds tunisienne peut être
complété à partir de : **Crunchbase** (filtre Tunisie), **Partech Africa
Report**, **Africa: The Big Deal** (Base de données sur le financement des
startups africaines), **Dealroom** et les rapports d'**ANAVA – Smart Capital**.
*À documenter au fil de l'extraction.*

---

## 👤 Auteur

### Faker BEN NOOMEN

Développeur **Full-Stack** & étudiant en **Intelligence Stratégique & Gestion de Projet**.

**Parcours académique**
- 🎓 **2026 (en cours)** — Mastère Professionnel **VIC** — Veille & Intelligence Compétitive — **ESEN Manouba × ISCAE Manouba** *(collaboration)*
- 🎓 **2025** — Mastère Professionnel (M2) **DDS** — Digitalisation des Services — **ESSECT Tunis**
- 🎓 **2024** — Master 1 (M1) **IGP** — Innovation & Gestion de Projet — **ISIMS Sfax**
- 🎓 **2023** — Licence **Informatique de Gestion** (E-Business) — **ESSECT Montfleury**

**Stack** : TypeScript · NestJS · Next.js · React · Spring Boot · FastAPI ·
Streamlit · PostgreSQL · MongoDB · OracleDB · MySQL · SQLite · Firebase ·
Prisma/TypeORM · Docker · Cloud.

**Profils**
- 💼 [LinkedIn](https://linkedin.com/in/fakerbennoomen)
- 💻 [GitHub](https://github.com/bennoomenfaker)
- 📧 fakerbennoomen@gmail.com

---

## 🤝 Partenaires & encadrement

Ce mastère **VIC** est une **collaboration entre** :

- **[ESEN Manouba](https://esen.rnu.tn/portail/)** — École Supérieure d'Économie Numérique
- **[ISCAE Manouba](https://iscae.rnu.tn/fr)** — Institut Supérieur de Comptabilité et d'Administration des Entreprises
  - **Responsable pédagogique & coordinatrice du mastère VIC** :
    **Mme Afef BELGHITH** ([LinkedIn](https://www.linkedin.com/in/afef-belghith-99a74a25/)) — afef.belghith@iscae.uma.tn

Avec le soutien de :

- **[ATVIC](https://atvic.wordpress.com/)** — Association Tunisienne de Veille et Intelligence Compétitive
  ([qui sommes-nous](https://atvic.wordpress.com/qui-sommes-nous/) · [Facebook](https://www.facebook.com/VeilleetIntelligenceCompetitive) · atvic.contact@gmail.com)

---

## 📄 Licence

Projet **open source**, **gratuit**, à but **pédagogique et universitaire**.
Toutes les données sont issues de sources publiques officielles
([startup.gov.tn](https://startup.gov.tn), [StartupBlink](https://startupblink.com),
Startup Genome) — chaque source est citée et liée dans l'application.

© 2026 Faker BEN NOOMEN — Étudiant Master VIC (Veille & Intelligence Compétitive).
