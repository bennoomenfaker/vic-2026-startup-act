# Paquet de réextraction validée — Startup Act Tunisie

Ce dossier contient une réextraction et une validation locale du corpus des **88 PDF de sessions S0–S87**, avec comparaison aux JSON structurés, au classeur Excel existant et aux compteurs officiels par session.

## Résultats validés

| Mesure | Valeur |
|---|---:|
| PDF de session | 88 |
| Sessions | 88 |
| Entrées détaillées | 3 528 |
| Candidatures officielles | 3 079 |
| Labels officiels | 1 356 |
| Prélabels officiels | 641 |
| Conversions | 369 |
| Retraits officiels | 153 |
| Reportés détaillés | 4 |

Les candidatures officielles proviennent des compteurs publiés par session. Les entrées détaillées proviennent des lignes documentaires des PDF/JSON. Ces deux périmètres ne doivent pas être forcés à égalité par une formule unique.

## Contrôle PDF

Les 88 PDF possèdent une clé de session unique. Les noms d’entreprise ont été retrouvés dans le texte PDF/OCR pour 3 465 lignes sur 3 528 (98,21 %). Les mots-clés de décision ont été retrouvés pour 3 396 lignes (96,26 %). Les PDF 12/2020 et 01/2021 ont reçu un OCR français/anglais supplémentaire, car leur couche texte est absente ou incomplète.

Treize lignes ne présentent pas de fondateur exploitable dans la source structurée. Elles sont conservées comme **Non renseigné** ; aucun nom n’a été inventé. Les quatre lignes Reporté sont conservées dans la couleur terracotta du classeur.

## Fichiers principaux

- `Startup_Act_88_sessions_reextrait_valide.xlsx` : classeur avec synthèse, 88 feuilles de session, décisions, entreprises, fondateurs et contrôle qualité.
- `reextraction_88_canonical.json` : registre canonique structuré.
- `database_sessions_reextrait.csv` : compteurs par session.
- `database_entrees_reextrait.csv` : lignes détaillées.
- `database_companies_reextrait.csv` : index des entreprises.
- `database_founders_reextrait.csv` : index des fondateurs observés.
- `database_company_founders_reextrait.csv` : relations entreprise–fondateur.
- `startup_act_database_reextrait_valide.sql` : SQL régénéré avec candidatures officielles explicites et IDs de décisions uniques.
- `validation_exports_finaux.json` : contrôle automatisé final ; résultat `pass: true`.

La comparaison des fichiers Google Drive reste en attente, car le compte Google n’est pas authentifié dans l’environnement. Aucun fichier Drive n’a été modifié.
