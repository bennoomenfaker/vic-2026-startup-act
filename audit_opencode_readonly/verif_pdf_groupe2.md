# Vérification directe des PDFs — Groupe 2 (5 sessions)

**Mode :** lecture seule des PDFs via PyMuPDF (`fitz.open` / `page.get_text()`).
**Référence :** MASTER_88_sessions_FINAL.csv (valeurs fournies dans la mission).
**Convention du rapport :** chaque constat est classé **OBSERVÉ (fait PDF direct)** | **HYPOTHÈSE** | **NON DÉTERMINABLE** | **ÉCART CONFIRMÉ**.
**Avertissement extraction :** pour 02/2023 le texte natif était intercalé (colonnes lues dans le désordre) ; j'ai utilisé l'extraction positionnelle `get_text('dict')` triée par coordonnées pour reconstituer les lignes. Comptages faits ligne par ligne (société).

---

## Synthèse des comptages observés (PDF)

| Session | Table principale (candidatures) | L_acc | P_acc | L_non | P_non | reporté | Conversions | Retrait | Total lignes doc |
|---|---|---|---|---|---|---|---|---|---|
| 04/2021 | 80 | 18 | 24 | 7 (dont 1 irrecevable) | 31 | 0 | 4 | 1 | 85 |
| 09/2021 | 25 | 2 | 6 | 3 | 13 | 1 (SHYK) | 13 | 0 | 38 |
| 10/2021 | 41 | 15 | 7 | 6 (dont 1 irrecevable) | 13 | 0 | 8 | 0 | 49 |
| 02/2023 | 33 | 7 | 11 | 7 | 8 | 0 | 11 | 1 | 45 |
| 04/2023 | 40 | 9 | 5 | 11 (dont 1 irrecevable) | 15 | 0 | 4 | 0 | 44 |

L_acc = Label accordé ; P_acc = Prélabel accordé ; L_non = Label non accordé ; P_non = Prélabel non accordé.

---

## 1) Session 04/2021 — `session_2021_04.pdf` (4 pages)

### STEP A / B — Tables physiques et décisions
**3 tables détectées :**
1. **Table de pitching principale** (pages 1–3) : **80 lignes**.
   - Label accordé : **18**
   - Prélabel accordé : **24**
   - Label non accordé : **7** (6 + 1 irrecevable : *Shwoppy*, « dossier irrecevable pour présentation d'un document officiel altéré », Recevabilité = Non)
   - Prélabel non accordé : **31**
2. **Table « Passage de Prélabels aux Labels »** (page 3 bas / page 4) : **4 conversions** (toutes « Label accordé »).
   - BOS BLASTER OZONE SOLUTIONS, Keto Life Style, Smart Brain Corporation, ECGLab.
3. **Table « Retrait de Label Startup »** (page 4) : **1 retrait** — *Educanet Tunisia* (« la société a dépassé l'âge maximum de 8 ans »).

### STEP C / D — Comparaison référentiel
| Réf. MASTER | Valeur | PDF observé | Verdict |
|---|---|---|---|
| candidatures_officielles = 80 | 80 | Table principale = **80 lignes** | **COHÉRENT** (match exact) |
| labels_officiels = 22 | 22 | 18 directs + 4 conversions = **22** | **COHÉRENT** |
| prelabels_officiels = 24 | 24 | Table principale P_acc = **24** | **COHÉRENT** |
| lignes_pdf = 81 | 81 | Total doc = **85** (80+4+1) | **ÉCART CONFIRMÉ** : lignes_pdf MASTER sous-estime de 4 (= le 4 conversions exclues) |
| Commentaire « 18 Labels et 4 Prelabels à Labels » | — | 18 directs + 4 conversions = **visible en table dédiée** | **COHÉRENT** : le commentaire officiel correspond exactement aux faits |

**candidatures_officielles expliquées :** OUI — 80 = la table de pitching principale.
**Conversions visibles en table séparée :** OUI (4 lignes nommées).
**Statut : COHÉRENT** (tous les agrégats officiels s'expliquent depuis le PDF), à l'exception du seul `lignes_pdf=81` (partition différente : principal+retrait, conversions exclues) — écart résiduel documenté **-4** correspondant aux 4 conversions non comptées.

---

## 2) Session 09/2021 — `session_2021_09.pdf` (2 pages)

### STEP A / B — Tables physiques et décisions
**2 tables détectées :**
1. **Table de pitching principale** (pages 1–2) : **25 lignes**.
   - Label accordé : **2** (TADREEX, Urban Green)
   - Prélabel accordé : **6** (Unify, Smartfleet, CUIDA, CAIRUS DIGITAL BUSINESS CENTER, GARK, Pivlo)
   - Label non accordé : **3** (D-SIGNALITIQUE, DIGITAL DRINA, Jibheli)
   - Prélabel non accordé : **13** (Meducol, Delivery, Promo alert, Mosta9bli, NETOX, Baazar, STAGGY, YARAKA PROTEIN, Med Marine Eng., La Beylicale, SOSADRESSE.COM, iziclaim, Kiné Plus)
   - **reporté : 1 — SHYK** (OBSERVÉ, ligne présente : « Candidature reportée — La candidature a été reportée à la session de Septembre »). **→ SHYK confirmé**.
2. **Table « Passage de Prélabels aux Labels »** (page 2) : **13 conversions**, toutes « Label accordé ».
   Liste nommée (vérifiée une à une, 13/13 présents dans le PDF = liste MASTER) :
   Provectus Technology, DIGITIN, STE PERSAVIA (NextAV), EdTrust (School Pack), REDUP (KICK LIGHT), STE Vizmerald, Cooptatio, INVESTHUNE PLUS, Analytix YS, FIVE DELIVERY, WELINCO, RIBLUM, DIMAZINA. **→ 13 conversions CONFIRMÉES.**

Aucune table de retrait.

### STEP C / D — Comparaison référentiel
| Réf. MASTER | Valeur | PDF observé | Verdict |
|---|---|---|---|
| lignes_pdf = 38 | 38 | 25 (principal) + 13 (conversions) = **38** | **COHÉRENT** (match exact) |
| Table principale = 25 lignes (dont SHYK reporté) | 25 | **25 lignes** confirmé | **COHÉRENT** |
| Table conversions = 13 lignes nommées | 13 | **13 lignes nommées** confirmées | **COHÉRENT** |
| candidatures_officielles = 15 | 15 | Table principale = **25 lignes** | **ÉCART CONFIRMÉ / anomalie** : 15 ≠ 25. Aucune lecture raisonnable ne redonne 15 depuis la table principale (il faudrait exclure les refus/reporté, soit étroitement « 2 L_acc + 6 P_acc + … »). |
| labels_officiels = 13 | 13 | conversions = 13 (mais il y a aussi 2 Labels directs) | **ÉCART partiel** : 13 = uniquement les conversions ; les 2 Labels directs de la table principale ne sont pas comptés. Total Labels réellement octroyés = 15. |
| prelabels_officiels = 6 | 6 | P_acc table principale = **6** | **COHÉRENT** |
| Commentaire « 2 Labels et 13 Prelabels à Labels » | — | 2 directs + 13 conversions = 15 | Lecture : commentaire = 2 directs + 13 conversions (cohérent en soi avec la table), mais il contredit `labels_officiels=13` et `candidatures_officielles=15`. |

**candidatures_officielles expliquées ?** NON DÉTERMINABLE / ÉCART CONFIRMÉ. La table principale contient 25 candidatures (fait PDF observable indiscutable). Le chiffre officiel 15 ne correspond à aucun sous-ensemble naturel de ces 25 lignes ; l'hypothèse MASTER « 2 Labels directs + 13 conversions = 15 » est plausible comme **explication du chiffre 15** (HYPOTHÈSE), mais ne représente pas un nombre de candidatures de la table principale. Ceci conforte la « suspected anomaly in the official /results page ».
**Conversions visibles en table séparée :** OUI (13 lignes nommées).
**Statut : ÉCART CONFIRMÉ** (candidatures officielles 15 vs 25 lignes PDF), avec **faits PDF observés** : SHYK reporté ✓, 13 conversions nommées ✓, 38 lignes doc ✓.

---

## 3) Session 10/2021 — `session_2021_10.pdf` (13 pages dont 11 vides)

**Observation structurelle :** le PDF fait 13 pages mais seules les **pages 1–2 contiennent du texte** ; les pages 3 à 13 sont **entièrement vides** (0 caractère, confirmé par `get_text`). Ceci n'affecte pas les contenus de tableaux.

### STEP A / B — Tables physiques et décisions
**2 tables détectées :**
1. **Table de pitching principale** (pages 1–2) : **41 lignes**.
   - Label accordé : **15** (Tajrabti, BaBa Ali, Pwn & Patch, Byessa.com, Ground Transportation, Limonade Technologies, Domicilier.tn, Tagamuta Valley, Makerfy, Pure Beauty Labs, Ijeni, JURIDOC, Faza.tn, bmoov, Chill&Lit)
   - Prélabel accordé : **7** (Storzy, BIESSA AUTO, Bartita, Quiz Mentor, WaveOn, Avoconsulte, SHYK)
   - Label non accordé : **6** (VOLUS, aivataria, Digipages, INNOV'ALGUE, chendir, Log'In — ce dernier irrecevable, Recevabilité = Non)
   - Prélabel non accordé : **13** (Litteuls, Tawelti, SNO, CHLOROFIN, Guya Gang, i-mouzika, TIKA CLUB, Hemileco-Plast, Organic City, The Hub Coworking, D-carte, Wassali, Artalk)
2. **Table « Passage de Prélabels aux Labels »** (page 2) : **8 conversions** :
   PROTABAR COM, ROBODOT, Décotis, Les Ateliers de Yallaa, Z-Partners (capxvalue), Click and Win (isondF), WASSALNI EXPRESS (TAWSILA), DIGIZONE (MCOM).
   **→ 8 conversions, PAS 13.**

Aucune table de retrait.

### STEP C / D — Comparaison référentiel
| Réf. MASTER | Valeur | PDF observé | Verdict |
|---|---|---|---|
| candidatures_officielles = 41 | 41 | Table principale = **41 lignes** | **COHÉRENT** (match exact) |
| prelabels_officiels = 7 | 7 | P_acc table principale = **7** | **COHÉRENT** |
| labels_officiels = 23 | 23 | 15 directs + 8 conversions = **23** | **COHÉRENT** |
| lignes_pdf = 49 | 49 | 41 + 8 = **49 lignes doc** | **COHÉRENT** (match exact) |
| Commentaire « 2 Labels et 13 Prelabels à Labels » | — | 15 directs + **8 conversions** (table séparée = 8, pas 13) | **ÉCART CONFIRMÉ / commentaire erroné** : la table de conversions du PDF contient **8** entrées nommées, pas 13 ; et le nombre de Labels directs est **15**, pas 2. Le commentaire officiel reproduit en réalité celui de 09/2021 (copier-coller apparent). |

**candidatures_officielles expliquées ?** OUI — 41 = table principale.
**Conversions visibles en table séparée ?** OUI mais **4 conversions déclarées ≠ 8 observées** → désaccord avec le commentaire officiel.
**Statut : ÉCART CONFIRMÉ** sur le commentaire officiel (compte de conversions et de labels directs erroné) ; les totaux `labels_officiels=23` et `lignes_pdf=49` se recalculent correctement par ailleurs.

---

## 4) Session 02/2023 — `session_2023_02.pdf` (3 pages)

**Note extraction :** texte natif intercalé ; reconstruit par coordonnées. « Elevage des abeilles pour la collecte » est le **secteur** de la société BEE SPRING (pas une ligne supplémentaire) — NON DÉTERMINABLE n'est plus nécessaire, OBSERVÉ après reconstitution.

### STEP A / B — Tables physiques et décisions
**3 tables détectées :**
1. **Table de pitching principale** (pages 1–2) : **33 lignes**.
   - Label accordé : **7** (Linkivia, Replic-A, Tunisia Baits, Tunisian Campers, Tsiwrat Stock, Advantry X, KOM YA)
   - Prélabel accordé : **11** (My Brain, TOF, cercina.ai, Grün Skincare, Xpro, Gifty.tn, A.M.I.S., Ziwziw Family Friend, COADIS, PARKEY, Thiqab)
   - Label non accordé : **7** (Certif.tn, ITEM TUNISIA, DigiQuorum, Addval Solutions, Ukka, CG-Box, Afar tunisie)
   - Prélabel non accordé : **8** (Artifis, Moneymakr, NER, NEWAY Solutions, NEVER LOST, booky, Tunisie Colis, EyTecFarm)
2. **Table « Passage de Prélabels aux Labels »** (pages 2–3) : **11 conversions** :
   Voltat Technologies, CAMINOVA, SOCIETE SAGUEDNI, BLUEPSOL, SOCIETE INNOVEGA, MRC SURVEY, Workly Hub, BEE SPRING, Kicksoft Studio, BOKYVACATIONS, PAPIPETS.
3. **Table « Retrait de Label Startup »** (page 3) : **1 retrait** — *Avempace SARL* (« dépassé l'âge maximum de 8 ans »).

### STEP C / D — Comparaison référentiel
| Réf. MASTER | Valeur | PDF observé | Verdict |
|---|---|---|---|
| candidatures_officielles = 33 | 33 | Table principale = **33 lignes** | **COHÉRENT** |
| labels_officiels = 18 | 18 | 7 directs + 11 conversions = **18** | **COHÉRENT** |
| prelabels_officiels = 11 | 11 | P_acc table principale = **11** | **COHÉRENT** |
| Commentaire « 7 Labels et 11 Prélabels à Labels » | — | 7 directs + 11 conversions = **table séparée de 11** | **COHÉRENT** (le commentaire correspond exactement aux faits) |
| lignes_pdf = 42 | 42 | Total doc = **45** (33+11+1) | **ÉCART CONFIRMÉ** : lignes_pdf MASTER sous-estime de 3 |

**candidatures_officielles expliquées ?** OUI — 33 = table principale.
**Conversions visibles en table séparée ?** OUI (11 lignes nommées, cohérent avec « 11 Prélabels à Labels »).
**Statut : COHÉRENT** pour tous les agrégats officiels ; seul `lignes_pdf=42` diffère du total doc 45 (écart **-3**).

---

## 5) Session 04/2023 — `session_2023_04.pdf` (2 pages)

### STEP A / B — Tables physiques et décisions
**2 tables détectées :**
1. **Table de pitching principale** (pages 1–2) : **40 lignes**.
   - Label accordé : **9** (Bi'nergy, ONECLOUD, ECOFEED Tunisie, Servini, Pas Comme Eux, H eco ferme, Xgenbox, The Package Center, Bytale Games)
   - Prélabel accordé : **5** (Alifa, cell pulse, Conception/formulation pharmaceutique, Randev, Beitary)
   - Label non accordé : **11** (Oriwood, Teachica, NORMA TUNISIE, SURVIVE RESILIENCE, droplocal.ai, souk elfalleh, Twansa, Karhabti.app, Kosmos technologies, IrWise, verified authentic — ce dernier irrecevable dès le 1er tour, Recevabilité = Non)
   - Prélabel non accordé : **15** (GET BIG FAST, WEeFARM, ShooFu, halli.tn, Noah, BME-Power, ECORISE, trymyculture, BiBin, Metamax, HealthyGO, goodbye, AI WITH YOU, Au delà du Bio, BE beverages)
2. **Table « Passage Prélabel Label »** (page 2) : **4 conversions** :
   vivid (Flexipik), SOCIETE FIRMASOLUTIONS STARTUP (Firma Solutions), Color and Natural Extracts C-NEXTS, Ste Arrimapp Tech (Arrima Agritech).

Aucune table de retrait.

### STEP C / D — Comparaison référentiel
| Réf. MASTER | Valeur | PDF observé | Verdict |
|---|---|---|---|
| candidatures_officielles = 40 | 40 | Table principale = **40 lignes** | **COHÉRENT** |
| prelabels_officiels = 5 | 5 | P_acc table principale = **5** | **COHÉRENT** |
| labels_officiels = 14 | 14 | 9 directs + 4 conversions = **13** | **ÉCART CONFIRMÉ** : le PDF donne 13, pas 14 (différence de 1) |
| Commentaire « 10 Labels et 4 Prélabels à Labels » | — | 9 directs + 4 conversions (=13) | **ÉCART CONFIRMÉ** : 10 Labels directs déclarés mais **9** observés (4 conversions correctes) |
| lignes_pdf = 40 | 40 | Total doc = **44** (40+4) | **ÉCART CONFIRMÉ** : lignes_pdf MASTER = table principale seule (40), conversions (4) exclues |

**candidatures_officielles expliquées ?** OUI — 40 = table principale.
**Conversions visibles en table séparée ?** OUI (4 lignes nommées) ; cohérentes avec le « 4 Prélabels à Labels » du commentaire.
**Statut : ÉCART CONFIRMÉ** — l'écart porte sur le **nombre de Labels** (officiel 14 / commentaire 10 directs, vs PDF 13 totaux / 9 directs) et sur `lignes_pdf` (40 vs 44). Résidu **-4** cohérent avec la différence lignes_pdf vs total doc.

---

## Comparaison générale lignes_pdf (MASTER) vs total de lignes documentaires (PDF)

| Session | lignes_pdf MASTER | Total doc PDF observé | Écart MASTER vs PDF | Obs. |
|---|---|---|---|---|
| 04/2021 | 81 | 85 | **-4** | lignes_pdf = principal+retrait, conversions (4) exclues |
| 09/2021 | 38 | 38 | **0** | match parfait (principal 25 + conversions 13) |
| 10/2021 | 49 | 49 | **0** | match parfait (principal 41 + conversions 8) |
| 02/2023 | 42 | 45 | **-3** | lignes_pdf sous-estime de 3 |
| 04/2023 | 40 | 44 | **-4** | lignes_pdf = principal seul (40), conversions (4) exclues |

**Conclusion lignes_pdf :** la colonne `lignes_pdf` de MASTER **n'applique pas une règle de comptage unique** d'une session à l'autre : elle inclut les conversions pour 09/2021 et 10/2021, mais les exclut (en tout ou partie) pour 04/2021, 02/2023 et 04/2023. Elle **correspond exactement au PDF** uniquement pour **09/2021 (38/38)** et **10/2021 (49/49)**.

---

## STATUT FINAL PAR SESSION

| Session | Statut global | Points clés |
|---|---|---|
| **04/2021** | **COHÉRENT** (écart lignes_pdf documenté) | principal=80=candidatures ; labels 22=18+4conv ; commentaire officiel exact |
| **09/2021** | **ÉCART CONFIRMÉ** (anomalie candidatures officielles) | main=25 (SHYK reporté ✓) ; 13 conversions nommées exactement ✓ ; lignes doc 38 ✓ ; candidatures officielles 15 ≠ 25 (anomalie /results) |
| **10/2021** | **ÉCART CONFIRMÉ** (commentaire officiel erroné) | main=41=candidatures ; 23=15+8conv ✓ ; lignes 49 ✓ ; mais commentaire « 2 Labels / 13 conv » FAUX (8 conv réelles, copie de 09/2021) ; 11 pages vides |
| **02/2023** | **COHÉRENT** (écart lignes_pdf documenté) | main=33=candidatures ; labels 18=7+11conv ; prelabels 11 ✓ ; commentaire officiel exact |
| **04/2023** | **ÉCART CONFIRMÉ** (compte de Labels / commentaire) | main=40=candidatures ; prelabels 5 ✓ ; mais labels officiels 14 vs 13 PDF ; commentaire « 10 Labels » vs 9 directs observés |

**Légende des constats :**
- **OBSERVÉ (fait PDF direct) :** tous les comptages de lignes, listes de sociétés (conversions/retrait), lignes « reporté », pages vides.
- **HYPOTHÈSE :** conciliation de `candidatures_officielles=15` pour 09/2021 (« 2 directs + 13 conversions ») — plausible comme origine du chiffre 15 mais ne correspond à aucune ligne de la table principale.
- **ÉCART CONFIRMÉ :** chaque fois que le chiffre officiel/MASTER diffère du PDF de façon avérée.
- **NON DÉTERMINABLE :** non utilisé ici — tous les éléments ont pu être tranchés à partir du PDF (avec reconstitution par coordonnées pour 02/2023).
