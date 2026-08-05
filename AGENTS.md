# Mémoire projet — VIC Startup Act (AE1)

## ⚠️ Règle CRITIQUE — Données corrigées (ne jamais oublier)

- **Les données du tableau `/sessions` du site startup.gov.tn sont FAUSSES** (labels/prélabels erronés sur 20 sessions / 85).
- **Source de vérité = PDF officiels des sessions** ré-extraits et recalculés par l'utilisateur, documentés dans la **page « Corrections » de l'app** (ancien tableau faux vs nouveau tableau corrigé).
- **Valeurs corrigées à utiliser** : **1 311 labels** (pas 1 324) · **623 pré-labels** (pas 617) · **140 retraits** (pas 190) · **2 958 candidatures** (somme 85 sessions) · **502 conversions / 80,6 %** · **taux moyen 44,3 %** (1 311/2 958, pas 44,8 %).
- **Fichiers de référence** : `public/data/dashboard_data.json`, `public/data/parcours.json`, `public/data/corrections.json`, `public/data/database_startups.json`.
- **Fichier PÉRIMÉ, ne pas utiliser** : `public/data/analyse_quantitative_results.json` (1 324 / 617 / 190 / « 1 824 entrées PDF »).
- Les 7 KPI calculables (KPI-26, 27, 28, 31, 32, 33, 39) sont implémentés dans `streamlit-app/public/index.html` ; les autres (29, 30, 34, 35, 36, 37, 38, 40) nécessitent extraction/collecte — ne pas les prétendre calculables.
- Chiffre « 1 824 » = anciennes entrées extraites des PDFs (fichier périmé), **pas** le nombre de candidatures.

## Projet

- Tableau de bord Streamlit (statique, `streamlit-app/`), serveur local `python3 server.py <port>`, données dans `public/data/`.
- Livrables du mémoire dans `livrables/memoire/`.
- Branch : `main`. Commits/push sur GitHub (`bennoomenfaker/vic-2026-startup-act`) uniquement sur demande explicite.
