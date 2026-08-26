# Étude quantitative du Startup Act tunisien — 88 sessions (S0–S87)
> **Périmètre statistique final.** L’étude distingue le compteur institutionnel de **3 079 candidatures officielles**, le corpus de **3 571 lignes détaillées PDF**, et le compteur corrigé de **3 574 candidatures** obtenu en ajoutant **3 ajournés hors PDF** signalés par des commentaires officiels (2 en 03/2019 et 1 en 06/2019). Ces trois mesures ne sont pas interchangeables.


**Auteur : Faker BEN NOOMEN — ESEN / ISCAE Manouba**  
**Date de consolidation : 22 août 2026**

## Résumé

Cette étude examine les 88 sessions de décision du Startup Act tunisien, de mars 2019 à juin 2026. Elle combine les compteurs officiels publiés par Startup Tunisia, les comptes rendus PDF et les exports normalisés du corpus. Le résultat principal est la présentation de deux séries distinctes : **3 571 lignes détaillées selon le corpus PDF réextrait** et **3 079 candidatures selon le site officiel**. Le corpus PDF conserve également **3 571 lignes documentaires** ; ces lignes incluent des décisions, conversions et retraits. Les trois périmètres ne sont pas fusionnés et le rapport indique toujours leur unité statistique.

Le corpus officiel agrégé contient **1 356 Labels**, **641 Prélabels**, **153 retraits officiels** et **369 conversions**. Cinq dossiers sont explicitement confirmés comme Reporté : Tunisia Biotech (02/2020), Campus Numérique des métiers (03/2020), TN Smartbot (07/2021) et RYBSEN (10/2024, examiné en novembre 2024).

## 1. Problématique et objectifs

La question de recherche est la suivante : comment mesurer la dynamique de labellisation du Startup Act lorsque les compteurs administratifs des sessions ne coïncident pas avec les lignes extraites des PDF ? L’étude poursuit trois objectifs : reconstituer une base couvrant S0–S87 ; documenter les écarts entre le compteur officiel et le registre documentaire ; et fournir des exports reproductibles pour le dashboard, le SQL, le CSV, l’Excel et la soutenance.

## 2. Sources et méthode

La base primaire est composée des comptes rendus PDF des sessions et de la page officielle [Startup Tunisia — résultats du Startup Act][1]. Les exports normalisés conservent l’identifiant de session, l’entreprise, les fondateurs, la décision brute, la catégorie normalisée, la section PDF, le commentaire et le contrôle qualité. Les nouveaux PDF d’avril, mai et juin 2026 sont intégrés comme S85, S86 et S87.

La normalisation distingue les catégories décisionnelles suivantes : `Label accordé`, `Label non accordé`, `Prélabel accordé`, `Prélabel non accordé`, `Retrait Label` et `Reporté`. Le cas administratif **Pitch décalé** est conservé comme statut documentaire distinct dans les détails : ITMMA en juin 2024 n’est pas compté comme Reporté.

> **Règle de double comptage.** Le réexamen PDF de l’étude compte les dossiers/lignes retenus manuellement et ajoute les ajournés explicitement mentionnés hors lignes ; il s’agit de la mesure analytique du corpus étudié. En parallèle, le compteur officiel de Startup Tunisia est conservé comme valeur publiée de référence. Les conversions et retraits restent visibles dans le détail PDF et ne sont pas éliminés de la mesure du réexamen PDF.

## 3. Résultats agrégés

| Indicateur | Valeur | Interprétation |
|---|---:|---|
| Sessions couvertes | 88 | S0–S87, mars 2019–juin 2026 |
| Candidatures corrigées de l’étude | 3 574 | Dossiers/lignes retenus par l’étude, avec ajournés hors lignes explicitement mentionnés |
| Candidatures selon le site officiel | 3 079 | Somme des compteurs publiés par session |
| Lignes détaillées | 3 571 | Registre des décisions/conversions/retraits |
| Écart réexamen PDF − site | +452 | Différence de périmètre documentaire et administratif |
| Labels accordés | 1 356 | Compteur officiel |
| Prélabels accordés | 641 | Compteur officiel |
| Labels + Prélabels | 1 997 | Décisions positives officielles |
| Taux descriptif Labels / candidatures | 44.0 % | Dénominateur officiel |
| Reportés confirmés | 5 | S11, S12, S28, S30, S67 |

Le taux de 44.0 % est présenté avec le dénominateur officiel de 3 079 candidatures. Une analyse complémentaire peut rapporter les mêmes Labels au réexamen PDF de 3 571 lignes détaillées, mais ce taux est une mesure analytique différente et doit être explicitement étiqueté comme telle.

## 4. Évolution annuelle

| Année | Sessions | Candidatures officielles | Labels | Prélabels | Entrées détaillées |
|---:|---:|---:|---:|---:|---:|
| 2019 | 10 | 311 | 192 | 59 | 334 |
| 2020 | 12 | 407 | 209 | 108 | 438 |
| 2021 | 12 | 478 | 243 | 103 | 583 |
| 2022 | 12 | 398 | 175 | 90 | 484 |
| 2023 | 12 | 395 | 165 | 79 | 469 |
| 2024 | 12 | 440 | 144 | 74 | 474 |
| 2025 | 12 | 421 | 153 | 87 | 492 |
| 2026 | 6 | 229 | 75 | 41 | 254 |


La lecture annuelle doit rester prudente lorsque le nombre de sessions n’est pas constant. Les variations reflètent à la fois le rythme administratif, les décisions positives et la composition documentaire des PDF.

## 5. Audit critique de S62 — mai 2024

S62 constitue le cas de contrôle le plus important. Le réexamen PDF de l’étude retient **46 dossiers/lignes observés**, tandis que le site officiel publie **39 candidatures**. Les 46 lignes comprennent les 39 dossiers du bloc de session, **5 conversions Prélabel → Label** et **2 retraits de Labels**. Les quatre dossiers administratifs (Numeryx MEA, Télésurveillance profonde des patients via une plateforme clinique de suivi médical, TECHPRO SOLUTION et HIVE) restent des dossiers observés dans le PDF, avec le statut distinct `Décision non précisée — motif administratif`.

| Élément S62 | Valeur | Traitement |
|---|---:|---|
| Candidatures selon réexamen PDF | 46 | Dossiers/lignes retenus par l’étude |
| Candidatures selon le site officiel | 39 | Compteur publié par Startup Tunisia |
| Labels accordés — total détaillé | 14 | 9 Labels initiaux + 5 conversions |
| Prélabels accordés | 5 | Décision positive |
| Labels non accordés | 7 | Décision négative |
| Prélabels non accordés | 14 | Décision négative |
| Décisions non précisées — motif administratif | 4 | Dossiers observés, sans décision normalisée publiée |
| Conversions Prélabel → Label | 5 | Lignes historiques visibles dans le PDF |
| Retraits de Labels | 2 | Lignes documentaires séparées |
| Entrées détaillées | 46 | 39 + 5 + 2 |

Ainsi, le réexamen PDF peut retenir **46 dossiers observés**, alors que le site officiel affiche **39 candidatures**. Dans le rapport, 46 est présenté comme la mesure de l’étude et 39 comme la mesure publiée ; aucune des deux valeurs n’est supprimée. Les quatre dossiers administratifs sont inclus dans le corpus observé et ne sont pas soustraits.

## 6. Reportés confirmés et corrections

| Session | Entreprise | Décision / commentaire | Conséquence |
|---|---|---|---|
| S11 — 02/2020 | Tunisia Biotech | Candidature reportée à la session suivante | Ligne Reporté, conservée dans le détail |
| S12 — 03/2020 | Campus Numérique des métiers | Candidature reportée à la session suivante | Ligne Reporté, conservée dans le détail |
| S28 — 07/2021 | TN Smartbot | Candidature reportée | Ligne Reporté, conservée dans le détail |
| S67 — 10/2024 | RYBSEN | Pitch reporté à novembre 2024 ; Label accordé en 11/2024 | Reporté dans S67, labellisation dans la session ultérieure |

Quarante-cinq lignes historiques des sessions S17–S20 avaient été normalisées à tort comme `Reporté`. Leur décision brute correspond à `Label`; la ligne TECHNOLOGIQUES SOLAIRES est confirmée `Label accordé` dans le PDF officiel de novembre 2020. Elles ont été reclassées et la trace de contrôle qualité est conservée.

## 7. Sessions 2026 ajoutées

| Session | Candidatures | Entrées | Labels | Prélabels | Conversions | Retraits documentaires |
|---|---:|---:|---:|---:|---:|---:|
| S82 — 01/2026 | 31 | 42 | 9 | 7 | 7 | 5 |
| S85 — 04/2026 | 41 | 50 | 12 | 5 | 4 | 5 |
| S86 — 05/2026 | 40 | 48 | 13 | 10 | 5 | 3 |
| S87 — 06/2026 | 40 | 47 | 7 | 9 | 4 | 3 |

Les PDF 2026 ne contiennent pas de variable de genre exploitable ; aucune inférence de genre à partir des prénoms n’est effectuée pour ces sessions.

## 8. Cohérence des exports et limites

Après correction, le SQL contient 88 sessions et 3 571 décisions détaillées sans `decision_id` dupliqué. Les champs de session enregistrent les compteurs officiels au lieu de valeurs nulles. Les catégories détaillées totalisent 1 201 Labels accordés, 659 Labels non accordés, 636 Prélabels accordés, 982 Prélabels non accordés, 45 retraits, 5 Reporté et 1 Pitch décalé ; cette distribution détaillée n’a pas vocation à remplacer les compteurs officiels.

Les données de genre et de géographie restent des indicateurs dérivés ou externes lorsqu’elles ne peuvent pas être observées directement dans chaque PDF. Les valeurs manquantes sont conservées comme telles. Toute publication doit indiquer la source, la période, l’unité statistique et le dénominateur.

## Conclusion

La base finale est cohérente si elle conserve deux séries de candidatures et un registre documentaire : **3 571 lignes détaillées selon le corpus PDF réextrait** et **3 079 candidatures selon le site officiel**, ainsi qu’un registre de **3 571 lignes documentaires**. S62 démontre pourquoi ces niveaux ne doivent pas être fusionnés : l’étude retient 46 dossiers observés, tandis que le site publie 39 candidatures. Le dashboard, les exports et la soutenance affichent désormais les deux périmètres avec leur définition respective.

## Références

[1]: https://startup.gov.tn/fr/startup_act/results "Startup Tunisia — Résultats du Startup Act"
[2]: https://github.com/bennoomenfaker/vic-2026-startup-act "Dépôt de travail et exports 88 sessions"
[3]: https://startup.gov.tn/sites/default/files/2021-11/Compte-rendu-Mars-2019.pdf "Compte rendu officiel — mars 2019"
[4]: https://startup.gov.tn/sites/default/files/2022-10/Rapport_annuel_2021_VERSIONWEB_opt_1.pdf "Rapport annuel Startup Tunisia 2021"
