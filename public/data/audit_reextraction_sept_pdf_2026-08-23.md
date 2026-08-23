# Audit de réextraction — sept PDF Startup Act

**Date de contrôle : 23 août 2026.** Les PDF officiels ont été confrontés aux entrées du corpus canonique, au classeur 88 sessions et aux compteurs publiés sur [Startup Tunisia](https://startup.gov.tn/fr/startup_act/results). Les deux séries sont conservées : **candidatures officielles** d’une part, **lignes détaillées PDF** d’autre part.

## Résultat global

| Indicateur | Valeur après synchronisation |
|---|---:|
| Sessions | 88 |
| Candidatures officielles | 3 079 |
| Labels officiels | 1 356 |
| Prélabels officiels | 641 |
| Lignes détaillées PDF | 3 555 |
| Décisions SQL | 3 555 |

## Sessions réexaminées

| Session | Vérification PDF | État après contrôle |
|---|---|---|
| 12/2019 (S9) | 42 lignes ; 32 lignes de décision et 10 conversions historiques | Cohérente en volume ; sections PDF séparées dans JSON, CSV, SQL et Excel |
| 02/2020 (S11) | 41 lignes ; 32 lignes principales et 9 conversions ; Tunisia Biotech est reportée | Cohérente ; Reporté conservé et conversions séparées |
| 07/2020 (S16) | 51 lignes ; 40 lignes principales, 9 conversions et 2 retraits | Statuts principaux réattribués d’après lecture visuelle/OCR ; limites OCR conservées dans la traçabilité |
| 09/2021 (S30) | 38 lignes ; 25 principales et 13 conversions ; SHYK est reportée | Corrigée : SHYK = **Reporté**, avec son commentaire |
| 12/2021 (S33) | 51 lignes ; retraits historiques vérifiés dans le PDF | Aucun changement de volume ; retrait documentaire maintenu séparé |
| 05/2024 (S62) | 46 lignes ; 39 candidatures officielles, 4 motifs administratifs, 5 conversions et 2 retraits | Corrigée : les quatre dossiers sont **Décision non précisée — motif administratif**, jamais Reporté |
| 04/2025 (S73) | 29 lignes ; 21 principales et 8 conversions | Corrigée : **Vegana** et **DecliTech** ajoutées aux détails |

## Interprétation de S62

Le compteur officiel de S62 reste **39 candidatures**. Le PDF contient toutefois **46 lignes documentaires** : 39 lignes du bloc de décision, 5 conversions Prélabel → Label et 2 retraits. Les quatre dossiers portant uniquement le motif administratif « Non présentation des états financiers… » restent des lignes de candidature documentées avec un statut distinct ; ils ne sont ni retranchés mécaniquement, ni transformés en Reporté.

## Incohérences restantes à surveiller

La différence entre 3 079 candidatures officielles et 3 555 lignes PDF n’est pas une erreur arithmétique : elle provient des conversions historiques, retraits, lignes documentaires supplémentaires et de la méthode institutionnelle de comptage. Les sessions dont `entries` dépasse `candidatures` doivent donc être lues avec leur section PDF, et non avec la formule `entries − reportés`.

Aucun nouvel écart de volume n’a été détecté parmi les sept PDF après corrections. Les seules réserves sont qualitatives : l’encodage du PDF S16 reste pauvre en extraction texte et certains noms de fondateurs nécessitent une validation visuelle ponctuelle ; la décision et les catégories ont été conservées sans inventer de texte illisible.

## Fichiers synchronisés

Le paquet contient les versions corrigées du JSON canonique, des JSON de sessions, des CSV, du SQL, du classeur Excel à 88 feuilles et de la source TypeScript du dashboard. La page Sessions affiche désormais **3 555 entrées détaillées** et colore les cinq sessions comportant un dossier Reporté : 02/2020, 03/2020, 07/2021, 09/2021 et 10/2024.
