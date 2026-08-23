# Rapport académique complet — Réconciliation PDF primaire du Startup Act tunisien
> **Périmètre statistique final.** L’étude distingue le compteur institutionnel de **3 079 candidatures officielles**, le corpus de **3 555 lignes détaillées PDF**, et le compteur corrigé de **3 558 candidatures** obtenu en ajoutant **3 ajournés hors PDF** signalés par des commentaires officiels (2 en 03/2019 et 1 en 06/2019). Ces trois mesures ne sont pas interchangeables.


## Résumé

Ce travail constitue une réconciliation documentaire de **88 sessions** de labellisation du Startup Act tunisien. L’objectif est de ne pas remplacer silencieusement les compteurs institutionnels, mais de les comparer à une extraction ligne par ligne des PDF officiels. La conclusion méthodologique est que le compteur officiel et le volume détaillé PDF sont deux unités complémentaires.

## 1. Problématique et sources

La page institutionnelle de résultats fournit des compteurs agrégés par session. Les comptes rendus PDF fournissent les entreprises, fondateurs, secteurs, décisions, conversions, retraits et reports. Lorsque les deux sources divergent, le PDF est retenu comme **preuve primaire pour la correction documentaire**, tandis que la valeur institutionnelle est conservée comme repère historique.

## 2. Méthodologie

Le corpus canonique a été construit à partir de 88 PDF. Chaque ligne reçoit un identifiant de décision, une session, une entreprise, les fondateurs disponibles, la décision brute, une catégorie normalisée et un champ de provenance. Les corrections sont auditées par session. Les conversions et retraits ne sont pas supprimés : ils sont conservés comme événements documentaires distincts.

## 3. Résultats quantitatifs

| Mesure | Série officielle | Série corrigée PDF |
|---|---:|---:|
| Sessions | 88 | 88 |
| Candidatures | 3 079 | 3 555 |
| Labels | 1 356 | 1 343 |
| Prélabels | 641 | 647 |
| Lignes PDF détaillées | — | 3 555 |

La série corrigée PDF donne **+476** lignes par rapport au compteur officiel. Ce résultat ne signifie pas que 476 candidatures institutionnelles nouvelles ont été déposées : il reflète une différence entre dossiers comptés institutionnellement et événements/lignes conservés dans les PDF.

## 4. Ventilation des décisions

- **Décision non précisée — motif administratif :** 4 lignes.
- **Label accordé :** 1 232 lignes.
- **Label non accordé :** 653 lignes.
- **Pitch décalé :** 1 lignes.
- **Prélabel accordé :** 634 lignes.
- **Prélabel non accordé :** 980 lignes.
- **Reporté :** 5 lignes.
- **Retrait Label :** 46 lignes.

La somme des catégories est **3 555**, exactement égale aux **3 555 lignes PDF**. Cette égalité est une égalité de classification documentaire ; elle ne doit pas être comparée directement au compteur officiel sans tenir compte des conversions, retraits et reports.

## 5. Exemple analytique : S62 / 05-2024

S62 illustre le problème de manière nette : **39 candidatures officielles** contre **46 lignes documentaires PDF**. Les 4 dossiers portant uniquement le motif administratif « Non présentation des états financiers… » sont inclus dans les 39 candidatures officielles et reçoivent le statut « Décision non précisée — motif administratif ». Le tableau corrigé conserve donc 46 lignes, sans prétendre que les 7 lignes supplémentaires sont 7 nouvelles candidatures institutionnelles.

## 6. Qualité, transparence et reproductibilité

Les exports JSON, CSV, SQL, SQLite et Excel sont produits à partir du même corpus canonique. Le classeur contient une synthèse, un tableau de rapprochement officiel → corrigé PDF, le détail des décisions et une feuille par session. Les cinq Reporté et les limites OCR sont explicitement signalés. S16 a fait l’objet d’un contrôle visuel de structure, mais les noms faiblement lisibles restent soumis à une validation humaine ponctuelle.

## Conclusion

La version recommandée pour les KPI analytiques de cette étude est la **série corrigée PDF** ; la version recommandée pour citer l’indicateur institutionnel est la **série officielle**. Les deux doivent apparaître ensemble dans toute restitution afin d’éviter de transformer un écart de définition en contradiction cachée.
