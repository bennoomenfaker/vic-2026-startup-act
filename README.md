# Startup Act Tunisie — Étude quantitative

> **Projet open source et universitaire** créé par **[Faker BEN NOOMEN](https://github.com/bennoomenfaker)** dans le cadre du Mastère Professionnel **Veille et Intelligence Compétitive (VIC)**, en collaboration entre l’**ESEN Manouba** et l’**ISCAE Manouba**.

[![CI — Validate & Test](https://github.com/bennoomenfaker/vic-2026-startup-act/actions/workflows/ci.yml/badge.svg)](https://github.com/bennoomenfaker/vic-2026-startup-act/actions)

| Ressource | Lien |
|---|---|
| Code source | https://github.com/bennoomenfaker/vic-2026-startup-act |
| Site public | https://vic-esen-iscae-2026-startup-act.onrender.com |
| Site personnel | https://bennoomenfaker.github.io |

## Objet du projet

Ce projet documente le programme tunisien de labellisation **Startup Act**, fondé sur la loi n°2018-20 du 17 avril 2018, sur la période 2019–2026. L’application rassemble les comptes rendus PDF des **88 sessions** publiées par [startup.gov.tn](https://startup.gov.tn), les données de sessions et les corrections issues de la comparaison entre compteurs institutionnels et lignes documentaires.

Le site propose un tableau officiel par session, un tableau détaillé des entreprises et fondateurs, des filtres par session et par décision, des exports téléchargeables ainsi que les pages de corrections, de qualité des données et d’étude quantitative.

## Contrat statistique

Les trois périmètres sont conservés séparément. Une ligne documentaire n’est pas automatiquement équivalente à une candidature institutionnelle : les PDF contiennent notamment des conversions prélabel→label, des retraits et des décisions reportées. Les trois ajournés de 03/2019 et 06/2019 sont documentés hors PDF nominatif et ne sont pas inventés comme entreprises.

| Indicateur | Compteur officiel | Travail fondé sur les PDF |
|---|---:|---:|
| Sessions | 88 | 88 |
| Candidatures | 3 079 | 3 566 lignes PDF ; 3 569 avec 3 ajournés hors PDF |
| Labels accordés | 1 356 | 1 343 corrigés par rapprochement des sessions |
| Prélabels accordés | 641 | 647 corrigés par rapprochement des sessions |
| Retraits de label | 153 | Catégorie documentaire séparée |
| Reportés | Compteur institutionnel séparé | Catégorie documentaire séparée |

Le chiffre **3 566** désigne les lignes documentaires PDF après l’intégration de onze lignes manquantes dans les sessions 04/2026, 05/2026 et 06/2026. Le chiffre **3 569** ajoute les trois ajournés hors PDF. Ces valeurs ne remplacent pas le compteur institutionnel de **3 079 candidatures**.

### Audit des trois dernières sessions

| Session | Lignes PDF intégrées | Lignes ajoutées lors de l’audit |
|---|---:|---|
| 04/2026 | 50 | Mathix Academy, SURUS, Tunisia transfert |
| 05/2026 | 48 | Deep SaaS, Carbon Zero Tech, NFASS, FIXITECHPRO, Cuber, shopyia |
| 06/2026 | 47 | Nvitee, Creedex |

La session 03/2019 est affichée avec **16 candidatures officielles et 16 corrigées**, dont **12 labels accordés, 2 labels non accordés et 2 ajournés hors PDF**. La session 06/2019 comporte également **1 ajourné hors PDF**. Les commentaires de report sont conservés comme commentaires, tandis que le statut normalisé est **Reporté** lorsque le dossier est reporté à la session suivante, comme pour ITMMA en 06/2024.

## Organisation du dépôt

```text
vic-2026-startup-act/
├── streamlit-app/
│   ├── server.py                 # Serveur HTTP Python
│   └── public/
│       └── index.html            # Application web HTML/JavaScript
├── public/data/
│   ├── reextraction_88_canonical.json       # Corpus canonique des lignes PDF
│   ├── session-pdfs/                        # PDF des 88 sessions
│   ├── session-pdfs-json/                   # Données détaillées par session
│   ├── database_startups_88.json             # Tableau détaillé consultable
│   ├── sessions_table.json                   # Compteurs et rapprochement par session
│   ├── database_entrees_brutes_88.csv        # Export détaillé CSV
│   ├── database_entrees_reextrait_88_corrige.csv
│   ├── Startup_Act_88_sessions_reextrait_corrige_2026-08-23.xlsx
│   ├── startup_act_database.sql              # Export SQL relationnel
│   ├── founders_database.sqlite               # Base SQLite consultable
│   └── dashboard_data.json                   # Métadonnées du dashboard
├── scripts/reconciliation/                  # Scripts d’intégration et de contrôle
├── corrections.md                            # Documentation des corrections
└── render.yaml                               # Configuration Render Python
```

## Lancer l’application localement

À la racine du dépôt :

```bash
pip install -r requirements.txt
python3 streamlit-app/server.py
```

Le serveur utilise le port fourni par `PORT` lorsqu’il est défini ; en local, il peut être consulté sur le port indiqué par le serveur.

## Configuration Render

Le service doit être configuré comme **Web Service Python** avec la racine du dépôt comme répertoire racine :

| Champ Render | Valeur |
|---|---|
| Runtime | Python |
| Root Directory | Vide |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python3 streamlit-app/server.py` |
| Version Python | `3.12.10` recommandée |

Après un push sur `main`, utilisez **Manual Deploy → Deploy latest commit** dans Render. Le dépôt contient un serveur Python ; il ne faut pas utiliser `pnpm`, `vite` ou `requirements.txt` avec un runtime Node/React.

## Méthodologie et qualité

Les PDF officiels constituent la source documentaire principale. L’extraction combine le texte PDF, le repérage des blocs de décisions et les contrôles manuels des sessions signalées comme incohérentes. Les champs individuels — noms de startups, fondateurs ou secteurs — peuvent rester approximatifs lorsqu’ils sont difficiles à lire ; les compteurs officiels et les lignes documentaires sont donc présentés dans des colonnes distinctes.

Les principales règles de rapprochement sont les suivantes :

1. Le compteur **officiel** reprend le compteur institutionnel de la session.
2. Les **lignes PDF** représentent les enregistrements imprimés et peuvent contenir des opérations historiques supplémentaires.
3. Le périmètre **corrigé** ajoute les ajournés hors PDF documentés, sans créer de nom d’entreprise fictif.
4. Les conversions prélabel→label, les retraits et les Reportés restent identifiables comme catégories distinctes.
5. Les sessions 04/2026, 05/2026 et 06/2026 ont été complétées par onze lignes contrôlées dans les PDF.

Le dossier `public/data/` contient les exports régénérés. Les scripts de réconciliation et le contrôle final permettent de reproduire les volumes et de vérifier l’absence de doublons dans les trois fichiers JSON de session 2026.

## Sources

Les données institutionnelles et les PDF sont consultables sur [startup.gov.tn](https://startup.gov.tn), notamment la page [Startup Act — résultats](https://startup.gov.tn/fr/startup_act/results). Les rapports annuels utilisés pour le contexte sont référencés dans l’application et dans les documents d’étude.

La page de veille comparative StartupBlink utilise des données externes explicitement identifiées dans l’application ; elles ne sont pas mélangées aux compteurs du programme Startup Act.

## Auteur et partenaires

**Faker BEN NOOMEN** est étudiant en Mastère Professionnel VIC — Veille et Intelligence Compétitive. Le projet est réalisé dans le cadre de la collaboration **[ESEN Manouba](https://esen.rnu.tn/portail/) × [ISCAE Manouba](https://iscae.rnu.tn/fr)**, avec le soutien de l’**[ATVIC](https://atvic.wordpress.com/)**.

Profils : [GitHub](https://github.com/bennoomenfaker) · [LinkedIn](https://linkedin.com/in/fakerbennoomen) · [site personnel](https://bennoomenfaker.github.io) · fakerbennoomen@gmail.com

## Licence et usage

Projet open source, gratuit et à but pédagogique et universitaire. Les données sont issues de sources publiques ; les limites d’extraction, les différences de périmètre et les corrections sont affichées pour permettre un contrôle manuel et une réutilisation responsable.

© 2026 Faker BEN NOOMEN — Projet académique VIC.
