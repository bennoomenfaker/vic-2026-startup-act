# Audit du dossier Drive `startup-act-export`

## Accès et périmètre

Le dossier suivant est accessible en lecture seule depuis le navigateur :

`https://drive.google.com/drive/folders/1iHuPeTEDgVptQjWWNehsnw0QarPT5r4B?usp=drive_link`

Le téléchargement « Tout télécharger » a réussi le 22 août 2026. L’archive contient 13 éléments principaux : plusieurs classeurs 88 sessions, `startup_act_database.sql`, `SUMMARY.json` et le dossier `csv_88_sessions_final`.

## Résumé du verdict

Le dossier Drive est **accessible**, mais ses fichiers ne sont pas homogènes et ne peuvent pas encore être validés comme paquet final unique.

| Contrôle | Fichier Drive | Référence de réextraction PDF locale | Verdict |
|---|---:|---:|---|
| Sessions | 88 dans `SUMMARY.json` et les CSV S0–S87 | 88 | Conforme |
| Lignes CSV par session | 3 527 | 3 528 | Une ligne manquante |
| Candidatures du résumé | 3 493 | 3 079 officielles | Source de comptage différente, à documenter |
| Labels du résumé | 1 343 | 1 356 officiels | Divergence |
| Prélabels du résumé | 645 | 641 officiels | Divergence |
| SQL `INSERT decisions` | 3 528 | 3 528 | Volume écrit conforme |
| IDs SQL réellement uniques | 3 521 | 3 528 attendus | 7 doublons, chargement SQLite en échec |
| Compteurs Excel officiels | S0–S84 seulement + total ancien | S0–S87 | Incomplet |

## Anomalie S62

Le dossier Drive contient 45 lignes pour S62 alors que la réextraction PDF canonique contient 46 lignes documentaires. L’écart est explicable par trois transformations dans le CSV Drive :

1. `ACRIDIDEA` et `culturify` sont fusionnés dans une seule ligne « ACRIDIDEA culturify DourbIA » ;
2. le nom long de « Télésurveillance profonde des patients via une plateforme clinique de suivi médical » est coupé en deux lignes ;
3. `NEXT PROTEIN TUNISIA` et `COGNIRA TUNISIA` sont fusionnés dans une seule ligne.

Le bilan net est donc 46 − 1 + 1 − 1 = 45. Cette représentation n’est pas adaptée à une base relationnelle où chaque société et chaque décision doit conserver sa propre ligne.

## Anomalie des classeurs `Compteurs_Officiels`

Les classeurs `88_sessions_scraped.xlsx` et `Faker88session_corrigee_compteurs_officiels.xlsx` possèdent 94 feuilles, mais leur feuille `Compteurs_Officiels` ne contient que 86 identifiants de session non vides : S0–S84, puis une ligne vide et une ligne `TOTAL`. Les sessions S85, S86 et S87 ne figurent pas dans cette feuille de compteurs.

La ligne `TOTAL` de cette feuille conserve les anciens totaux : **1 311 Labels, 623 Prélabels, 1 934 décisions positives et 142 retraits**. Elle ne reflète donc pas les trois sessions 2026 ajoutées dans le reste du classeur. Le fait que les feuilles S85–S87 existent ailleurs ne corrige pas cette absence dans la table officielle agrégée.

## Anomalie du SQL Drive

Le SQL contient les volumes suivants :

| Table | Instructions `INSERT` |
|---|---:|
| `sessions` | 88 |
| `companies` | 3 229 |
| `founders` | 3 186 |
| `company_founders` | 3 591 |
| `decisions` | 3 528 |

Cependant, une exécution SQLite du SQL échoue sur `UNIQUE constraint failed: decisions.decision_id`. Le contrôle syntaxique trouve **3 528 IDs écrits, 3 521 IDs uniques et 7 IDs répétés**. Les identifiants concernés sont : `2b6b5c0c6c36`, `10cd542efdbe`, `a74f4c9748a6`, `9780dd8b85e2`, `b9381eff7615`, `3ed1eb6f859b` et `8fd2378a1046`.

Certaines répétitions correspondent effectivement à plusieurs décisions documentaires concernant la même entreprise, mais cela ne justifie pas la réutilisation de la même clé primaire. Il faut conserver les lignes et attribuer un identifiant unique à chaque décision.

## Conclusion opérationnelle

Le lien Drive est fonctionnel et les fichiers ont pu être téléchargés. Le dossier est utile comme source de comparaison, mais il n’est pas encore une version finale cohérente : `SUMMARY.json` utilise une série 3 493/1 343/645, la feuille Excel officielle reste à 85 sessions, le CSV S62 fusionne des sociétés, et le SQL ne se charge pas dans SQLite.

Le paquet local `reextraction_validee_88` reste la version recommandée pour les exportations corrigées : il conserve séparément les 46 lignes S62, les 88 sessions, les fondateurs non renseignés sans invention et les IDs SQL uniques. Les valeurs Drive ne doivent pas être fusionnées automatiquement avec cette version sans décision préalable sur la source officielle des compteurs.
