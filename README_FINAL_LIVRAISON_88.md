# Livraison finale — Étude quantitative du Startup Act tunisien

## Périmètre et métriques de référence

Cette livraison couvre les **88 sessions S0–S87** et distingue volontairement deux niveaux de mesure. Le compteur administratif officiel totalise **3 079 candidatures**, **1 356 Labels**, **641 Prélabels**, **1 997 décisions positives**, **153 retraits officiels** et **4 Reporté confirmés**. Le registre documentaire contient **3 528 décisions détaillées** : il conserve les lignes des PDF, les conversions Prélabel → Label et les retraits sans les transformer automatiquement en nouvelles candidatures.

| Élément | Valeur finale | Source / interprétation |
|---|---:|---|
| Sessions | 88 | S0–S87 |
| Candidatures officielles | 3 079 | Compteurs officiels par session |
| Décisions détaillées | 3 528 | Lignes documentaires du registre canonique |
| Labels officiels | 1 356 | Compteurs officiels par session |
| Prélabels officiels | 641 | Compteurs officiels par session |
| Décisions positives | 1 997 | Labels + Prélabels |
| Retraits officiels | 153 | Compteurs officiels par session |
| Reporté confirmés | 4 | S11, S12, S28 et S67 |

## Cas S62 — 05/2024

S62 conserve **39 candidatures officielles** et **45 enregistrements documentaires** dans la version canonique : 39 lignes du bloc principal, 4 conversions historiques Prélabel → Label identifiées dans les lignes, et 2 retraits. La session ne contient **aucun Reporté**. Le compteur officiel de S62 est donc la référence; la formule « lignes moins Reporté » ne remplace pas ce compteur.

## SQL

Le SQL final comprend 88 compteurs de session avec des identifiants `S0` à `S87`, 3 528 `decision_id` distincts, 3 088 entreprises et 3 189 fondateurs. La table `company_founders` est incluse; les 6 doublons strictement identiques du CSV de relations sont ignorés par `INSERT OR IGNORE` afin de respecter la clé composite, tandis que le CSV source est conservé intégralement dans le paquet de réextraction.

## Fichiers principaux

- `public/data/reextraction_validee_88/` : Excel 88 feuilles, JSON canonique, CSV des sessions, décisions, entreprises, fondateurs et relations, SQL, validations et audit Drive.
- `public/data/dashboard_data.json`, `sessions.json`, `session_pdfs_extracted.json` et `session_pdf_counts.json` : sources consommées par le dashboard.
- `streamlit-app/public/index.html`, `streamlit-app/server.js` et `streamlit-app/server.py` : interface et routes avec contrôle anti-cache.
- `rapport_academique_startup_act_88_sessions.md` et `rapport_academique_startup_act_88_sessions.pdf` : rapport complet synchronisé.
- `soutenance_startup_act/` et `logique_candidatures_deck/` : sources HTML des deux diaporamas révisés.

## Statut GitHub et Render

Le commit local de synchronisation est `93cf307`. La branche distante `main` reste actuellement sur `1f797587` car le token GitHub disponible a renvoyé **403 — permission d’écriture refusée**. Après activation d’un accès GitHub avec permission d’écriture sur `bennoomenfaker/vic-2026-startup-act`, pousser le commit local puis déclencher manuellement un nouveau déploiement Render. Le service Render ne se mettra pas à jour tant que le commit corrigé n’est pas accepté par GitHub et redéployé.
