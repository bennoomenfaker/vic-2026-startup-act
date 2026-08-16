# Notice — Écart documenté Session 04/2019 (« 1 ajourné »)

**Date** : 16/08/2026
**Objet** : écart entre les 51 candidatures officielles de la session 04/2019 et les 52 décisions listées dans le Compte-Rendu (CR).

---

## 1. Les deux sources

| Source | Candidatures | Labels accordés | Commentaire |
|---|---|---|---|
| `sessions.json` (tableau `/sessions` startup.gov.tn) | **51** | 33 | « 1 ajourné à la session suivante » |
| CR officiel — `public/data/manual_sessions/2019_04.json` (vérité de terrain) | **52** | 33 | 52 décisions : 33 accordés, 14 refus, 5 irrecevables |

## 2. Vérifications effectuées

1. **PDF brut de la session** (`/tmp/opencode/pdf_text_recheck_all/session_2019_04.txt`) : les 52 lignes existent bien, aucune erreur de saisie manuelle. Aucune mention « ajourné » dans le texte PDF.
2. **Chiffre officiel des labels** : 33 labels accordés = exactement le chiffre officiel. Il n'y a aucune divergence sur les labels.
3. **Recoupement avec la session 05/2019** : le seul nom commun trouvé (Sawssen Bellaj) est un **faux positif** — Issam Bellaj (mai) et Sawssen Bellaj (avril) sont des personnes différentes. La ligne ajournée n'est pas identifiable par les noms.

## 3. Hypothèse retenue

L'une des 52 lignes du CR 04/2019 correspond au dossier **ajourné**, examiné en mai 2019. Cela explique le commentaire de la session 05/2019 : « **29 candidats pour mai + 1 candidat de la session d'avril** » = 30 candidatures.

## 4. Décision

- On **conserve les 52 lignes** du CR (vérité de terrain).
- L'écart « 52 CR vs 51 officiel » est documenté :
  - dans `public/data/corrections.json` (entrée 04/2019, **labels inchangés** à 33) ;
  - dans `meta.ecart_a_documenter` de `public/data/manual_sessions/2019_04.json`.
- **Avertissement** : ne pas recalculer le taux officiel 04/2019 (33/51 = 64,7 %) sur une base de 52 candidatures **tant que la ligne ajournée n'est pas identifiée**.

## 5. Validation croisée (16/08/2026)

6/7 sessions relues manuellement sont exactement cohérentes avec `sessions.json` et le tableau corrigé. Le seul écart est cette candidature 04/2019. Les 33 labels 04/2019 sont confirmés.
