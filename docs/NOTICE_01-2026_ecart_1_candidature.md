# Notice — Écart documenté Session 01/2026 (31 officiel vs 30 CR)

**Date** : 16/08/2026
**Objet** : écart entre les 31 candidatures officielles de la session 01/2026 (Session 82) et les 30 dossiers listés dans le Compte-Rendu (CR).

---

## 1. Les deux sources

| Source | Candidatures | Labels accordés | Prélabels accordés | Commentaire |
|---|---|---|---|---|
| `sessions.json` (tableau `/sessions` startup.gov.tn) | **31** | 10 (3 labels + 7 conversions) | 7 | « 03 Labels et 06 Prélabels à Labels » |
| CR officiel — `public/data/manual_sessions/2026_01.json` (vérité de terrain) | **30** | 3 labels accordés (IMMUNO KAAR, Arcube, GoToGreen) + 7 conversions | 7 | 30 dossiers : 24 page 1 + 6 page 2 |

## 2. Vérifications effectuées

1. **PDF brut de la session** (`/tmp/opencode/pdf_text_recheck_all/session_2026_01.txt`) : les 30 lignes existent bien (24 sur la page 1, 6 sur la page 2), aucune erreur de saisie manuelle. Aucune mention « ajourné » dans le texte PDF.
2. **Chiffre officiel des labels** : 10 labels accordés = 3 labels directs + 7 conversions — confirmé par le CR. 7 prélabels accordés — confirmés par le CR.
3. **Commentaire officiel « 06 Prélabels à Labels » erroné** : le CR liste 7 conversions réelles (Rhizome, Compta Smart Solutions, DIA Industries, Dash Master, ERPY, Park & Charge, Ligalo), mais le **total** labels officiel (10 = 3 + 7) reste cohérent.
4. **Le PDF seul ne permet pas d'identifier la 31e candidature manquante** : aucune ligne « ajourné », aucun recoupement de noms disponible entre 01/2026 et 02/2026 permettant d'isoler le dossier manquant.

## 3. Décision

- On **conserve les 30 lignes** du CR (vérité de terrain).
- L'écart « 30 CR vs 31 officiel » est documenté :
  - dans `public/data/corrections.json` (entrée 01/2026, **labels corrigés 9 → 10**) ;
  - dans `meta.ecart_a_documenter` de `public/data/manual_sessions/2026_01.json`.
- **Avertissement** : ne pas recalculer le taux officiel 01/2026 (10/31 = 32,3 %) sur une base de 30 candidatures **tant que la ligne manquante n'est pas identifiée**.

## 4. Conflits d'intérêt déclarés

- **Hassen Aarfaoui** : Arcube, GoToGreen, SAHTEE, Qubit Labs Tunis, Eyproc, 9atratech.
- **Mehdi Nakouri** : HopeVisionAI.

## 5. Cohérence des sessions voisines

- **06/2025** (Session 75) : 36 candidatures / 12 labels / 8 prélabels — **cohérence totale** avec le PDF, aucune correction requise (fichier `manual_sessions/2025_06.json` créé à titre de vérification).
