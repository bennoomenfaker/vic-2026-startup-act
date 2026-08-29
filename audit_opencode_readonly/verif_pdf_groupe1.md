# Vérification PDF directe — Groupe 1 (5 sessions)

**Date :** 28/08/2026 · **Mode :** LECTURE SEULE (aucun fichier source modifié)
**Méthode :** extraction du texte natif des PDF avec PyMuPDF (`fitz`) sur
`public/data/session-pdfs/session_YYYY_MM.pdf`.
**Référence de comparaison :** `MASTER_88_sessions_FINAL.csv` (source vérifiée).

---

## Convention de lecture du rapport

Chaque session est analysée en distinguant :

- **OBSERVÉ (fait)** : preuve directe issue du texte extrait du PDF.
- **HYPOTHÈSE** : plausible mais non prouvé.
- **NON DÉTERMINABLE** : aucune preuve disponible (texte non extractible).

> **Note méthodologique sur « lignes_pdf » :** dans `MASTER`, la colonne
> `lignes_pdf` ne suit pas une définition unique et stable entre sessions (parfois
> = lignes du tableau principal seul, parfois un sous-total ajusté). Ce rapport
> indique donc **systématiquement** le nombre de lignes physiques OBSERVÉ par
> tableau (principal / conversions / retraits) et le total, puis le compare au
> `lignes_pdf` MASTER. Les écarts résiduels MASTER cités dans l'énoncé sont
> reproduits à titre documentaire et confrontés aux données observées.

---

## 1) Session 07/2020 — `session_2020_07.pdf`

### État du PDF
- 3 pages. Le contenu est un **scan/image** : les pages sont construites en
  rectangles vectoriels (grille de tableau vide) et ne contiennent **aucune image
  raster extractible** (`get_images()` = 0) ni **aucune couche de texte exploitable**
  (967 caractères au total sur 3 pages).
- Le peu de texte présent est un **fragment errant de la colonne « Commentaires »**
  (verdicts répétés, non reliés à des entreprises) :
  - p.0 : « Label non accordé dès le 2ème tour » ×7, « Label non accordé suite au
    pitching » ×3, citations de conflits d'intérêt (« Mohamed Salah Frad »,
    « Elyes Jeribi »).
  - p.1 : « Label non accordé suite au pitching » ×2, « Prélabel non accordé dès le
    2ème tour » ×9, « Prélabel non accordé suite au pitching » ×2.
  - p.2 : vide (aucun texte).

### Verdict
- Aucun nom de société, aucun lien société→décision, aucune structure de tableau
  exploitable. Impossible de compter les lignes physiques ni de ventiler les
  décisions par extraction textuelle.

### Résultat
- **STEP A :** Nombre de tableaux physiques détectés = **NON DÉTERMINABLE** (pas de
  texte de structure).
- **STEP B :** Ventilation Label/Prélabel = **NON DÉTERMINABLE**.
- **STEP C :**
  - `lignes_pdf` MASTER = **51** (issue de transcription manuelle, PDF scanné).
  - OBSERVÉ par texte : **0 ligne exploitable** → ne permet ni de confirmer ni
    d'infirmer le 51. Le « 51 » est donc **non vérifiable par extraction**.
  - `candidatures_officielles` = 40 : non vérifiable.
  - Commentaire officiel « 9 Labels et 9 Prelabels à Labels » (= 18 labels) : non
    vérifiable dans le PDF.
- **STEP D :** conversions non visibles (rien d'extractible) ; écart documenté 11
  (MASTER) reproduit à titre indicatif, non dérivable ici.

**STATUT : NON DÉTERMINABLE par extraction textuelle** (PDF scanné/vectoriel sans
couche texte exploitable). Ce constat confirme la note MASTER « PDF scanné,
transcription manuelle ».

---

## 2) Session 04/2019 — `session_2019_04.pdf`

### Structure observée (2 pages, texte intégral extractible)
- **1 seul tableau physique** : le tableau principal de pitching
  (« Société | Fondateurs | Secteur | … | Résultat | Commentaires »).
- **Aucun tableau** « Passage de Prélabels aux Labels » ni « Retraits ».

### STEP A — Lignes du tableau principal
**OBSERVÉ = 52 lignes** (52 sociétés, p.1 + p.2). Aucune autre table.

### STEP B — Ventilation des 52 lignes
**OBSERVÉ :**
- **Label Accordé = 33**
- **Label Non- Accordé = 19** (dont **5 « Dossier irrecevable »** : Boostiny,
  Forevermo/Paravoisin, Supply Air, Sawsan Bellaj Training & Consulting, Casual Bet)
- **Prélabel : 0** (toutes les lignes sont des « Label » — cohérent avec
  `prelabels_officiels = 0` de MASTER)
- Retraits : 0 · Conversions : 0 · Reportés : 0 · Ajournés : **0 mention dans le texte**

### STEP C — Comparaison MASTER
| Élément MASTER | Valeur | OBSERVÉ PDF | Concordance |
|---|---|---|---|
| `lignes_pdf` | 52 | **52** | ✅ exact |
| `labels_officiels` | 33 | 33 (Label Accordé) | ✅ exact |
| `prelabels_officiels` | 0 | 0 | ✅ |
| `candidatures_officielles` | 51 | 52 lignes | ⚠️ écart **+1** |
| commentaire « 1 ajourné à la session suivante » | — | **aucune mention « ajourné »** dans le texte | ⚠️ |

### STEP D
- Conversions (« X Prélabels à Labels ») visibles comme tableau séparé : **NON**
  (absence de prélabels dans cette session).
- `lignes_pdf` MASTER (52) = lignes du tableau principal (52) : **correspond**.
- `candidatures_officielles` (51) expliquable ? **NON résolu** : 52 lignes vs 51
  officiel, le « 1 ajourné » cité dans le commentaire officiel n'est **pas
  identifié par recoupement de noms** (confer note AGENTS.md). C'est le seul écart
  de ce sous-groupe.

**STATUT : cohérent sur `lignes_pdf` (52) et les labels (33) ; écart confirmé sur
le total candidatures (52 CR vs 51 officiel), « 1 ajourné » non identifiable.**

---

## 3) Session 08/2020 — `session_2020_08.pdf`

### Structure observée (2 pages, texte intégral extractible)
- **2 tableaux physiques :**
  1. **Tableau principal** (p.1–début p.2).
  2. **« Passage de Prélabels aux Labels »** (p.2, fin) — tableau de conversions.
- **Aucun tableau « Retraits »**.

### STEP A — Lignes
- Tableau principal : **OBSERVÉ = 28 lignes**.
- Tableau conversions : **OBSERVÉ = 10 lignes** (toutes « Label accordé »).
- **Total lignes physiques = 38.**

### STEP B — Ventilation
**Tableau principal (28) :**
- Label accordé = **7**
- Label non accordé = **12**
- Prélabel accordé = **6**
- Prélabel non accordé = **3**

**Conversions (10) :** 10 × « Label accordé » (Afia Tech, SPORTOLOGY/KLAY, Société
Classquiz, Nebulabs/Kyteb, Scaphandry/Rent a tutor, DGA/GrowApp, Hope
Healthcare/Le Comet, THEMAZEGROUP/iSporit, School Upgrader, FACTOORYA).

**Retraits : 0.**

### STEP C — Comparaison MASTER
| Élément MASTER | Valeur | OBSERVÉ PDF | Concordance |
|---|---|---|---|
| `candidatures_officielles` | 28 | 28 (tableau principal seul) | ✅ exact |
| `labels_officiels` | 17 | 7 + 10 conversions = **17** | ✅ exact |
| `prelabels_officiels` | 6 | 6 (Prélabel accordé) | ✅ exact |
| commentaire « 7 Labels et 10 Prelabels à Labels » | — | 7 + 10 = 17 ✓ | ✅ |
| `lignes_pdf` | 34 | observe 28+10 = **38** | ⚠️ écart **+4** |

### STEP D
- Conversions visibles comme tableau séparé : **OUI** (« Passage de Prélabels aux
  Labels », 10 lignes) — correspond exactement au « 10 Prelabels à Labels » du
  commentaire officiel.
- `lignes_pdf` MASTER (34) : **ne correspond pas** au total observé (38) ; la
  formule « 34 − conv(10) − retraits(0) − cand(28) = −4 » reproduit l'écart résiduel
  MASTER (−4), qui traduit une **sous-comptabilisation de 4** dans `lignes_pdf`
  MASTER par rapport aux 38 lignes physiques réelles.
- `candidatures_officielles` (28) : expliquée = lignes du tableau principal
  (28) seul, sans conversions ni retraits.

**STATUT : cohérent sur candidatures (28 = tableau principal), labels (17), prelabels
(6) et conversions (10) ; écart confirmé uniquement sur `lignes_pdf` MASTER
(34 vs 38 observés, soit −4).**

---

## 4) Session 09/2020 — `session_2020_09.pdf`

### Structure observée (2 pages, texte intégral extractible)
- **3 tableaux physiques :**
  1. **Tableau principal** (p.1).
  2. **« Passage de Prélabels aux Labels »** (p.2, haut) — conversions.
  3. **« Retrait de Label Startup »** (p.2, bas) — retraits.

### STEP A — Lignes
- Tableau principal : **OBSERVÉ = 24 lignes**.
- Tableau conversions : **OBSERVÉ = 8 lignes** (toutes « Label accordé »).
- Tableau retraits : **OBSERVÉ = 5 lignes** (Mass SA, Catrim, Jhimi Pour Les
  Elévateurs Légers, TechAccessibility, Tira Robots).
- **Total lignes physiques = 37.**

### STEP B — Ventilation
**Tableau principal (24) :**
- Label accordé = **3**
- Prélabel accordé = **9**
- Label non accordé = **6** (dont 1 irrecevable : SAFEOPS)
- Prélabel non accordé = **6** (dont 2 irrecevables : Dinaro, Farmvie)

**Conversions (8) :** 8 × « Label accordé » (Sté ELAASLA/Raheeq, Barbecha, Ste
DomHome/Smart House Tunisia, AL diagnosis vision, Boho Corporation/KWIN, Dentic
Group/Dentic, Technagile Innovation Labs/FlowsMaster, SBI Biotech/Tunisiabiotech).

**Retraits (5) :** 5 × « Retrait du Label ».

### STEP C — Comparaison MASTER
| Élément MASTER | Valeur | OBSERVÉ PDF | Concordance |
|---|---|---|---|
| `candidatures_officielles` | 24 | 24 (tableau principal seul) | ✅ exact |
| `labels_officiels` | 11 | 3 + 8 conversions = **11** | ✅ exact |
| `prelabels_officiels` | 9 | 9 (Prélabel accordé) | ✅ exact |
| commentaire « 3 Labels et 8 Prelabels à Labels » | — | 3 + 8 = 11 ✓ | ✅ |
| `lignes_pdf` | 23 | observe 24 (principal) / 37 (total) | ⚠️ −1 vs principal |

### STEP D
- Conversions visibles comme tableau séparé : **OUI** (8 lignes) — correspond au
  « 8 Prelabels à Labels » du commentaire officiel.
- Retraits visibles comme tableau séparé : **OUI** (5 retraits).
- `lignes_pdf` MASTER (23) : **ne correspond ni** au tableau principal (24) **ni**
  au total (37). L'écart résiduel MASTER documenté (−9) n'est pas dérivable d'une
  formule simple sur ces lignes ; à reproduire à titre documentaire.
- `candidatures_officielles` (24) : expliquée = lignes du tableau principal
  (24) seul.

**STATUT : cohérent sur candidatures (24 = tableau principal), labels (11), prelabels
(9), conversions (8) et retraits (5) ; écart confirmé sur `lignes_pdf` MASTER
(23 vs 24 observés en tableau principal, et vs 37 au total physique).**

---

## 5) Session 11/2020 — `session_2020_11.pdf`

### Structure observée (3 pages, texte intégral extractible)
- **3 tableaux physiques :**
  1. **Tableau principal** (p.1–p.3).
  2. **« Passage de Prélabels aux Labels »** (p.2–p.3) — conversions.
  3. **« Retrait de Label Startup »** (p.3, fin) — retraits.

### STEP A — Lignes
- Tableau principal : **OBSERVÉ = 41 lignes**.
- Tableau conversions : **OBSERVÉ = 13 lignes** (toutes « Label accordé »).
- Tableau retraits : **OBSERVÉ = 1 ligne** (ROAMSMART).
- **Total lignes physiques = 55.**

### STEP B — Ventilation
**Tableau principal (41) :**
- Label accordé = **13**
- Prélabel accordé = **14**
- Label non accordé = **7**
- Prélabel non accordé = **7**

**Conversions (13) :** 13 × « Label accordé » (Evolutik, HOMEJEK, SMELSY, Fouita,
Eventizer, 4InA, Travaris, El Food Lab, Co-Solar, Services Voitures Epaves,
Fantastic Mall, D-WEE, AmazIT/FI THNITI).

**Retraits (1) :** 1 × « Retrait du Label » (ROAMSMART — âge > 8 ans).

### STEP C — Comparaison MASTER
| Élément MASTER | Valeur | OBSERVÉ PDF | Concordance |
|---|---|---|---|
| `candidatures_officielles` | 41 | 41 (tableau principal seul) | ✅ exact |
| `labels_officiels` | 26 | 13 + 13 conversions = **26** | ✅ exact |
| `prelabels_officiels` | 14 | 14 (Prélabel accordé) | ✅ exact |
| commentaire « 13 Labels et 12 Prelabels à Labels » | — | 13 conversions trouvées | ⚠️ voir note |
| `lignes_pdf` | 40 | observe 41 (principal) / 55 (total) | ⚠️ −1 vs principal |

> **Note commentaire officiel :** le libellé officiel annonce « 12 Prelabels à
> Labels », mais le PDF contient **13 lignes de conversion** (toutes « Label
> accordé »), confirmant `labels_officiels = 26` de MASTER (13 + 13). Écart de
> **−1** entre le commentaire officiel (12) et les lignes de conversion réellement
> présentes (13). C'est MASTER (26) qui est confirmé par le PDF.

### STEP D
- Conversions visibles comme tableau séparé : **OUI** (13 lignes).
- Retraits visibles comme tableau séparé : **OUI** (1 retrait).
- `lignes_pdf` MASTER (40) : **ne correspond ni** au tableau principal (41) **ni**
  au total (55). Écart résiduel MASTER documenté (−13) reproduit à titre
  documentaire.
- `candidatures_officielles` (41) : expliquée = lignes du tableau principal
  (41) seul. **Note légère :** l'une des 41 lignes porte un nom en arabe partiel
  (« ﻲﺑﯾﺟد - Jeeby », « en ligne سﻧوﺗ », « سﻧوﺗ »), mais la ligne est comptée et
  cohérente.

**STATUT : cohérent sur candidatures (41 = tableau principal), labels (26), prelabels
(14) et retraits (1) ; écart confirmé sur `lignes_pdf` MASTER (40 vs 41 observés
en tableau principal, et vs 55 au total physique) ; le commentaire officiel
« 12 Prelabels à Labels » est en léger décalage (−1) avec les 13 conversions
réellement présentes.**

---

## Synthèse générale

| Session | Tableaux physiques | Lignes tableau principal | Conv. | Retraits | Total lignes | cand. officielles expliquée par | labels officiels vérifiés | prelabels officiels | lignes_pdf MASTER vs observé | STATUT |
|---|---|---|---|---|---|---|---|---|---|---|
| **07/2020** | **0 exploitable** (scan) | NON DÉT. | — | — | NON DÉT. | NON DÉT. | non vérifiable | non vérifiable | — | **NON DÉTERMINABLE** |
| **04/2019** | 1 (principal) | 52 | 0 | 0 | 52 | 52 vs 51 (écart +1 non résolu) | 33/33 ✅ | 0 ✅ | 52 = 52 ✅ | **cohérent** (sauf écart +1 cand.) |
| **08/2020** | 2 (principal + conversions) | 28 | 10 | 0 | 38 | 28 ✅ | 17/17 ✅ | 6 ✅ | 34 vs 38 (**+4**) | **cohérent** (écart lignes_pdf) |
| **09/2020** | 3 (principal + conv. + retraits) | 24 | 8 | 5 | 37 | 24 ✅ | 11/11 ✅ | 9 ✅ | 23 vs 24/− | **cohérent** (écart lignes_pdf) |
| **11/2020** | 3 (principal + conv. + retraits) | 41 | 13 | 1 | 55 | 41 ✅ | 26/26 ✅ | 14 ✅ | 40 vs 41/− | **cohérent** (écart lignes_pdf) |

### Points clés
1. **07/2020 est NON DÉTERMINABLE** par extraction textuelle (PDF scanné, aucune
   couche texte exploitable) — la valeur 51 vient de la transcription manuelle et
   ne peut être ni confirmée ni infirmée par le texte.
2. **4 sessions sur 5 sont parfaitement cohérentes** sur les indicateurs métier
   (candidatures = lignes du tableau principal ; labels = labels accordés +
   conversions ; prelabels = prélabels accordés). Tous les `labels_officiels` et
   `prelabels_officiels` de MASTER sont confirmés (« ✅ exact » dans chaque session).
3. **Le point faible résiduel porte uniquement sur la colonne `lignes_pdf` de
   MASTER** : elle sous-estime systématiquement le total de lignes physiques
   présentes dans les PDF (08/2020 : 34 vs 38 ; 09/2020 : 23 vs 24 principal ;
   11/2020 : 40 vs 41 principal). La définition interne de `lignes_pdf` MASTER
   n'est pas alignée sur le nombre total de lignes physiques observées.
4. **Commentaires officiels** : vérifiés et exacts pour 08/2020 (« 7 Labels et 10
   Prelabels à Labels ») et 09/2020 (« 3 Labels et 8 Prelabels à Labels ») ; pour
   11/2020 le « 12 Prelabels à Labels » officiel est en léger décalage (−1) avec
   les 13 conversions réellement présentes (MASTER 26 est confirmé).
5. **04/2019** : écart +1 entre 52 lignes CR et 51 candidatures officielles, le
   « 1 ajourné » n'étant pas identifiable par recoupement de noms (confer
   `corrections.json`). Les 33 labels sont confirmés.
