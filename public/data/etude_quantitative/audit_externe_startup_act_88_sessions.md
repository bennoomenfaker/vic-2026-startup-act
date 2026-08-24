# Audit externe Startup Act — exécution du prompt

**Statut : audit exécuté en réutilisant les extractions existantes. Aucune réextraction des 88 PDF et aucune modification du dépôt n’a été effectuée dans cette exécution.**

## Conclusion exécutive

Le chiffre de **3 338 candidatures** demandé comme hypothèse dans le prompt n’est pas reproductible avec les données déjà vérifiées. Le compteur officiel recalculé à partir de la page Startup Tunisia est **3 079** pour 88 sessions. Le registre documentaire PDF déjà extrait contient **3 555 lignes**, et la série corrigée ajoute **3 ajournés hors PDF**, soit **3 558 enregistrements documentaires corrigés**. [1] [2]

| Série | Total | Ce que la série mesure |
|---|---:|---|
| Scénario A — institutionnel | **3 079** | Candidatures selon le compteur officiel |
| Scénario B — documentaire PDF | **3 555** | Lignes de tous les blocs PDF |
| Scénario B corrigé | **3 558** | 3 555 lignes + 3 ajournés hors PDF |

> `3 555 − 3 079 = 476`. Les 476 ne sont pas 476 candidatures supplémentaires prouvées ; ce sont des occurrences documentaires supplémentaires. `3 558 − 3 079 = 479` après les trois ajournés.

## Définition des deux scénarios

### Scénario A — comptage institutionnel

Le scénario A conserve le compteur officiel de chaque session. Il reproduit la série institutionnelle sans ajouter mécaniquement les conversions, retraits ou lignes historiques des PDF. Les totaux officiels de la page sont **3 079 candidatures, 1 356 Labels et 641 Prélabels**. [1]

### Scénario B — comptage documentaire corrigé

Le scénario B compte les lignes réellement présentes dans les exports issus des PDF, en distinguant le tableau principal de la session, les conversions Prélabel → Label, les retraits, les reports et les ajournés hors PDF. Une conversion ne doit pas être assimilée automatiquement à une nouvelle candidature : elle est généralement une décision ultérieure sur un dossier déjà prélabelisé.

## Réponse aux questions du prompt

| Question | Conclusion auditée | Niveau de confiance |
|---|---|---|
| Le site compte-t-il les lignes PDF ? | Non démontré ; les totaux ne suivent pas les lignes de tous les blocs PDF. | Élevé |
| Le site compte-t-il les dossiers uniques ? | Le chiffre officiel est institutionnel, mais la règle exacte de dédoublonnage n’est pas publiée. | Moyen |
| Une conversion Prélabel → Label est-elle une nouvelle candidature ? | Dans le PDF, c’est une ligne historique de décision ; elle ne doit pas être ajoutée comme nouvelle candidature sans preuve d’un nouveau dossier. | Élevé |
| Les retraits sont-ils des candidatures nouvelles ? | Non ; ce sont des événements ultérieurs documentés dans un bloc séparé. | Élevé |
| Les reports sont-ils comptés deux fois ? | Non déterminable pour chaque dossier sans identifiant ; le rapport conserve les occurrences et documente les transitions prouvées. | Moyen |
| Les ajournés hors PDF sont-ils inclus officiellement ? | Non démontrable ; ils sont ajoutés séparément uniquement dans la série documentaire corrigée. | Moyen |
| Les Labels officiels incluent-ils les conversions ? | Les comparaisons montrent que les nombres de Labels officiels correspondent souvent à Labels directs + conversions annoncées ; la page ne publie pas la formule détaillée, mais l’hypothèse est fortement corroborée. | Élevé |
| Les Prélabels devenus Labels restent-ils Prélabels officiels ? | Les conversions sont comptées comme Labels dans le total de Labels ; elles ne doivent pas être recomptées comme Prélabels finaux. | Élevé |

## Tableau complet des 88 sessions

| Session | PDF | Uniques approximés | Lignes PDF | Officiel | Corrigé | Labels directs | Conversions | Labels finaux | Prélabels accordés | Prélabels non accordés | Retraits | Reports | Ajournés | Écart brut | Résiduel sans double compte | Formule prompt | Scénario A | Scénario B |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 03/2019 | session_2019_03.pdf | 14 | 14 | 16 | 16 | 12 | 0 | 12 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | -2 | 16 | 16 |
| 04/2019 | session_2019_04.pdf | 52 | 52 | 51 | 52 | 33 | 0 | 33 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 51 | 52 |
| 05/2019 | session_2019_05.pdf | 30 | 30 | 30 | 30 | 23 | 0 | 23 | 8 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 30 | 30 |
| 06/2019 | session_2019_06.pdf | 32 | 32 | 33 | 33 | 27 | 0 | 27 | 10 | 1 | 0 | 0 | 1 | 0 | 0 | -1 | 33 | 33 |
| 07/2019 | session_2019_07.pdf | 29 | 29 | 28 | 29 | 22 | 0 | 22 | 8 | 3 | 0 | 0 | 0 | 1 | 1 | 1 | 28 | 29 |
| 08/2019 | session_2019_08.pdf | 28 | 28 | 28 | 28 | 25 | 0 | 25 | 5 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 28 | 28 |
| 09/2019 | session_2019_09.pdf | 27 | 27 | 24 | 27 | 21 | 0 | 21 | 6 | 4 | 0 | 0 | 0 | 3 | 3 | 3 | 24 | 27 |
| 10/2019 | session_2019_10.pdf | 39 | 39 | 34 | 39 | 28 | 0 | 28 | 5 | 5 | 0 | 0 | 0 | 5 | 5 | 5 | 34 | 39 |
| 11/2019 | session_2019_11.pdf | 41 | 41 | 35 | 41 | 27 | 0 | 27 | 10 | 10 | 0 | 0 | 0 | 6 | 6 | 6 | 35 | 41 |
| 12/2019 | session_2019_12.pdf | 42 | 42 | 32 | 42 | 21 | 10 | 31 | 8 | 6 | 0 | 0 | 0 | 10 | 0 | 0 | 32 | 42 |
| 01/2020 | session_2020_01.pdf | 42 | 42 | 38 | 42 | 29 | 0 | 29 | 11 | 4 | 0 | 0 | 0 | 4 | 4 | 4 | 38 | 42 |
| 02/2020 | session_2020_02.pdf | 40 | 41 | 32 | 41 | 24 | 9 | 33 | 11 | 3 | 0 | 1 | 0 | 9 | 0 | 0 | 32 | 41 |
| 03/2020 | session_2020_03.pdf | 40 | 40 | 35 | 40 | 26 | 0 | 26 | 10 | 6 | 0 | 1 | 0 | 5 | 5 | 5 | 35 | 40 |
| 04/2020 | session_2020_04.pdf | 45 | 45 | 40 | 45 | 27 | 0 | 27 | 7 | 8 | 1 | 0 | 0 | 5 | 4 | 4 | 40 | 45 |
| 05/2020 | session_2020_05.pdf | 32 | 32 | 26 | 32 | 22 | 0 | 22 | 10 | 5 | 1 | 0 | 0 | 6 | 5 | 5 | 26 | 32 |
| 06/2020 | session_2020_06.pdf | 30 | 30 | 26 | 30 | 17 | 0 | 17 | 5 | 9 | 0 | 0 | 0 | 4 | 4 | 4 | 26 | 30 |
| 07/2020 | session_2020_07.pdf | 50 | 51 | 40 | 51 | 16 | 9 | 25 | 7 | 13 | 2 | 0 | 0 | 11 | 0 | 0 | 40 | 51 |
| 08/2020 | session_2020_08.pdf | 34 | 34 | 28 | 34 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | 6 | 6 | 6 | 28 | 34 |
| 09/2020 | session_2020_09.pdf | 23 | 23 | 24 | 23 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | -1 | -1 | -1 | 24 | 23 |
| 10/2020 | session_2020_10.pdf | 49 | 49 | 41 | 49 | 19 | 7 | 26 | 10 | 16 | 1 | 0 | 0 | 8 | 0 | 0 | 41 | 49 |
| 11/2020 | session_2020_11.pdf | 40 | 40 | 41 | 40 | 16 | 0 | 16 | 2 | 0 | 0 | 0 | 0 | -1 | -1 | -1 | 41 | 40 |
| 12/2020 | session_2020_12.pdf | 36 | 36 | 36 | 36 | 20 | 0 | 20 | 8 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 36 | 36 |
| 01/2021 | session_2021_01.pdf | 36 | 36 | 36 | 36 | 22 | 0 | 22 | 7 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 36 | 36 |
| 02/2021 | session_2021_02.pdf | 47 | 48 | 41 | 48 | 28 | 7 | 35 | 10 | 6 | 0 | 0 | 0 | 7 | 0 | 0 | 41 | 48 |
| 03/2021 | session_2021_03.pdf | 56 | 56 | 41 | 56 | 20 | 13 | 33 | 8 | 13 | 2 | 0 | 0 | 15 | 0 | 0 | 41 | 56 |
| 04/2021 | session_2021_04.pdf | 81 | 81 | 80 | 81 | 42 | 0 | 42 | 24 | 31 | 1 | 0 | 0 | 1 | 0 | 0 | 80 | 81 |
| 05/2021 | session_2021_05.pdf | 47 | 47 | 40 | 47 | 21 | 6 | 27 | 8 | 12 | 1 | 0 | 0 | 7 | 0 | 0 | 40 | 47 |
| 06/2021 | session_2021_06.pdf | 47 | 47 | 41 | 47 | 17 | 7 | 24 | 6 | 13 | 0 | 0 | 0 | 6 | -1 | -1 | 41 | 47 |
| 07/2021 | session_2021_07.pdf | 50 | 50 | 40 | 50 | 15 | 11 | 26 | 5 | 15 | 0 | 1 | 0 | 10 | -1 | -1 | 40 | 50 |
| 08/2021 | session_2021_08.pdf | 33 | 33 | 25 | 33 | 10 | 7 | 17 | 4 | 6 | 1 | 0 | 0 | 8 | 0 | 0 | 25 | 33 |
| 09/2021 | session_2021_09.pdf | 38 | 38 | 15 | 38 | 8 | 13 | 21 | 6 | 13 | 0 | 1 | 0 | 23 | 10 | 10 | 15 | 38 |
| 10/2021 | session_2021_10.pdf | 49 | 49 | 41 | 49 | 22 | 8 | 30 | 7 | 13 | 0 | 0 | 0 | 8 | 0 | 0 | 41 | 49 |
| 11/2021 | session_2021_11.pdf | 47 | 47 | 40 | 47 | 22 | 7 | 29 | 10 | 10 | 0 | 0 | 0 | 7 | 0 | 0 | 40 | 47 |
| 12/2021 | session_2021_12.pdf | 50 | 51 | 38 | 51 | 25 | 6 | 31 | 11 | 9 | 7 | 0 | 0 | 13 | 0 | 0 | 38 | 51 |
| 01/2022 | session_2022_01.pdf | 45 | 46 | 38 | 46 | 17 | 6 | 23 | 8 | 10 | 4 | 0 | 0 | 8 | -2 | -2 | 38 | 46 |
| 02/2022 | session_2022_02.pdf | 21 | 22 | 18 | 22 | 11 | 4 | 15 | 3 | 5 | 0 | 0 | 0 | 4 | 0 | 0 | 18 | 22 |
| 03/2022 | session_2022_03.pdf | 30 | 30 | 21 | 30 | 10 | 9 | 19 | 5 | 6 | 0 | 0 | 0 | 9 | 0 | 0 | 21 | 30 |
| 04/2022 | session_2022_04.pdf | 27 | 27 | 22 | 27 | 11 | 4 | 15 | 6 | 6 | 1 | 0 | 0 | 5 | 0 | 0 | 22 | 27 |
| 05/2022 | session_2022_05.pdf | 49 | 49 | 41 | 49 | 17 | 6 | 23 | 9 | 12 | 2 | 0 | 0 | 8 | 0 | 0 | 41 | 49 |
| 06/2022 | session_2022_06.pdf | 46 | 46 | 40 | 46 | 20 | 4 | 24 | 10 | 10 | 2 | 0 | 0 | 6 | 0 | 0 | 40 | 46 |
| 07/2022 | session_2022_07.pdf | 45 | 45 | 40 | 45 | 23 | 4 | 27 | 9 | 9 | 1 | 0 | 0 | 5 | 0 | 0 | 40 | 45 |
| 08/2022 | session_2022_08.pdf | 43 | 44 | 36 | 44 | 18 | 6 | 24 | 12 | 8 | 2 | 0 | 0 | 8 | 0 | 0 | 36 | 44 |
| 09/2022 | session_2022_09.pdf | 49 | 49 | 40 | 49 | 15 | 9 | 24 | 5 | 15 | 0 | 0 | 0 | 9 | 0 | 0 | 40 | 49 |
| 10/2022 | session_2022_10.pdf | 45 | 45 | 38 | 45 | 15 | 6 | 21 | 7 | 13 | 1 | 0 | 0 | 7 | 0 | 0 | 38 | 45 |
| 11/2022 | session_2022_11.pdf | 42 | 42 | 34 | 42 | 19 | 8 | 27 | 10 | 10 | 0 | 0 | 0 | 8 | 0 | 0 | 34 | 42 |
| 12/2022 | session_2022_12.pdf | 39 | 39 | 30 | 39 | 12 | 9 | 21 | 5 | 12 | 0 | 0 | 0 | 9 | 0 | 0 | 30 | 39 |
| 01/2023 | session_2023_01.pdf | 38 | 38 | 26 | 38 | 12 | 10 | 22 | 6 | 5 | 2 | 0 | 0 | 12 | 0 | 0 | 26 | 38 |
| 02/2023 | session_2023_02.pdf | 42 | 42 | 33 | 42 | 18 | 8 | 26 | 11 | 8 | 1 | 0 | 0 | 9 | 0 | 0 | 33 | 42 |
| 03/2023 | session_2023_03.pdf | 42 | 42 | 37 | 42 | 15 | 5 | 20 | 6 | 15 | 0 | 0 | 0 | 5 | 0 | 0 | 37 | 42 |
| 04/2023 | session_2023_04.pdf | 40 | 40 | 40 | 40 | 14 | 0 | 14 | 5 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | 40 | 40 |
| 05/2023 | session_2023_05.pdf | 45 | 45 | 39 | 45 | 22 | 6 | 28 | 9 | 11 | 0 | 0 | 0 | 6 | 0 | 0 | 39 | 45 |
| 06/2023 | session_2023_06.pdf | 34 | 34 | 28 | 34 | 12 | 6 | 18 | 8 | 12 | 0 | 0 | 0 | 6 | 0 | 0 | 28 | 34 |
| 07/2023 | session_2023_07.pdf | 42 | 42 | 33 | 42 | 14 | 9 | 23 | 8 | 12 | 0 | 0 | 0 | 9 | 0 | 0 | 33 | 42 |
| 08/2023 | session_2023_08.pdf | 33 | 33 | 26 | 33 | 9 | 7 | 16 | 5 | 12 | 0 | 0 | 0 | 7 | 0 | 0 | 26 | 33 |
| 09/2023 | session_2023_09.pdf | 41 | 41 | 33 | 41 | 13 | 8 | 21 | 6 | 15 | 0 | 0 | 0 | 8 | 0 | 0 | 33 | 41 |
| 10/2023 | session_2023_10.pdf | 31 | 31 | 31 | 31 | 9 | 1 | 10 | 4 | 14 | 0 | 0 | 0 | 0 | -1 | -1 | 31 | 31 |
| 11/2023 | session_2023_11.pdf | 38 | 38 | 30 | 38 | 11 | 8 | 19 | 7 | 17 | 0 | 0 | 0 | 8 | 0 | 0 | 30 | 38 |
| 12/2023 | session_2023_12.pdf | 43 | 43 | 39 | 43 | 12 | 4 | 16 | 5 | 15 | 0 | 0 | 0 | 4 | 0 | 0 | 39 | 43 |
| 01/2024 | session_2024_01.pdf | 35 | 36 | 33 | 36 | 12 | 6 | 18 | 4 | 13 | 0 | 0 | 0 | 3 | -3 | -3 | 33 | 36 |
| 02/2024 | session_2024_02.pdf | 33 | 33 | 33 | 33 | 10 | 0 | 10 | 6 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | 33 | 33 |
| 03/2024 | session_2024_03.pdf | 34 | 34 | 31 | 34 | 9 | 4 | 13 | 7 | 10 | 0 | 0 | 0 | 3 | -1 | -1 | 31 | 34 |
| 04/2024 | session_2024_04.pdf | 42 | 42 | 39 | 42 | 14 | 5 | 19 | 5 | 10 | 0 | 0 | 0 | 3 | -2 | -2 | 39 | 42 |
| 05/2024 | session_2024_05.pdf | 46 | 46 | 39 | 46 | 14 | 5 | 19 | 5 | 14 | 2 | 0 | 0 | 7 | 0 | 0 | 39 | 46 |
| 06/2024 | session_2024_06.pdf | 40 | 40 | 37 | 40 | 16 | 3 | 19 | 5 | 15 | 0 | 0 | 0 | 3 | 0 | 0 | 37 | 40 |
| 07/2024 | session_2024_07.pdf | 34 | 34 | 33 | 34 | 11 | 2 | 13 | 7 | 12 | 0 | 0 | 0 | 1 | -1 | -1 | 33 | 34 |
| 08/2024 | session_2024_08.pdf | 39 | 39 | 37 | 39 | 10 | 5 | 15 | 6 | 16 | 0 | 0 | 0 | 2 | -3 | -3 | 37 | 39 |
| 09/2024 | session_2024_09.pdf | 39 | 39 | 34 | 39 | 15 | 5 | 20 | 9 | 12 | 0 | 0 | 0 | 5 | 0 | 0 | 34 | 39 |
| 10/2024 | session_2024_10.pdf | 49 | 49 | 43 | 49 | 16 | 6 | 22 | 7 | 16 | 0 | 1 | 0 | 6 | 0 | 0 | 43 | 49 |
| 11/2024 | session_2024_11.pdf | 43 | 43 | 41 | 43 | 19 | 2 | 21 | 7 | 13 | 0 | 0 | 0 | 2 | 0 | 0 | 41 | 43 |
| 12/2024 | session_2024_12.pdf | 39 | 39 | 40 | 39 | 14 | 0 | 14 | 4 | 17 | 0 | 0 | 0 | -1 | -1 | -1 | 40 | 39 |
| 01/2025 | session_2025_01.pdf | 44 | 44 | 39 | 44 | 10 | 5 | 15 | 2 | 18 | 0 | 0 | 0 | 5 | 0 | 0 | 39 | 44 |
| 02/2025 | session_2025_02.pdf | 45 | 45 | 41 | 45 | 18 | 4 | 22 | 9 | 14 | 0 | 0 | 0 | 4 | 0 | 0 | 41 | 45 |
| 03/2025 | session_2025_03.pdf | 21 | 21 | 21 | 21 | 11 | 0 | 11 | 5 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 21 | 21 |
| 04/2025 | session_2025_04.pdf | 29 | 29 | 21 | 29 | 10 | 8 | 18 | 5 | 6 | 0 | 0 | 0 | 8 | 0 | 0 | 21 | 29 |
| 05/2025 | session_2025_05.pdf | 50 | 50 | 47 | 50 | 23 | 3 | 26 | 13 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 47 | 50 |
| 06/2025 | session_2025_06.pdf | 41 | 41 | 36 | 41 | 15 | 5 | 20 | 8 | 11 | 0 | 0 | 0 | 5 | 0 | 0 | 36 | 41 |
| 07/2025 | session_2025_07.pdf | 34 | 34 | 29 | 34 | 12 | 5 | 17 | 8 | 12 | 0 | 0 | 0 | 5 | 0 | 0 | 29 | 34 |
| 08/2025 | session_2025_08.pdf | 50 | 50 | 41 | 50 | 15 | 9 | 24 | 9 | 10 | 0 | 0 | 0 | 9 | 0 | 0 | 41 | 50 |
| 09/2025 | session_2025_09.pdf | 31 | 31 | 25 | 31 | 11 | 6 | 17 | 10 | 10 | 0 | 0 | 0 | 6 | 0 | 0 | 25 | 31 |
| 10/2025 | session_2025_10.pdf | 51 | 51 | 41 | 51 | 19 | 10 | 29 | 12 | 9 | 0 | 0 | 0 | 10 | 0 | 0 | 41 | 51 |
| 11/2025 | session_2025_11.pdf | 47 | 47 | 39 | 47 | 10 | 8 | 18 | 3 | 17 | 0 | 0 | 0 | 8 | 0 | 0 | 39 | 47 |
| 12/2025 | session_2025_12.pdf | 51 | 51 | 41 | 51 | 12 | 10 | 22 | 6 | 16 | 0 | 0 | 0 | 10 | 0 | 0 | 41 | 51 |
| 01/2026 | session_2026_01.pdf | 37 | 37 | 31 | 37 | 10 | 7 | 17 | 7 | 13 | 0 | 0 | 0 | 6 | -1 | -1 | 31 | 37 |
| 02/2026 | session_2026_02.pdf | 39 | 39 | 36 | 39 | 12 | 3 | 15 | 3 | 17 | 0 | 0 | 0 | 3 | 0 | 0 | 36 | 39 |
| 03/2026 | session_2026_03.pdf | 44 | 44 | 41 | 44 | 17 | 3 | 20 | 7 | 14 | 0 | 0 | 0 | 3 | 0 | 0 | 41 | 44 |
| 04/2026 | session_2026_04.pdf | 47 | 47 | 41 | 47 | 0 | 0 | 17 | 5 | 15 | 5 | 0 | 0 | 6 | 1 | 1 | 41 | 47 |
| 05/2026 | session_2026_05.pdf | 42 | 42 | 40 | 42 | 0 | 0 | 21 | 8 | 6 | 3 | 0 | 0 | 2 | -1 | -1 | 40 | 42 |
| 06/2026 | session_2026_06.pdf | 45 | 45 | 40 | 45 | 0 | 0 | 16 | 9 | 10 | 3 | 0 | 0 | 5 | 2 | 2 | 40 | 45 |

## Sessions cohérentes et incohérentes selon la formule du prompt

La formule proposée dans le prompt, `candidatures corrigées − candidatures officielles − conversions − retraits − ajournés hors PDF`, doit être utilisée avec prudence. Ici, `candidatures corrigées = lignes PDF + ajournés hors PDF`; soustraire ensuite les ajournés les retire une seconde fois. La formule non ambiguë retenue pour classer les sessions est `résiduel = (lignes PDF + ajournés hors PDF) − candidatures officielles − conversions − retraits`.

Sur les données existantes, le recalcul donne **60 sessions cohérentes** et **28 sessions incohérentes** avec la formule non ambiguë. La liste de 60/28 du fichier de départ n’est donc pas reproduite telle quelle ; elle mélange vraisemblablement une autre définition de `candidatures corrigées`, des ajustements déjà intégrés et/ou des valeurs de session différentes.

### Sessions incohérentes recalculées

| Session | Résiduel sans double compte | Résiduel de la formule littérale du prompt | Interprétation prudente |
|---|---:|---|
| 04/2019 | +1 | +1 | excédent documentaire non expliqué par les ajustements identifiés |
| 07/2019 | +1 | +1 | excédent documentaire non expliqué par les ajustements identifiés |
| 09/2019 | +3 | +3 | excédent documentaire non expliqué par les ajustements identifiés |
| 10/2019 | +5 | +5 | excédent documentaire non expliqué par les ajustements identifiés |
| 11/2019 | +6 | +6 | excédent documentaire non expliqué par les ajustements identifiés |
| 01/2020 | +4 | +4 | excédent documentaire non expliqué par les ajustements identifiés |
| 03/2020 | +5 | +5 | excédent documentaire non expliqué par les ajustements identifiés |
| 04/2020 | +4 | +4 | excédent documentaire non expliqué par les ajustements identifiés |
| 05/2020 | +5 | +5 | excédent documentaire non expliqué par les ajustements identifiés |
| 06/2020 | +4 | +4 | excédent documentaire non expliqué par les ajustements identifiés |
| 08/2020 | +6 | +6 | excédent documentaire non expliqué par les ajustements identifiés |
| 09/2020 | -1 | -1 | déficit documentaire ; ligne absente, périmètre différent ou extraction à contrôler |
| 11/2020 | -1 | -1 | déficit documentaire ; ligne absente, périmètre différent ou extraction à contrôler |
| 06/2021 | -1 | -1 | déficit documentaire ; ligne absente, périmètre différent ou extraction à contrôler |
| 07/2021 | -1 | -1 | déficit documentaire ; ligne absente, périmètre différent ou extraction à contrôler |
| 09/2021 | +10 | +10 | excédent documentaire non expliqué par les ajustements identifiés |
| 01/2022 | -2 | -2 | déficit documentaire ; ligne absente, périmètre différent ou extraction à contrôler |
| 10/2023 | -1 | -1 | déficit documentaire ; ligne absente, périmètre différent ou extraction à contrôler |
| 01/2024 | -3 | -3 | déficit documentaire ; ligne absente, périmètre différent ou extraction à contrôler |
| 03/2024 | -1 | -1 | déficit documentaire ; ligne absente, périmètre différent ou extraction à contrôler |
| 04/2024 | -2 | -2 | déficit documentaire ; ligne absente, périmètre différent ou extraction à contrôler |
| 07/2024 | -1 | -1 | déficit documentaire ; ligne absente, périmètre différent ou extraction à contrôler |
| 08/2024 | -3 | -3 | déficit documentaire ; ligne absente, périmètre différent ou extraction à contrôler |
| 12/2024 | -1 | -1 | déficit documentaire ; ligne absente, périmètre différent ou extraction à contrôler |
| 01/2026 | -1 | -1 | déficit documentaire ; ligne absente, périmètre différent ou extraction à contrôler |
| 04/2026 | +1 | +1 | excédent documentaire non expliqué par les ajustements identifiés |
| 05/2026 | -1 | -1 | déficit documentaire ; ligne absente, périmètre différent ou extraction à contrôler |
| 06/2026 | +2 | +2 | excédent documentaire non expliqué par les ajustements identifiés |

## Cas obligatoires

### 03/2019
Le PDF contient 14 lignes détaillées et le commentaire officiel signale 2 ajournés. Le rapprochement correct est `14 + 2 = 16`. Les deux ajournés sont conservés séparément sans créer d’entreprises fictives et sans les compter dans les lignes PDF.

### 04/2019 et 06/2019
Les ajournements mentionnés dans les commentaires sont distingués des lignes Reporté présentes dans d’autres sessions. Aucun ajourné non identifié ne doit être fusionné avec une société existante sans preuve.

### 07/2019
La mention des Labels/Prélabels provenant de mai est une provenance historique. Elle ne doit pas être additionnée comme nouvelle candidature sans identifiant de dossier.

### 08/2019
Le détail PDF compte les lignes du tableau et conserve les conversions identifiées. Les quatre conversions annoncées dans le commentaire mais non individualisées ne sont pas transformées en entreprises inventées. Les fondateurs sont conservés tels qu’extraits, avec réserve si le PDF est ambigu.

### 05/2024 — S62
Le PDF est séparé en 39 lignes principales, 5 conversions et 2 retraits, soit 46 lignes documentaires. Les 4 dossiers administratifs sans décision publiée restent dans le détail avec leur motif administratif ; ils ne sont pas reclassés comme Reporté.

### 06/2024 — ITMMA
La formule « pitch décalé » est conservée comme commentaire de calendrier et ne doit pas être confondue automatiquement avec un Reporté décisionnel.

### 10/2024 et 11/2024 — RYBSEN
Le parcours reporté puis labellisé doit être traité longitudinalement comme un même dossier si le rapprochement est démontré ; il ne faut pas le compter comme deux candidatures indépendantes.

### Sessions 2026
Les volumes des PDF d’avril, mai et juin 2026 sont conservés dans le tableau des 88 sessions ; aucune nouvelle extraction n’a été relancée dans cette exécution.

## Anomalies et limites

La valeur **24 entries** en 10/2020 dans `session_pdf_counts.json` est une référence interne incohérente : le PDF contient 41 lignes principales + 7 conversions + 1 retrait = 49 lignes. La valeur 24 ne doit pas être utilisée.

La ligne unique par société est seulement un proxy : sans identifiant de dossier, deux noms normalisés identiques peuvent être un doublon ou deux événements, tandis qu’une même société peut apparaître sous des variantes orthographiques. La colonne `candidatures_uniques_pdf` doit donc être lue comme « sociétés distinctes après normalisation de nom », non comme une preuve de candidatures uniques.

Les PDF 12/2020 et 01/2021 ont une qualité de couche texte faible et ont été traités précédemment par OCR/contrôle visuel ; aucune nouvelle extraction n’a été faite ici.

## Verdict

Le chiffre **3 338** est infirmé par les sources disponibles. Le chiffre officiel reproductible est **3 079** ; le chiffre documentaire déjà extrait et réconcilié est **3 555** ; le chiffre documentaire corrigé est **3 558**. Le site officiel et les PDF ne comptent pas nécessairement la même unité. La conclusion la plus défendable est de publier les deux scénarios côte à côte et de ne jamais appeler 3 558 « candidatures uniques ».

## Références

[1]: https://startup.gov.tn/fr/startup_act/results "Startup Tunisia — résultats officiels"
[2]: https://github.com/bennoomenfaker/vic-2026-startup-act/tree/main/public/data/session-pdfs "88 PDF Startup Act"
[3]: https://github.com/bennoomenfaker/vic-2026-startup-act "Dépôt GitHub"
