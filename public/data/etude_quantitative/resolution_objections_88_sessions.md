# Résolution des deux objections méthodologiques (contradiction + hypothèse 2e tour)

Vérifié sur disque et sur les données réelles (29/08/2026). Répond aux deux points soulevés
par la revue avant toute publication dans le mémoire.

---

## Objection 1 — Contradiction « 82/85 conformes » vs « 55/88 labels »

**Verdict : c'est une fausse contradiction (hypothèse A : deux métriques différentes),
PAS un bug.** Confirmé en lisant `comparaison_json_vs_pdf.md` + `parse_pdfs_v7.py` +
`dashboard_data.json`.

### Ce que mesure réellement chaque chiffre

| Chiffre | Ce qu'il compare | Référentiel |
|---|---|---|
| **82/85 « conformes »** (`comparaison_json_vs_pdf.md`) | `labelsCorriges` (PDF v7) **vs l'ancien JSON scrapé** `labels` | L'ancien JSON scrapé de l'époque, qui **n'est PAS** le compteur officiel actuel |
| **55/88 « labels »** (mon analyse récente) | `resultat_normalise` brut des `session-pdfs-json` **vs le compteur officiel live `/results` actuel** | Compteur officiel live 2026, corrigé depuis |

### Preuve décisive (par session, pour l'ère 2019)

| Session | md « JSON » (ancien scrapé) | md « PDF v7 » (corrigé) | Live officiel 2026 |
|---|---|---|---|
| 06/2019 | 14 | 14 | **15** |
| 07/2019 | 14 | 14 | **15** |
| 08/2019 | 20 | 20 | **24** |
| 09/2019 | 15 | 15 | 15 |
| 10/2019 | 23 | 23 | 23 |
| 11/2019 | 17 | 17 | 17 |

Le doc `comparaison_json_vs_pdf.md` prouve donc seulement que **le parseur PDF reproduit
fidèlement l'ancien JSON scrapé** (auto-cohérence interne) — c'est vrai. Mais cet ancien
JSON scrapé avait des valeurs de labels de 2019 **plus basses que le compteur officiel
actuel** (ex. 08/2019 : 20 au lieu de 24). D'où l'impression de contradiction : ce sont
deux référentiels différents, pas deux lectures du même fait.

### Conclusion Objection 1

- **Aucun des deux chiffres (82/85 ni 55/88) ne doit être cité comme « la » vérité** — les
  deux sont vrais dans leur propre définition, et le reviewer a raison sur ce point.
- La référence officielle correcte = `labelsOfficiels` (somme = **1 356**, vérifiée).
- La série PDF corrigée = `labelsCorriges` (somme = **1 343**). La série `resultat_normalise`
  brute (= ~1 233) est un **sous-comptage d'extraction** pour l'ère 2019-2021 (scans + classifier),
  à ne JAMAIS afficher comme total labels.

---

## Objection 2 — Hypothèse « dossier reporté en 2e tour » (09/2021, 11/2019)

**Verdict : partiellement confirmée — elle explique une partie réelle mais INCOMPLÈTE des écarts.**
Testé en croisant les noms du tableau principal de chaque session avec toutes les sessions
précédentes.

### 09/2021 (officiel 15, main-table 25 lignes)

- Candidatures du tableau principal : 25 noms distincts.
- **1 seul** (GARK) apparaît aussi dans une session précédente (05/2020, où il était
  « Prélabel non accordé » → 2e passage en 09/2021 « Prélabel accordé »).
- 1 ligne explicitement « Reporté » (SHYK).
- → Même après SHYK (reporté) + GARK (2e passage), il reste **~23 noms réellement nouveaux**
  dans le PDF de 09/2021, alors que l'officiel ne compte que **15**.
- **L'hypothèse 2e tour n'explique que ~2 des ~10 d'écart.** Le reste est un vrai écart
  officiel-pdf non expliqué par le report.

### 11/2019 (officiel 35, main-table 41 lignes)

- Candidatures du tableau principal : 41 noms distincts.
- **4 noms** (athena-io, eat & fit, minima.ai, rhintos games) apparaissent aussi dans des
  sessions précédentes (07→10/2019) → 2e passages.
- → 41 − 4 (2e tour) = 37, officiel = 35. Il reste **2 d'écart** non expliqués.
- Hypothèse 2e tour explique **4 des 6** d'excédent, mais pas tout.

### Objection 2 bis — Double contrôle avec matching FLOU + dédoublonnage intra-session

Deux réserves de la revue ont été testées sur les données réelles :

**A. Dédoublonnage intra-session.** Vérifié sur les 88 sessions : 5 sessions présentent un
nom répété dans la section candidature du même compte-rendu (07/2020, 12/2021, 02/2022,
08/2022, 01/2024 : 1 seul doublon chacune, probablement un tableau répété sur la coupure de
page). Les comptages de cette audit utilisent des **noms distincts**, donc ce biais est déjà
filtré. L'écart 09/2021 n'est PAS issu d'un doublon intra-session (25 noms distincts).

**B. Matching flou inter-session (difflib.get_close_matches, cutoff 0.80).** Résultat
**négatif** : le flou n'a **pas** refermé l'écart, il a au contraire introduit de **faux
positifs**. Exemples vérifiés manuellement :
- `educart` : aucun précédent réel (faux positif) ;
- `ng technologies` : ses seuls précédents sont 07/2020 et 10/2020, soit **après** 11/2019
  (donc pas un 2e tour avant 11/2019) ;
- les 4 vrais précédents de 11/2019 (athena-io, eat & fit, minima.ai, rhintos games) le sont
  déjà en matching exact ; et `eat & fit` était **Label accordé en 08/2019** puis réapparaît
  « Prélabel accordé » en 11/2019 — suspect (une société labellisée ne se recandidate pas en
  prélabel), typique d'un doublon de nom ou d'un réexamen, pas d'une nouvelle candidature.

**Conclusion Objection 2 (définitive).** En matching exact comme en flou, l'hypothèse
2e tour ne referme **pas** l'écart :
- 11/2019 : les 4 correspondances exactes sont réelles mais douteuses (eat & fit), l'écart
  brut (41 vs 35) repose sur des sociétés réellement listées dans le PDF, pas des doublons.
- 09/2021 : il ne reste **pas moins de 23-24** noms distincts « nouveaux » dans le PDF contre
  15 officiels, même après matching flou.

Donc la formulation « une partie imputable au 2e passage, le reste à documenter ligne à
ligne » est confirmée — et **le résidu reste réel** pour 09/2021. On ne peut pas affirmer
catégoriquement que le site « sous-compte » ; on documente un écart à expliquer PDF par PDF.

---

## Recommandation finale pour le mémoire

1. **Ne publier comme label officiel que `labelsOfficiels` (1 356)** et comme candidatures
   officielles que le compteur `/results` (3 079). C'est la seule vérité institutionnelle.
2. **Présenter `labelsCorriges` (1 343) / `candidatures_pdf_calculees` (3 078) comme une
   « série PDF ajustée pour rapprochement »**, jamais comme une mesure PDF indépendante ni
   comme un total canonique à part entière.
3. **Écarter la série `resultat_normalise` brute (~1 233 labels)** : sous-comptage connu de
   l'ère des scans, utilisable uniquement en diagnostic.
4. **Remplacer « le site officiel sous-compte » par la formulation nuancée** :
   « pour plusieurs sessions 2019-2021, le nombre de lignes de décision dans le PDF excède le
   compteur officiel ; une partie est imputable aux dossiers en 2e passage, le reste reste à
   documenter ligne à ligne. »
5. **Documenter explicitement la différence de référentiel** entre `comparaison_json_vs_pdf.md`
   (82/85 = fidélité parseur vs ancien scrapé) et le compteur officiel actuel, pour ne pas laisser
   le lecteur conclure à une contradiction.
