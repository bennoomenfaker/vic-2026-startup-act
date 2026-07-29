# Guide de l'Étude Quantitative — Startup Act Tunisie
## Analyse & Interprétation (Phase 4 : 22/09 → 19/10)

---

## Étape 0 : Préparer l'environnement

```bash
pip install pandas matplotlib seaborn plotly jupyter
```

Utiliser `analyse_quantitative.py` fourni ci-dessous.

---

## Étape 1 : Analyse des Sessions (85 sessions)

### Questions à回答
1. **Comment évolue le taux d'acceptation depuis 2019 ?** 
   → Baisse continue : 61,7% (2019) → 36,3% (2025) = **-41%**
2. **Y a-t-il une saisonnalité dans les labellisations ?**
   → Mois les plus actifs : décembre (102 labels), mai (98), mars (94)
   → Mois le moins actif : juillet (45)
3. **Quelle est la relation entre nombre de candidatures et labels accordés ?**
4. **Les commentaires des sessions révèlent-ils des tendances ?**

### Visualisations à produire
- Courbe d'évolution des candidatures/labels/pré-labels (line chart)
- Diagramme en barres des taux d'acceptation par année
- Heatmap mensuelle des labels (saisonnalité)

---

## Étape 2 : Analyse Sectorielle (18 secteurs)

### Questions
1. **Quels sont les secteurs dominants ?**
   → Top 4 (Business Software, Commerce, HealthTech, EdTech) = **51,6%** des startups
   → Indice de concentration HHI = **1 044** (concentration modérée)
2. **Comment la répartition sectorielle évolue-t-elle dans le temps ?**
3. **Y a-t-il des secteurs émergents à surveiller ?**
4. **Quelle est la diversité sectorielle par région ?** (si données géo disponibles)

### Visualisations
- Treemap des 18 secteurs
- Bar chart horizontal top 10 + "Autres"
- Évolution annuelle par secteur (stacked area chart)
- Pareto (80/20) : 4 secteurs = 51,6%, 18 secteurs = 100%

---

## Étape 3 : Analyse Temporelle des Créations

### Questions
1. **Quand les startups ont-elles été créées ?**
   → **Pic en 2020** : 214 startups créées (23,2% du total)
   → Croissance 2018→2020 : **+229%** (65 → 214)
   → Déclin 2020→2025 : **-93%** (214 → 16)
2. **Y a-t-il un décalage entre création et labellisation ?**
3. **Les startups créées pendant le COVID (2020) ont-elles un profil différent ?**

### Visualisations
- Histogramme des années de création
- Courbe de tendance avec moyenne mobile
- Comparaison création vs labellisation par année (dual axis)

---

## Étape 4 : Analyse des Résultats de Labellisation (1 824 entrées PDF)

### Questions
1. **Quel est le taux de retrait des labels ?**
   → **190 retraits** sur 1 824 entrées = **10,4%**
2. **Combien de startups passent du Pré-Label au Label ?**
   → **76 conversions** identifiées
3. **Quels secteurs ont le plus de retraits ?**
4. **Quelle est la durée de vie moyenne d'un label ?** (si données disponibles)

### Visualisations
- Diagramme circulaire : Label / Retrait / Conversion
- Taux de retrait par secteur (bar chart)
- Taux de conversion Pré-Label → Label par année

---

## Étape 5 : Analyse des Rapports Annuels

### Questions transversales
1. **Genre et diversité**
   → 2019 : **35%** femmes → 2021 : **21%** femmes → **Baisse significative**
   → 2020 : **63%** des startups ont des femmes dans l'équipe fondatrice
2. **Emploi**
   → 2020 : **3 222 emplois** créés
3. **Investissement**
   → 2020 : **2,1 mTND**
   → 2021 : **157 M USD** (dont 100M USD pour Instadeep)
4. **Internationalisation**
   → 2021 : **45%** des startups à l'international
5. **B2B vs B2C**
   → 2019 : **70%** B2B → 2021 : **65%** B2B

### Visualisations
- Tableau de bord comparatif 2019-2020-2021
- Radar chart des indicateurs clés
- Gap analysis : indicateurs mesurés vs objectifs initiaux

---

## Étape 6 : Analyses Croisées (Corrélations)

### À explorer

| Analyse | Données | Méthode |
|---------|---------|---------|
| Secteur × Année | Quels secteurs émergent et lesquels déclinent ? | Matrice de transition |
| Taux acceptation × Candidatures | Plus de candidatures = sélection plus dure ? | Régression linéaire |
| Mois de label × Secteur | Y a-t-il des saisons par secteur ? | Heatmap croisée |
| Fondateurs × Secteur | Y a-t-il une corrélation entre nombre de fondateurs et secteur ? | ANOVA |
| Retraits × Secteur | Quels secteurs perdent le plus de labels ? | Tableau de contingence |

---

## Étape 7 : Génération des Livrables Phase 4

### À produire avant le 19 octobre 2026

1. **Rapport d'analyse Axe 1** (PDF)
   - Exécutif summary (1 page)
   - 20+ visualisations avec interprétations
   - Tableaux de données sources
   - Annexes méthodologiques

2. **Dashboard interactif** (Web) 
   - KPIs en temps réel
   - Filtres (année, secteur, mois)
   - Export PNG des graphiques

3. **Base de données consolidée** (CSV/JSON) 
   - Données nettoyées et enrichies
   - Documentation des champs
   - Traçabilité des sources

4. **Recommandations préliminaires**
   - 5-10 recommandations basées sur les données
   - Priorisation par impact/effort
   - Chiffrage des enjeux

---

## Script Python d'Analyse

```python
import json, csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données
with open("public/data/dashboard_data.json") as f:
    dd = json.load(f)

# 1. Sessions → DataFrame
df_sessions = pd.DataFrame(dd['sessions'])
df_yearly = pd.DataFrame(dd['yearly'])
df_sectors = pd.DataFrame(dd['database']['sectors'])
df_creation = pd.DataFrame(dd['database']['byCreationYear'])
df_labels_month = pd.DataFrame(dd['database']['byLabelMonth'])
df_pdf = pd.DataFrame(dd['pdfExtracted'])

print("=== DONNÉES CHARGÉES ===")
print(f"Sessions: {df_sessions.shape}")
print(f"Yearly: {df_yearly.shape}")
print(f"Secteurs: {df_sectors.shape}")
print(f"Création: {df_creation.shape}")
print(f"Labels/mois: {df_labels_month.shape}")
print(f"PDF extrait: {df_pdf.shape}")

# 2. ANALYSE SESSIONS
print("\n=== ANALYSE SESSIONS ===")
print(df_yearly.to_string())

# Tendance taux d'acceptation
df_yearly['taux'] = df_yearly['tauxAcceptation'].astype(float)
print(f"\nTaux moyen: {df_yearly['taux'].mean():.1f}%")
print(f"Tendance: {df_yearly['taux'].iloc[0]:.1f}% → {df_yearly['taux'].iloc[-2]:.1f}%")
print(f"Baisse totale: {(df_yearly['taux'].iloc[-2] - df_yearly['taux'].iloc[0]) / df_yearly['taux'].iloc[0] * 100:.0f}%")

# 3. ANALYSE SECTEURS
print("\n=== ANALYSE SECTEURS ===")
total = df_sectors['count'].sum()
df_sectors['pct'] = df_sectors['count'] / total * 100
df_sectors = df_sectors.sort_values('count', ascending=False)
print(df_sectors.to_string())
print(f"\nTop 4 = {df_sectors.head(4)['count'].sum()}/{total} = {df_sectors.head(4)['count'].sum()/total*100:.1f}%")

# HHI
shares = (df_sectors['count'] / total * 100) ** 2
hhi = shares.sum()
print(f"HHI = {hhi:.0f} {'(concentration modérée)' if hhi < 1500 else '(concentration forte)'}")

# 4. ANALYSE CRÉATION
print("\n=== ANALYSE CRÉATION ===")
print(df_creation.to_string())
peak = df_creation.loc[df_creation['count'].idxmax()]
print(f"Pic: {peak['year']} ({peak['count']} startups)")

# 5. ANALYSE PDF
print("\n=== ANALYSE PDF ===")
retraits = df_pdf[df_pdf['resultat'].str.contains('retrait', case=False)]
conversions = df_pdf[df_pdf['resultat'].str.contains('passage|prélabel', case=False)]
labels = df_pdf[~df_pdf['resultat'].str.contains('retrait|passage|prélabel', case=False)]
print(f"Labels: {len(labels)}")
print(f"Retraits: {len(retraits)} ({len(retraits)/len(df_pdf)*100:.1f}%)")
print(f"Conversions Pré-Label→Label: {len(conversions)}")

# 6. SAUVEGARDER RAPPORT
with open("public/data/analyse_quantitative_results.json", "w") as f:
    json.dump({
        "sessions_yearly": df_yearly.to_dict('records'),
        "sectors": df_sectors.to_dict('records'),
        "creation": df_creation.to_dict('records'),
        "summary": {
            "total_sessions": len(df_sessions),
            "total_candidatures": int(df_yearly['candidatures'].sum()),
            "total_labels": int(df_yearly['labels'].sum()),
            "total_prelabels": int(df_yearly['preLabels'].sum()),
            "total_startups_uniques": dd['database']['totalStartups'],
            "taux_moyen": round(df_yearly['taux'].mean(), 1),
            "tendance_taux": "baisse",
            "pic_creation": int(peak['year']),
            "pic_creation_count": int(peak['count']),
            "hhi": round(hhi, 0),
            "top_4_sectors_pct": round(df_sectors.head(4)['count'].sum()/total*100, 1),
            "retrait_pct": round(len(retraits)/len(df_pdf)*100, 1)
        }
    }, f, indent=2, ensure_ascii=False)

print("\n✅ Rapport sauvegardé dans public/data/analyse_quantitative_results.json")
```

---

## Résultats déjà obtenus

| Indicateur | Valeur | Interprétation |
|------------|--------|----------------|
| Sessions | 85 (2019-2026) | Dispositif mature |
| Candidatures totales | 2 958 | Demande soutenue |
| Labels accordés | 1 324 | Mais baisse du taux d'acceptation |
| Startups uniques | 922 | Base active |
| Taux d'acceptation | 61,7% → 36,3% | Sélection plus rigoureuse |
| Secteur dominant | Business Software (23%) | Startups de services |
| Pic création startups | 2020 (214 startups) | Effet COVID + Startup Act |
| Retraits de labels | 10,4% | Taux modéré |
| Femmes fondatrices | 35% → 21% | Baisse préoccupante |
| Investissement 2021 | 157 M USD | Dont 100M Instadeep |
| Emplois (2020) | 3 222 | Impact économique |
| Grand Tunis | 48% | Concentration régionale |

---

## Prochaine étape concrète

1. Copier le script Python dans `analyse_quantitative.py`
2. Lancer : `python3 analyse_quantitative.py`
3. Produire les graphiques avec matplotlib
4. Intégrer dans le dashboard HTML existant avec Chart.js
5. Rédiger le rapport d'analyse pour le Livre Blanc

Les données sont prêtes, l'infrastructure de calcul aussi — on peut lancer l'analyse maintenant.
