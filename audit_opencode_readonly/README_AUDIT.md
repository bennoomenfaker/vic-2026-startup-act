# Audit VIC Startup Act — Dossier « read-only » (aucun fichier source modifié)

Cet audit est **en lecture seule** : il ne modifie ni le code, ni les sources de données,
ni le site. Tous les livrables sont produits dans `audit_opencode_readonly/`.

## Question de l'utilisateur (rappel)

> « Candidatures/session : je compte `lignes PDF − reportés`. Est-ce exact ? »
> Et : « Pourquoi le tableau `/sessions` du site ne coïncide pas toujours avec le PDF ? »

## Réponse méthodologique — LA découverte centrale

Les PDF des comptes-rendus contiennent **jusqu'à 3 tableaux physiques distincts**,
encodés dans le champ `section_pdf` des `entrees` :

| Tableau physique (PDF) | `section_pdf` | Signification |
|---|---|---|
| **Tableau principal** (pitch/décisions) | `Session de décision` (ou `candidature` pour 2026) | = les candidatures |
| **Passage Prélabel → Label** | `Passage Prélabel → Label`, `Passage de Prélabels aux Labels`, `conversion` | conversions — **PAS** des candidatures |
| **Retrait de Label** | `Retrait de Label Startup`, `retrait`, `Retraits Labels` | retraits — **PAS** des candidatures |

**Donc : la formule correcte est**

> `candidatures PDF = lignes du tableau PRINCIPAL − reportés`

et pas simplement `toutes les lignes − reportés`, car les conversions (409) et les
retraits (49) ne sont pas des candidatures.

### Preuve chiffrée

| Série | Total | Sessions cohérentes avec l'officiel |
|---|---|---|
| Compteur officiel `/results` (live, vérifié 29/08/2026) | **3 079** | — |
| `candidatures_pdf_calculees` (sessions.json, déjà corrigée `lignes − conv − retraits − reportés`) | **3 078** | **87/88** (seul écart : 01/2026, le cas documenté « 31 officiel vs 30 CR ») |
| Reconstruction brute `section_pdf` tableau principal − reportés | 3 107 | 58/88 (les 30 autres sont les sessions 2019–2020 non pré-corrigées) |
| Ancienne série « toutes lignes − reportés » (obsolète) | 3 097 | — |

**Verdict :** la série `candidatures_pdf_calculees` du dépôt est **correcte et mieux
réconciliée** que la reconstruction brute. Le seul écart restant (01/2026, −1) est
exactement le cas documenté dans `corrections.json` / AGENTS.md (« 31 officiel vs
30 CR », la 31e ligne n'étant pas identifiée dans le PDF).

## Les deux séries à ne JAMAIS confondre

1. **Série institutionnelle** = compteur publié par session sur `startup.gov.tn/fr/startup_act/results` :
   **3 079 candidatures / 1 356 labels / 641 prélabels / 153 retraits**. Source de
   vérité institutionnelle (confirmée par re-scrape live en 08/2026).
2. **Série documentaire PDF** = lignes physiques des 88 comptes-rendus (3 tableaux par
   PDF). Chaque ligne reçoit une catégorie ; conversions et retraits sont conservés
   comme lignes documentaires mais ne sont pas des candidatures distinctes.

On ne doit pas additionner ni mélanger les deux : l'écart « official vs documentaire »
est structurel et documenté (cf. AGENTS.md, `corrections.json`, `reconciliation_88_pdf_primary.json`).

## Écart « 01/2026 » — seul résidu de la série corrigée

- `sessions.json` : 31 officiel vs 30 CR (`candidatures_pdf_calculees`).
- Le CR officiel (`manual_sessions/2026_01.json`) liste 30 dossiers ; 3 labels accordés,
  7 prélabels, 6 labels refusés, 13 prélabels refusés, 1 irrecevable. Le PDF ne permet
  pas d'identifier la 31e candidature. Documenté ; **ne pas recalculer le taux**
  10/31 = 32,3 % sur la base de 30.

## Livrables produits (dans ce dossier)

| Fichier | Contenu |
|---|---|
| `reconciliation_pdf_principal_officiel.csv` | Par session : officiel vs tableau principal PDF (section_pdf), conversions, retraits |
| `reconciliation_series_pdf_2026.csv` | Par session : les 3 séries PDF (pdf_calc, reexamen, section_principal) vs officiel |
| `incoherences_priorisees.md` | Liste priorisée des incohérences à expliquer/vérifier |
| `controle_s62.md` | Contrôle ligne à ligne de la session S62 (05/2024) |
| `comparaison_sessions_88.csv` | Comparaison officiel vs `entries` brutes (série obsolète, conservée pour mémoire) |
| `ajournements_reports.csv`, `SYNTHESE_AJOURNEMENTS.md` | Dossiers rapportés / ajournés |
| `resume_audit.md` | Résumé exécutif (mis à jour) |
| `verif_pdf_groupe1.md`, `verif_pdf_groupe2.md` | Vérifications PDF manuelles par groupe |

## Recommandations au site (propositions, non appliquées ici)

1. Afficher clairement que **le tableau `/sessions` mélange en réalité les compteurs
   officiels et les lignes PDF** — distinguer les colonnes « compteur officiel » et
   « lignes documentaires PDF ».
2. Documenter la règle des 3 tableaux par PDF dans une infobulle/note de la page
   « Corrections ».
3. Ajouter l'écart structurel (3 078 vs 3 079, uniquement 01/2026) comme note de bas de
   page plutôt que de le masquer.
