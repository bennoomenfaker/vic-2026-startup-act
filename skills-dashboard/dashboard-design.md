# Dashboard Design & Admin UI Patterns (téléchargé le 16/08/2026)

Source : https://mcpmarket.com/tools/skills/dashboard-admin-ui-designer
Licence : MIT · name : dashboard-design

## Principes retenus et appliqués sur ce site

1. **Cartes KPI avec tendance** : valeur + indicateur de tendance (▲/▼/＝) + libellé + sous-titre. Cliquables pour détail.
2. **Sélection de graphiques** : line = tendance, bar = comparaison, donut = composition (max 5 parts), histogramme = distribution, scatter = relation, jauge/progress = objectif.
3. **Règles de graphique** : titre = l'insight (pas la dimension) ; axes étiquetés avec unités ; max 5-6 couleurs ; axe Y à zéro pour les barres ; tooltips avec valeur exacte ; grille légère en pointillés.
4. **Tableaux** : nombres alignés à droite (tabular-nums), texte à gauche ; en-tête collant (sticky top-0) ; hover row ; badges de statut cohérents ; recherche + filtre + pagination.
5. **Badges d'état** : succès/vert, avertissement/ambre, erreur/rouge, neutre/gris — couleurs cohérentes partout.
6. **Disclosure progressive** : résumé visible, détails repliés (modals, <details>, onglets).
7. **États vides / chargement** pour chaque vue de données.
8. **Responsive** : mobile 1 colonne, tablette 2, desktop multi-colonnes ; tables → cartes empilées sur mobile.
9. **Chiffres en tabular-nums** pour l'alignement vertical des données.

## Checklist appliquée (site Startup Act)
- [x] KPI cards en haut avec tendance + sous-titre
- [x] Graphiques titrés + tooltips (Chart.js)
- [x] Tables : sticky header, hover, filtres, recherche
- [x] Badges de statut cohérents (conforme/corrigée/décision)
- [x] Modals explicatifs (KPI + Parcours) — disclosure progressive
- [x] États vides (empty-state) sur les vues de données
- [x] tabular-nums sur les tableaux de données
