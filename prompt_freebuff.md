# Prompt « freebuff » — Re-vérification indépendante des données Startup Act

Tu es **freebuff**, un auditeur de données indépendant. Voici la mission complète,
le contexte, les fichiers à analyser, et exactement ce que tu dois faire et retourner.

---

## 1. Situation (contexte)

Le site officiel **startup.gov.tn** publie, sur la page `/fr/startup_act/results`
(composant `/sessions` du dashboard), un tableau des sessions mensuelles de labellisation
Startup Act avec les colonnes : **Candidatures, Labels, Pré-Labels, Taux d'acceptation,
Taux d'échec, Commentaires**.

**Problème** : ce tableau affiché par startup.gov.tn est **FAUX**. Une comparaison avec les
PDF officiels des comptes rendus de sessions révèle des valeurs erronées sur 20 sessions
sur 85 (labels et/ou prélabels mal comptés par le site). En conséquence, les totaux et les
taux du tableau `/sessions` sont eux aussi faux.

**Ce qui a été fait** :
1. Les PDF officiels de **toutes les sessions** ont été téléchargés dans le dossier
   `public/data/session-pdfs/` (85 fichiers `session_YYYY_MM.pdf`).
2. Un parseur **v7** (`parse_pdfs_v7.py`) a extrait de chaque PDF le décompte réel :
   `new_labels` (nouveaux labels accordés), `new_prelabels` (nouveaux prélabels accordés),
   `conversions` (prélabels → labels), `retraits` (labels retirés).
3. Le tableau `/sessions` a été **corrigé** en conséquence.
4. Un travail d'analyse a produit plusieurs fichiers (détaillés en §3).

**Modèle de comptage appliqué** (celui du site, vérifié sur les commentaires officiels) :
- `labels` = nouveaux labels accordés + conversions prélabel→label
- `preLabels` = nouveaux prélabels accordés (les conversions ne comptent PAS ici)
- `retraits` = soustraction, déjà reflétée si la ligne du PDF dit « Retrait de Label »

---

## 2. Ta mission (freebuff)

1. **Re-extraire toi-même les données depuis les PDF** — indépendamment du parseur v7.
   Ouvre **chacun des 85 PDF** de `public/data/session-pdfs/` et compte toi-même, à la lecture :
   - nouveaux labels accordés,
   - nouveaux prélabels accordés,
   - conversions « Prelabels à Labels »,
   - retraits de labels.
   Ne te fie PAS à `pdf_parsed_v7.json` : refais le comptage. Ne te fie PAS au scrapé de
   startup.gov.tn : c'est justement lui qui est faux.
2. **Vérifier que tes extractions égalent mes extractions** : compare tes comptages à
   `public/data/pdf_parsed_v7.json` (le résultat du parseur v7).
3. **Vérifier que tes corrections égalent mes corrections** : calcule `labels` et `preLabels`
   selon le modèle de comptage ci-dessus, puis compare avec les valeurs corrigées dans
   `public/data/dashboard_data.json` (et `public/data/sessions.json`, identique).
4. **Vérifier les taux** :
   - `tauxAcceptationExact` == labels ÷ candidatures × 100 (valeur exacte) ;
   - `tauxAcceptation` == arrondi à 1 décimale de la valeur exacte ;
   - `tauxEchec` == arrondi à 1 décimale de (100 − valeur exacte) ; somme = 100.0 (±0.05).
5. **Me retourner le résultat détaillé** (format en §5) pour que je l'analyse.

---

## 3. Fichiers à analyser (ce que tu dois ouvrir et vérifier)

### 3.1 Source de vérité — les PDF officiels
- `public/data/session-pdfs/session_YYYY_MM.pdf` — **85 fichiers**, source de vérité.
  C'est sur eux que tu dois refaire tes comptages.

### 3.2 Fichiers que j'ai analysés / créés (contexte)
| Fichier | Rôle |
|---|---|
| `public/data/session-pdfs/session_YYYY_MM.pdf` | PDF officiels des sessions (source brute) |
| `public/data/pdf_parsed_v7.json` | Résultat du parseur v7 (85 sessions : `new_labels`, `new_prelabels`, `conversions`, `retraits`, `total_labels`, `total_prelabels`) — **à re-vérifier par toi** |
| `parse_pdfs_v7.py` | Le parseur automatique (référence de la méthode, pas une source de vérité) |
| `public/data/dashboard_data.json` | Données corrigées du dashboard : `meta` (sources, date de mise à jour `2026-07-31T12:00:00Z`), `sessions` (85), `yearly` (totaux par année) — **à vérifier** |
| `public/data/sessions.json` | Même tableau `/sessions`, liste seule (identique à `dashboard_data.json.sessions`) |
| `corrections.md` | Détail des 20 corrections + tableaux avant/après (scrapé vs corrigé) |
| `tableau_sessions.md` | Le tableau `/sessions` corrigé, complet |
| `prompt_freebuff.md` | Ce prompt |
| `comparaison_sessions.html` | Comparaison visuelle scrapé (faux) vs corrigé (vrai) |

### 3.3 Colonnes du JSON à vérifier (objet `sessions` de `dashboard_data.json`)
- `session` (ex. `02/2026`), `month`, `year`
- `candidatures`
- `labels` — **c'est le tableau `/sessions` du site, corrigé** → doit valoir `new_labels + conversions` du PDF
- `preLabels` — **corrigé** → doit valoir `new_prelabels` du PDF
- `commentaires` — commentaire officiel du PDF (ex. « 9 Labels et 9 Prelabels à Labels »)
- `tauxAcceptation` (string, 1 décimale), `tauxAcceptationExact` (float), `tauxEchec` (string), `tauxEchecExact` (float)

---

## 4. Les 20 corrections à vérifier en priorité

Ces sessions ont été corrigées par rapport au scrapé affiché par startup.gov.tn :

| Session | Labels corrigés | Pré-Labels corrigés | Valeur fausse scrapée (L/P) |
|---------|---------------|-------------------|---------------------------|
| 02/2026 | 20 | 3 | 21/3 |
| 01/2026 | 10 | 7 | 9/7 |
| 12/2025 | 16 | 6 | 15/6 |
| 05/2025 | 13 | 13 | 13/10 |
| 01/2025 | 13 | 2 | 18/2 |
| 07/2024 | 6 | 7 | 5/7 |
| 03/2024 | 6 | 7 | 7/7 |
| 12/2023 | 12 | 5 | 14/5 |
| 11/2023 | 12 | 7 | 14/4 |
| 10/2023 | 6 | 4 | 6/5 |
| 08/2023 | 11 | 5 | 11/6 |
| 04/2023 | 13 | 5 | 14/5 |
| 03/2023 | 14 | 6 | 13/6 |
| 12/2022 | 16 | 5 | 17/5 |
| 09/2021 | 15 | 6 | 13/6 |
| 02/2021 | 25 | 10 | 25/7 |
| 10/2019 | 23 | 5 | 23/4 |
| 08/2019 | 20 | 5 | 24/7 |
| 07/2019 | 14 | 8 | 15/8 |
| 06/2019 | 14 | 8 | 15/8 |

**Note** : les autres 65 sessions devraient être conformes (inchangées par rapport au scrapé,
elles aussi vérifiées contre les PDF) — vérifie-les quand même.

> **Correction apportée à ce prompt (v2)** : les valeurs ci-dessus sont maintenant exactes,
> générées directement depuis `dashboard_data.json`. Une première version du prompt contenait
> 10 valeurs de pré-labels erronées (10/2019, 09/2021, 12/2022, 03/2023, 04/2023, 08/2023,
> 12/2023, 03/2024, 07/2024, 01/2025) — c'était une erreur du prompt, PAS des données.

---

## 5. Ce que tu dois me retourner (le résultat que j'analyserai)

Pour **chaque session**, une ligne au format :

`SESSION | PDF: labels=X prelabels=Y conversions=Z retraits=W | MES_VALEURS: labels=A prelabels=B | CONFORME ou DIVERGENCE(écart) | taux exact E% / arrondi R% (ok|ko)`

Puis un **bilan final** :
- nombre de sessions où tes extractions == mes extractions (`pdf_parsed_v7.json`) ;
- nombre de sessions où tes corrections == mes corrections (`dashboard_data.json`) ;
- nombre de divergences, avec pour chacune : champ concerné, valeur attendue vs trouvée,
  et citation exacte du PDF (noms des startups ou ligne du tableau) ;
- un verdict global : « TES CORRECTIONS == MES CORRECTIONS » ou liste des écarts.

### Cas particuliers
- **3 PDF illisibles — mission OCR obligatoire** : `07/2020`, `12/2020`, `01/2021` sont des
  images (pas de couche texte exploitable). C'est la **seule donnée jamais vérifiée**
  (valeurs restaurées depuis le scrapé, non lues dans le PDF) : `07/2020 = 18/7`,
  `12/2020 = 21/8`, `01/2021 = 24/7`, cohérentes avec les commentaires officiels.
  **Lance un OCR** (tesseract/paddle/vision) sur ces 3 PDF et confirme ou infirme les valeurs.
  Retourne le texte OCR des colonnes Résultat si possible.
- **Session `10/25`** : la session d'octobre 2025 est stockée dans le dashboard sous la clé
  `10/25` au lieu de `10/2025` (incohérence de format avec les 84 autres, signalée par ton
  audit). Données sous-jacentes correctes (`2025/10` dans v7 = 17/12) — signale si l'OCR
  d'autres sources confirme 17 labels / 12 prélabels.
- **Anomalie corrigée 02/2020** : le scrapé affichait échec 31.3 (somme 100.1) ; corrigé en
  68.75 → 68.8% / 31.25 → 31.2% (somme 100.0). Vérifie aussi ce cas.

## 6. Règles absolues

- Le **PDF officiel fait foi**, jamais le tableau scrapé de startup.gov.tn.
- **Refais le comptage toi-même** ; ne réutilise pas les valeurs de `pdf_parsed_v7.json`
  comme point de départ, elles sont précisément ce que tu dois vérifier.
- Si un PDF est illisible sans OCR, **utilise l'OCR** (obligatoire pour 07/2020, 12/2020,
  01/2021) ; ne devine jamais une valeur.
- Produis un résultat exhaustif et reproductible (session par session), pas un simple résumé.
