# Étude quantitative du Startup Act tunisien — 88 sessions (S0–S87)

**Auteur : Faker BEN NOOMEN — ESEN / ISCAE Manouba**  
**Date de consolidation : 23 août 2026**

## Résumé

Cette étude examine les 88 sessions de décision du Startup Act tunisien, de mars 2019 à juin 2026. Elle combine les compteurs officiels publiés par Startup Tunisia, les comptes rendus PDF et les exports normalisés du corpus. Le résultat principal est une distinction nécessaire entre deux unités statistiques : **3 079 candidatures officielles** et **3 555 lignes détaillées**. La seconde population contient des décisions, conversions et retraits documentaires ; elle ne doit pas être utilisée mécaniquement comme dénominateur des taux.

Le corpus officiel agrégé contient **1 356 Labels**, **641 Prélabels**, **153 retraits officiels** et **369 conversions**. Cinq candidatures sont explicitement confirmées comme reportées : Tunisia Biotech (02/2020), Campus Numérique des métiers (03/2020), TN Smartbot (07/2021), SHYK (09/2021) et RYBSEN (10/2024, examiné en novembre 2024).

## 1. Problématique et objectifs

La question de recherche est la suivante : comment mesurer la dynamique de labellisation du Startup Act lorsque les compteurs administratifs des sessions ne coïncident pas avec les lignes extraites des PDF ? L’étude poursuit trois objectifs : reconstituer une base couvrant S0–S87 ; documenter les écarts entre le compteur officiel et le registre documentaire ; et fournir des exports reproductibles pour le dashboard, le SQL, le CSV, l’Excel et la soutenance.

## 2. Sources et méthode

La base primaire est composée des comptes rendus PDF des sessions et de la page officielle [Startup Tunisia — résultats du Startup Act][1]. Les exports normalisés conservent l’identifiant de session, l’entreprise, les fondateurs, la décision brute, la catégorie normalisée, la section PDF, le commentaire et le contrôle qualité. Les nouveaux PDF d’avril, mai et juin 2026 sont intégrés comme S85, S86 et S87.

La normalisation distingue les catégories décisionnelles suivantes : `Label accordé`, `Label non accordé`, `Prélabel accordé`, `Prélabel non accordé`, `Retrait Label` et `Reporté`. Le cas administratif **Pitch décalé** est conservé comme statut documentaire distinct dans les détails : ITMMA en juin 2024 n’est pas compté comme Reporté.

> **Règle de comptage.** Les candidatures sont le compteur officiel publié pour chaque session. Les lignes détaillées décrivent le contenu des PDF et peuvent inclure des passages historiques, des conversions ou des retraits. On ne calcule donc pas les candidatures par `entries − reportés`.

## 3. Résultats agrégés

| Indicateur | Valeur | Interprétation |
|---|---:|---|
| Sessions couvertes | 88 | S0–S87, mars 2019–juin 2026 |
| Candidatures officielles | 3 079 | Somme des compteurs par session |
| Lignes détaillées | 3 528 | Registre des décisions/conversions/retraits |
| Labels accordés | 1 356 | Compteur officiel |
| Prélabels accordés | 641 | Compteur officiel |
| Labels + Prélabels | 1 997 | Décisions positives officielles |
| Taux descriptif Labels / candidatures | 44.0 % | Dénominateur officiel |
| Reportés confirmés | 5 | S11, S12, S28, S30, S67 |

Le taux de 44.0 % est descriptif : il rapporte les Labels officiels aux candidatures officielles. Il ne s’agit pas d’un taux calculé à partir des 3 555 lignes détaillées, car celles-ci ne représentent pas une population homogène.

## 4. Évolution annuelle

| Année | Sessions | Candidatures officielles | Labels | Prélabels | Entrées détaillées |
|---:|---:|---:|---:|---:|---:|
| 2019 | 10 | 311 | 192 | 59 | 334 |
| 2020 | 12 | 407 | 209 | 108 | 463 |
| 2021 | 12 | 478 | 243 | 103 | 583 |
| 2022 | 12 | 398 | 175 | 90 | 484 |
| 2023 | 12 | 395 | 165 | 79 | 469 |
| 2024 | 12 | 440 | 144 | 74 | 474 |
| 2025 | 12 | 421 | 153 | 87 | 494 |
| 2026 | 6 | 229 | 75 | 41 | 254 |


La lecture annuelle doit rester prudente lorsque le nombre de sessions n’est pas constant. Les variations reflètent à la fois le rythme administratif, les décisions positives et la composition documentaire des PDF.

## 5. Audit critique de S62 — mai 2024

S62 constitue le cas de contrôle le plus important. Le PDF distingue **39 candidatures du bloc principal**. Il contient en outre **5 passages historiques de Prélabel vers Label** et **2 retraits de Labels**, soit **46 enregistrements documentaires**. Les 4 dossiers administratifs (Numeryx MEA, Télésurveillance profonde des patients via une plateforme clinique de suivi médical, TECHPRO SOLUTION et Hive) portent le statut distinct `Décision non précisée — motif administratif` ; ils ne sont pas reportés et ne sont pas classés comme Label non accordé.

| Élément S62 | Valeur | Traitement |
|---|---:|---|
| Candidatures officielles | 39 | Dénominateur de session |
| Labels accordés dans le bloc principal | 9 | Compteur de décision |
| Prélabels accordés | 5 | Compteur de décision |
| Labels non accordés | 7 | Décision négative publiée |
| Prélabels non accordés | 14 | Décision négative |
| Conversions Prélabel → Label | 5 | Lignes historiques, hors candidatures nouvelles |
| Retraits de Labels | 2 | Lignes documentaires séparées |
| Entrées détaillées | 46 | 39 + 5 + 2 |

Ainsi, le calcul `46 − 0 reporté = 46` ne restitue pas le compteur officiel de 39. Cette différence n’est pas une erreur arithmétique : elle résulte d’unités documentaires différentes.

## 6. Reportés confirmés et corrections

| Session | Entreprise | Décision / commentaire | Conséquence |
|---|---|---|---|
| S11 — 02/2020 | Tunisia Biotech | Candidature reportée à la session suivante | Ligne Reporté, conservée dans le détail |
| S12 — 03/2020 | Campus Numérique des métiers | Candidature reportée à la session suivante | Ligne Reporté, conservée dans le détail |
| S28 — 07/2021 | TN Smartbot | Candidature reportée | Ligne Reporté, conservée dans le détail |
| S30 — 09/2021 | SHYK | Candidature reportée à la session de septembre | Ligne Reporté, conservée dans le détail |
| S67 — 10/2024 | RYBSEN | Pitch reporté à novembre 2024 ; Label accordé en 11/2024 | Reporté dans S67, labellisation dans la session ultérieure |

Quarante-cinq lignes historiques des sessions S17–S20 avaient été normalisées à tort comme `Reporté`. Leur décision brute correspond à `Label`; la ligne TECHNOLOGIQUES SOLAIRES est confirmée `Label accordé` dans le PDF officiel de novembre 2020. Elles ont été reclassées et la trace de contrôle qualité est conservée.

## 7. Sessions 2026 ajoutées

| Session | Candidatures | Entrées | Labels | Prélabels | Conversions | Retraits documentaires |
|---|---:|---:|---:|---:|---:|---:|
| S85 — 04/2026 | 41 | 47 | 12 | 5 | 4 | 5 |
| S86 — 05/2026 | 40 | 42 | 13 | 10 | 5 | 3 |
| S87 — 06/2026 | 40 | 45 | 7 | 9 | 4 | 3 |

Les PDF 2026 ne contiennent pas de variable de genre exploitable ; aucune inférence de genre à partir des prénoms n’est effectuée pour ces sessions.

## 8. Cohérence des exports et limites

Après correction, le SQL contient 88 sessions et 3 555 décisions sans `decision_id` dupliqué. Les champs de session enregistrent les compteurs officiels au lieu de valeurs nulles. Les catégories détaillées totalisent 1 232 Labels accordés, 653 Labels non accordés, 634 Prélabels accordés, 980 Prélabels non accordés, 46 retraits, 5 Reporté, 4 décisions administratives non précisées et 1 Pitch décalé ; cette distribution détaillée n’a pas vocation à remplacer les compteurs officiels.

Les données de genre et de géographie restent des indicateurs dérivés ou externes lorsqu’elles ne peuvent pas être observées directement dans chaque PDF. Les valeurs manquantes sont conservées comme telles. Toute publication doit indiquer la source, la période, l’unité statistique et le dénominateur.

## Conclusion

La base finale est cohérente si elle conserve deux niveaux de vérité : le niveau administratif officiel, avec 3 079 candidatures et les compteurs par session, et le niveau documentaire, avec 3 555 lignes détaillées. S62 démontre pourquoi ces niveaux ne doivent pas être fusionnés. Le dashboard affiche les deux périmètres ; les cinq Reporté sont signalés en terracotta ; les conversions et retraits restent documentés sans gonfler le nombre de candidatures.

## Références

[1]: https://startup.gov.tn/fr/startup_act/results "Startup Tunisia — Résultats du Startup Act"
[2]: https://github.com/bennoomenfaker/vic-2026-startup-act "Dépôt de travail et exports 88 sessions"
[3]: https://startup.gov.tn/sites/default/files/2021-11/Compte-rendu-Mars-2019.pdf "Compte rendu officiel — mars 2019"
[4]: https://startup.gov.tn/sites/default/files/2022-10/Rapport_annuel_2021_VERSIONWEB_opt_1.pdf "Rapport annuel Startup Tunisia 2021"
