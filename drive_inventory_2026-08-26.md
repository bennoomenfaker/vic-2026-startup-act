# Inventaire initial du dossier Google Drive public

Dossier racine : [Projet Livre Blanc Startup Act](https://drive.google.com/drive/folders/1hyLN9oY9BN6DCVORPYP8zQmejkqI9M68)

Le dossier est accessible sans connexion. Les sous-dossiers visibles sont :

| Dossier | Rôle présumé |
|---|---|
| 00_Gouvernance | Gouvernance et organisation |
| 01_Modèles | Modèles |
| 02_Cadrage | Cadrage de l’étude |
| 03_Collecte | Collecte des données |
| 04_Analyse | Analyses |
| 05_Rapports | Rapports |
| 06_Livre Blanc | Livre blanc |
| 07_Références_documentaires | Références documentaires |
| 08_Formation | Formation |
| 09_Communication | Communication |

La pièce jointe `pasted_content_17.txt` contient surtout des reformulations de problématiques et d’hypothèses pour les axes 1 à 6 du plan de veille. Elle pourra alimenter une section méthodologique ou un plan de veille, mais elle ne constitue pas une nouvelle mesure statistique du corpus Startup Act.


Le HTML dynamique du dossier racine a été sauvegardé par le navigateur. L’accès est bien public et le nom du projet est « Projet Livre Blanc Startup Act ». Les sous-dossiers sont chargés comme lignes Drive, mais leurs identifiants ne sont pas exposés dans le texte Markdown ; ils seront extraits du HTML/JavaScript sauvegardé ou ouverts par navigation directe.


Les dossiers 04_Analyse et 05_Rapports sont accessibles comme conteneurs, mais leur contenu n’est pas lisible anonymement : Drive affiche « Sign in to add files to this folder » et aucun fichier n’est listé. Cela indique que le dossier racine est public, tandis que les sous-dossiers peuvent avoir des permissions distinctes ou nécessiter la session Google du propriétaire. Aucun document analytique supplémentaire ne peut encore être importé à partir de ces deux sous-dossiers sans lien de fichier direct ou accès autorisé.


Le dossier **02_Cadrage** est lisible publiquement et contient six sous-dossiers d’axes d’étude, un dossier « Chartes Projet veille » et un Google Doc intitulé **FICHE MÉTHODOLOGIQUE_Phase Cadrage** (8 KB, modifié le 15 août). Les six axes sont : état des lieux quantitatif, cadre juridique et gouvernance, financement, accompagnement et écosystème, évaluation des impacts, benchmark international. Ce dossier est la source la plus prometteuse pour enrichir la page méthodologique ; il faut encore ouvrir le Google Doc et les axes pour lire leur contenu.


Le dossier **Axe d’étude 1 — État des lieux quantitatif du Startup Act** est accessible publiquement. Il contient : un dossier Historique, une Google Doc **AE1 - CHARTE DE CADRAGE - livre blanc startup** (14 KB), une Google Doc **AE1 — PLAN DES INSTRUMENTS DE COLLECTE** (16 KB) et une Google Sheet **AE1_PLAN DE VEILLE & COLLECTE** (4 KB). Ces fichiers sont directement pertinents pour la page d’étude quantitative, la méthodologie et la future collecte ; ils doivent être lus avant toute intégration.


Documents de l’Axe 1 lus et téléchargés :

| Document | Apport vérifiable | Décision d’intégration |
|---|---|---|
| Charte de cadrage AE1 | Problématique, objectifs OS1–OS5, périmètre 2018–2026, sources prioritaires, risques et contrôle qualité | À intégrer comme cadre méthodologique, sans modifier les chiffres |
| Plan des instruments AE1 | Grille d’extraction des PV, demande de données institutionnelles, sources RNE/CNSS/INNORPI, questionnaire complémentaire et traçabilité | À intégrer comme méthode de collecte et dictionnaire de provenance |
| Plan de veille AE1 | 25 lignes opérationnelles couvrant candidatures, conversions, retraits, profils, territoire, secteurs, DeepTech et PI | À intégrer comme plan de veille ; les indicateurs non observés ne doivent pas être présentés comme résultats |

Le Drive apporte donc surtout une **méthodologie structurée**, pas de nouveaux compteurs validés du corpus 88 sessions. Les données du dashboard doivent rester fondées sur les PDF et les compteurs /results ; les variables proposées mais non présentes dans le corpus doivent être affichées comme « à collecter » ou « indisponibles », jamais comme valeurs estimées.


Le dossier **03_Collecte** contient le sous-dossier **Startup act data scrape by Faker** (identifiant Drive `1g-LOfaHV5CQYh6saz4EBEm37pj1aDthc`, modifié le 22 août). Il s’agit potentiellement d’une seconde copie ou d’un complément du corpus scrappé du dépôt GitHub. Ce sous-dossier doit être comparé aux exports canoniques avant toute intégration afin d’éviter un double comptage ou une divergence de source.


Le sous-dossier **Startup act data scrape by Faker** est riche en livrables : trois sous-dossiers (`json_generated_from_excel`, `rapport_academique_assets`, `startup-act-export`), plusieurs fichiers Excel 85 sessions, deux JSON normalisés de 7,3 MB, un SQL de 2,8 MB, deux CSV géographiques, un texte **Étude quantitative du Startup Act tunisien** (27 KB), un rapport Markdown de base normalisée, un résumé `SUMMARY.json`, et un fichier **Vérification candidatures versus entrées.md**. Il contient aussi les extractions Excel des sessions 04/2026, 05/2026 et 06/2026. Les fichiers analytiques prioritaires à lire sont le texte d’étude, SUMMARY.json, la vérification candidatures/entrées, les CSV géographiques et le Markdown de base normalisée.


Le dossier de données scrappées contient un `SUMMARY.json` qui annonce encore **85 fichiers, 1 311 Labels et 623 Prélabels**, avec 21 avertissements de qualité. Le comparateur local confirme que le canonique du dépôt contient **88 sessions et 3 571 lignes**. Le SUMMARY et l’étude quantitative du Drive sont donc des versions historiques (21 août) et ne doivent pas remplacer les exports corrigés du dépôt. Une tentative de téléchargement direct du fichier de vérification a expiré côté Drive ; ce fichier reste à récupérer via le navigateur ou un lien de téléchargement valide.


Le dossier **06_Livre Blanc** est vide pour un accès public anonyme. Le dossier **07_Références_documentaires** est accessible et contient six PDF : rapport annuel 2021 en anglais, décret 2018-417 en arabe, PDF « Label Results — Startup Tunisia », rapport annuel 2021 en français, document sur le cadre juridique du Startup Act et `Ta2018201.pdf`. Ces fichiers peuvent servir de références institutionnelles et juridiques, mais ils ne doivent être ajoutés au dashboard comme nouvelles observations quantitatives qu’après contrôle du périmètre et des doublons avec les sources déjà présentes dans le dépôt.


Le dossier **01_Modèles** contient trois sous-dossiers : `Cadrage`, `Qualité` et `Templates`. Il peut servir de référence de structure, mais aucun contenu analytique n’a encore été importé. Le dossier **09_Communication** contient un seul PDF `Présentation forum.pdf` de 1,9 MB ; il s’agit d’un support de communication à examiner séparément, pas d’une nouvelle source statistique. Les dossiers 00_Gouvernance et 08_Formation n’ont pas encore révélé de contenu analytique dans l’inventaire racine ; ils restent secondaires pour la demande actuelle.
