# Dashboard KPI — données et méthode

Le dashboard utilise une copie locale typée de `dashboard_data.json`, enrichie avec le catalogue KPI repéré dans `streamlit-app/public/index.html` du dépôt GitHub. Les compteurs de référence affichés dans la vue d’ensemble sont **3 015 candidatures corrigées**, **1 311 Labels accordés**, **623 Prélabels accordés** et **1 934 décisions positives**.

Le catalogue source du dépôt contient 40 entrées `KPI-01` à `KPI-40`. Le dashboard affiche 50 indicateurs en ajoutant dix KPI dérivés transparents (`KPI-41` à `KPI-50`) calculés à partir des 85 sessions ou décrivant la qualité du périmètre. Ils sont marqués dans la source comme compléments dérivés et non comme nouvelles observations externes.

Les données externes ou manquantes restent dans le catalogue avec le statut `warn` ou `miss`. Elles ne sont pas remplacées par des valeurs inventées. La vue Qualité & sources expose ces cas, tandis que la vue Sessions affiche les séries directement disponibles pour les comparaisons.

Le champ candidatures de la vue globale utilise le compteur corrigé de 3 015 lorsque toutes les années sont sélectionnées. Pour une année isolée, le dashboard agrège les valeurs annuelles de la source disponible ; cette différence est volontairement visible dans le filtre de période.

La direction visuelle retenue est **Civic Ledger** : papier d’archive, encre bleu profond, safran de registre, typographie Source Serif 4 + DM Sans, et navigation latérale persistante orientée provenance.
