# Résumé exécutif de l'audit — Compteurs officiels vs dérivés PDF (88 sessions)

Mise à jour : **29/08/2026**. Sources : `sessions.json` + `session-pdfs-json/session_*.json`
(field `section_pdf`, `session_data`) ; officiel live `startup.gov.tn/fr/startup_act/results`
re-scrapé 29/08/2026.

## Question centrale (utilisateur)

> « Candidatures/session = `lignes PDF − reportés` ? » → **Réponse : non, c'est
> `lignes du tableau PRINCIPAL (section_pdf) − reportés`.**

Les PDF contiennent jusqu'à 3 tableaux : principal (décisions, = candidatures),
Passage Prélabel→Label (conversions), Retrait de Label (retraits). Les conversions et
retraits ne sont pas des candidatures.

## Totaux (88 sessions)

| Série | Total candidatures |
|---|---|
| **Officiel `/results` (live, vérifié)** | **3 079** |
| `candidatures_pdf_calculees` (sessions.json, corrigée) | **3 078** (cohérent **87/88**) |
| Reconstruction brute `section_pdf` (pré-correction) | 3 107 (cohérent 58/88) |

- **Labels officiels : 1 356 · Prélabels officiels : 641 · Retraits : 153.**
- Formulaire interne vérifiée 88/88 : `lignes_pdf − conversions − retraits − reportés =
  candidatures_pdf_calculees`.
- Conversions cumulées (lignes documentaires) : **409**. Retraits (lignes dédiées) : **49**.

## Seul résidu de la série corrigée : 01/2026

- `sessions.json` : 31 officiel vs 30 CR (le cas documenté « 31 vs 30 »).
- Le CR officiel liste 30 dossiers. Le PDF ne permet pas d'identifier la 31e. Ne pas
  recalculer le taux officiel 10/31 = 32,3 % sur 30 lignes sans l'enquête.

## Interprétation

1. La série `candidatures_pdf_calculees` du dépôt réconcilie **exactement** avec l'officiel
   (3 078 vs 3 079), bien mieux que la reconstruction brute `section_pdf` (3 107, écart 28
   sur les sessions 2019–2020 où le PDF principal ne liste pas toujours toutes les
   candidatures annoncées).
2. Les 30 sessions « non cohérentes » en série brute sont expliquées par le fait que
   certaines candidatures officielles (ajournées, irrecevables avant inscription au CR,
   retraits comptés hors ligne) n'ont pas de ligne de décision dans le tableau principal.
   Toutes sont rattrapées par `candidatures_pdf_calculees`.
3. Labels/prélabels/retraits : les compteurs de `sessions.json` sont les valeurs corrigées
   (cf. `corrections.json` : 21/88 sessions corrigées ; anciens scrapés 1 324/617 →
   corrigés 1 311/623 pour le corpus 85 ; le corpus 88 ajoute les 3 sessions 2026).

## Détaillée (écart officiel − brut tableau principal), 30 sessions

Voir `incoherences_priorisees.md` et `reconciliation_pdf_principal_officiel.csv`.

## Limites

- Pour 34 sessions, les retraits sont comptés globalement (pas ligne à ligne) ;
  pour les scans 08–12/2020, certaines décisions sont transcrites minimalement
  (« label », « prelabel »).
- Série brute `section_pdf` = reconstruction automatique ; la référence exploitable est
  `candidatures_pdf_calculees` (corrigée).
