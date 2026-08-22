# Validation de la réextraction — 88 sessions

La réextraction couvre **88 PDF**, **88 JSON de session** et **3 528 entrées détaillées**. Les compteurs officiels sont conservés séparément : **3 079 candidatures**, **1 356 Labels**, **641 Prélabels**, **369 conversions**, **153 retraits** et **4 Reporté détaillés**.

## Contrôle PDF et OCR

Les 88 PDF possèdent une clé de session unique. Les noms d’entreprise ont été retrouvés dans le texte PDF/OCR pour 3 465 lignes sur 3 528 (98,21 %). Les mots-clés de décision ont été retrouvés pour 3 396 lignes (96,26 %). Les PDF 12/2020 et 01/2021 ont nécessité un OCR français/anglais supplémentaire, car leur couche texte était absente ou incomplète.

Treize lignes n’exposent pas de fondateur exploitable dans la source structurée. Elles sont conservées comme **Non renseigné** ; aucun nom n’a été inventé. Ces 13 lignes concernent exclusivement des retraits de Label : 2 en 05/2024, 5 en 04/2026, 3 en 05/2026 et 3 en 06/2026.

## Comparaison avec les anciens exports

L’ancien CSV 88 contient les mêmes 3 528 lignes et les mêmes 88 sessions, mais sept décisions individuelles diffèrent. La recherche directe dans les PDF confirme la réextraction canonique pour les sept cas : **فرید حول العالم** (07/2020) est Label non accordé ; **Bridges S.A** (02/2021) est Prélabel accordé ; **allcarta** (12/2021) est Label accordé ; **Hayat Tech** (01/2022) est Prélabel accordé ; **Kiddo** (02/2022) est Label accordé ; **The Vastlight Platform** (08/2022) est Label accordé ; **Catchy** (01/2024) est Label accordé. Les valeurs de l’ancien CSV sont donc erronées pour ces sept lignes.

## Règle de comptage

Les candidatures officielles sont les compteurs publiés par session. Les entrées détaillées sont les lignes documentaires extraites des PDF/JSON. Les deux périmètres ne doivent pas être forcés à égalité par une formule unique. Les Reporté, conversions et retraits sont des statuts ou événements documentaires séparés.

## Fichiers produits

Le classeur contient une synthèse, les compteurs des 88 sessions, les décisions détaillées, les entreprises, les fondateurs, le contrôle qualité et une feuille dédiée pour chacune des 88 sessions. Le SQL contient une table explicite `session_official_counts` et des identifiants de décisions uniques. Les fichiers Drive n’ont pas pu être comparés car les deux dossiers ont renvoyé une erreur d’authentification Google 401 ; aucun fichier Drive n’a été modifié.
