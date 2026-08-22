# Rapprochement des Labels — contrôle manuel

## Conclusion courte

Le calcul vérifié est **1 356 Labels officiels − 1 201 lignes détaillées classées « Label accordé » = 155**. Le nombre 155 n’est pas une liste de 155 lignes absentes du tableau. Il s’agit d’un écart entre deux unités : le compteur officiel agrège les résultats publiés par session, tandis que le tableau compte les décisions ligne par ligne après normalisation.

Le rapprochement session par session donne **162 écarts positifs** et **7 écarts négatifs**, soit **162 − 7 = 155**. Les écarts négatifs sont des sessions où les lignes détaillées dépassent légèrement le compteur officiel ; ils compensent une partie des écarts positifs.

## Totaux contrôlés

| Mesure | Valeur | Lecture |
|---|---:|---|
| Labels officiels | **1 356** | Somme des compteurs officiels des 88 sessions |
| Lignes détaillées « Label accordé » | **1 201** | Classification ligne par ligne du registre détaillé |
| Écart net | **155** | 1 356 − 1 201 |
| Labels nouveaux hors conversion | **987** | 1356 − 369 conversions documentées |
| Conversions documentées | **369** | Incluses dans les 1 356, non additionnées une seconde fois |

## Rapprochement par session

Le signe **+** signifie que le compteur officiel est supérieur aux lignes détaillées classées Label accordé. Le signe **−** signifie que les lignes détaillées sont supérieures au compteur officiel.

| Session | Officiel | Détaillé | Écart officiel−détaillé | Contrôle manuel |
|---|---:|---:|---:|---|
| 12/2020 | 21 | 0 | +21 | Priorité A |
| 11/2020 | 26 | 14 | +12 | Priorité A |
| 12/2019 | 23 | 13 | +10 | Priorité A |
| 01/2021 | 24 | 15 | +9 | Priorité A |
| 02/2020 | 22 | 13 | +9 | Priorité A |
| 02/2026 | 21 | 12 | +9 | Priorité A |
| 07/2020 | 18 | 9 | +9 | Priorité A |
| 11/2019 | 17 | 11 | +6 | Priorité B |
| 12/2024 | 16 | 10 | +6 | Priorité B |
| 01/2025 | 18 | 13 | +5 | Priorité B |
| 02/2024 | 9 | 4 | +5 | Priorité B |
| 04/2023 | 14 | 9 | +5 | Priorité B |
| 05/2020 | 12 | 7 | +5 | Priorité B |
| 08/2020 | 17 | 12 | +5 | Priorité B |
| 10/2019 | 23 | 18 | +5 | Priorité B |
| 01/2020 | 18 | 14 | +4 | Priorité B |
| 03/2020 | 16 | 12 | +4 | Priorité B |
| 04/2021 | 22 | 18 | +4 | Priorité B |
| 08/2019 | 24 | 20 | +4 | Priorité B |
| 02/2023 | 18 | 15 | +3 | Priorité C |
| 04/2020 | 20 | 17 | +3 | Priorité C |
| 09/2019 | 15 | 12 | +3 | Priorité C |
| 09/2020 | 11 | 8 | +3 | Priorité C |
| 10/2020 | 16 | 13 | +3 | Priorité C |
| 12/2023 | 14 | 11 | +3 | Priorité C |
| 08/2024 | 11 | 9 | +2 | Priorité C |
| 11/2023 | 14 | 12 | +2 | Priorité C |
| 07/2019 | 15 | 14 | +1 | Priorité C |
| 07/2021 | 22 | 21 | +1 | Priorité C |
| 12/2022 | 17 | 16 | +1 | Priorité C |
| 01/2026 | 9 | 10 | -1 | Priorité C |
| 03/2023 | 13 | 14 | -1 | Priorité C |
| 06/2019 | 15 | 16 | -1 | Priorité C |
| 07/2024 | 5 | 6 | -1 | Priorité C |
| 12/2025 | 15 | 16 | -1 | Priorité C |
| 09/2021 | 13 | 15 | -2 | Priorité C |

**Somme des écarts positifs : +162. Somme des écarts négatifs : -7. Écart net : +155.**

## Ce qui est trouvé et ce qui reste à vérifier

**Trouvé avec certitude :** le 155 est entièrement traçable par la différence arithmétique des 88 sessions, et non par une addition globale opaque. Les principales contributions sont S12/2020 (+21), S11/2020 (+12), S12/2019 (+10), S02/2020 (+9), S07/2020 (+9), S01/2021 (+9) et S02/2026 (+9).

**Pas démontré comme 155 lignes manquantes :** les données détaillées contiennent des décisions de conversion, des décisions multi-tours et des reclassements entre les champs `decision` et `resultat_normalise`. Dans le champ brut, on compte 1 245 lignes Label contre 1 201 après normalisation : cette différence nette de 44 lignes confirme que le classement ligne par ligne modifie le résultat, mais elle ne suffit pas à expliquer à elle seule les 155 officiels.

**À vérifier manuellement dans les PDF :** les 22 sessions à écart officiel positif, en commençant par les priorités A. Pour chacune, comparer le compteur officiel imprimé dans le PDF aux lignes de la section de décision et vérifier si le PDF présente plusieurs tours ou un tableau de résultats non transcrit comme ligne distincte.

## Règle à conserver dans le dashboard

Le dashboard doit afficher séparément : **1 356 Labels officiels**, **1 201 lignes détaillées Label accordé**, et l’explication « 155 = écart entre unités, pas 155 lignes cachées ». Le filtre du tableau doit continuer à compter les lignes détaillées ; il ne doit pas être artificiellement gonflé à 1 356.

## Fichiers de preuve

- `label_reconciliation_by_session.csv` : rapprochement complet des 88 sessions.
- `label_reconciliation_by_session.json` : même rapprochement en JSON.
- `label_gap_decomposition.txt` : décomposition officielle−brut + brut−normalisé.
- `label_gap_reasons.txt` : sessions et exemples de décisions reclassées.
