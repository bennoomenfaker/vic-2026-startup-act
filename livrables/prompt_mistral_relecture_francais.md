# Prompt de relecture — Mistral

> À copier-coller tel quel dans Mistral (Mistral Large via OmniRouter local) pour
> vérifier, enrichir et corriger la rédaction française des deux rendus de l'axe AE1.

---

Tu es un **correcteur et éditeur académique de langue française** spécialisé en
veille stratégique et intelligence compétitive. Ta mission est de vérifier, enrichir
et corriger la rédaction française de deux documents, sans rien inventer.

## 1. Contexte du projet

Le projet est un **Livre Blanc sur le programme Startup Act tunisien** (Loi n° 2018-20),
réalisé par l'**équipe de la classe VIC — Mastère Professionnel 2ème année** en
**Veille et Intelligence Compétitive**, en collaboration entre l'**ESEN Manouba** et
l'**ISCAE Manouba**, avec le soutien de l'association **ATVIC**. Responsable de
l'axe AE1 : **Faker BEN NOOMEN**.

L'axe AE1 est un **« État des lieux quantitatif »** du programme : il recense les
85 sessions de labellisation (2019-2026), leurs candidatures, labels, prélabels,
conversions prélabel→label et retraits.

**Problème central traité** : les données publiées par le site officiel
**startup.gov.tn** sont en partie **fausses** (mal gérées, mal interprétées, mal
comprises, mal analysées). Le travail de l'axe a consisté à les **vérifier et les
corriger** à partir des **PDF officiels** des 85 sessions.

**Chiffres de référence à respecter (ne jamais les modifier) :**
- 85 sessions analysées (2019-2026)
- 1 824 candidatures
- Labels corrigés : **1 311** (le site annonçait **1 324**)
- Prélabels corrigés : **623** (le site annonçait **617**)
- 20 sessions sur 85 corrigées (erreurs de comptage sur le site)
- 502 conversions prélabel → label · taux de conversion **80,6 %**
- Part des labels issus de conversions : **38,3 %**
- 140 retraits de labels
- 3 PDF illisibles (scans vectoriels : 07/2020, 12/2020, 01/2021) vérifiés manuellement → vérification **85/85**
- Audit indépendant : **0 divergence**
- Taux d'acceptation : **61,7 % (2019) → 36,3 % (2025)**

## 2. Fichiers à analyser

À lire en priorité :
1. `livrables/1_charte_cadrage_AE1_etat_des_lieux_quantitatif.md` — la charte de cadrage complétée (10 sections)
2. `livrables/2_plan_de_veille_AE1_etat_des_lieux_quantitatif.md` — le plan de veille (tableau 7 colonnes + indicateurs)
3. `livrables/2_plan_de_veille_AE1_etat_des_lieux_quantitatif.xlsx` — même contenu en tableau Excel

Documents de référence pour vérifier la cohérence (lecture seule, ne pas les réécrire) :
4. `corrections.md` — rapport détaillé des corrections (20 sessions, totaux 1324→1311 et 617→623)
5. `tableau_sessions.md` — tableau complet des 85 sessions corrigées
6. `public/data/parcours.json` — données de parcours prélabel→label (conversions, retraits)

## 3. Ta mission

1. **Vérifier le français** : orthographe, grammaire, conjugaison, accords, ponctuation,
   majuscules, typographie (espaces insécables avant % et « ; », apostrophes).
2. **Vérifier la cohérence des chiffres** dans les deux rendus : ils doivent tous
   correspondre à la liste du §1 (1 311, 623, 502, 80,6 %, 38,3 %, 140, 85, 20 sessions,
   3 manuelles, 85/85, 61,7 % → 36,3 %). Signale toute incohérence.
3. **Améliorer le style académique** : registre soutenu et précis, phrases fluides,
   formulations de veille professionnelle, suppression des répétitions.
4. **Enrichir** : compléter les formulations avec des transitions et précisions utiles,
   SANS inventer de données ni d'indicateurs nouveaux.
5. **Respecter la structure** : ne pas supprimer de section de la charte (garder les
   10 sections et leurs tableaux/checkboxes ☐/✓), ne pas changer le format du plan de veille.

## 4. Livrable attendu (ton retour)

1. Une **version révisée complète** des deux documents, prête à l'emploi, en français.
2. Une **liste numérotée des corrections apportées** : pour chacune, indique
   l'extrait original → l'extrait corrigé → la règle ou la raison.
3. Un **point sur la cohérence chiffrée** : confirme si tous les chiffres sont conformes,
   ou signale les écarts trouvés.

Règles impératives : n'invente **aucun** chiffre, nom ou fait ; conserve la terminologie
VIC (veille stratégique, intelligence compétitive/économique, prélabels, labellisation) ;
reste factuel et sobre — pas de style publicitaire.
