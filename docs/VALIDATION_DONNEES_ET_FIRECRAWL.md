# Validation Définitive des Données & Méthodologie Firecrawl

## 1. Données Vérités Validées (Startup Act Tunisie 2019–2026)

Les valeurs suivantes ont été extraites, recoupées et **définitivement validées** depuis les PDFs officiels des 85 sessions du Startup Act (`public/data/session-pdfs/`) :

- **1 311 Labels** accordés au total (809 nouveaux labels direct + 502 conversions).
- **623 Pré-Labels** octroyés au total.
- **2 958 Candidatures** examinées au cours des 85 sessions.
- **44,3 % Taux moyen** d'octroi de label ($\frac{1311}{2958}$).
- **80,6 % Taux de conversion** Pré-label $\rightarrow$ Label ($\frac{502}{623}$).
- **140 Retraits** de Label enregistrés.

> ⚠️ **Rappel** : Les données du tableau `/sessions` du site officiel `startup.gov.tn` contenaient des erreurs sur 20 sessions / 85. La source de vérité est consignée dans `public/data/corrections.json` et `public/data/parcours.json`.

---

## 2. Utilisation et Intégration de Firecrawl CLI

### A. Pourquoi utiliser Firecrawl ?
Firecrawl est utilisé via la commande CLI `firecrawl parse` (`npx -y firecrawl-cli@latest parse <pdf>`) pour transformer les comptes-rendus PDF bruts en documents Markdown structurés intégrant la mise en page sous forme de **tableaux Markdown natifs** (`| Société | Fondateurs | Secteur | ... |`).

### B. Pipeline et Emplacement des Livrables
- **Input (PDFs officiels)** : `public/data/session-pdfs/session_XXXX_XX.pdf`
- **Output (Markdown & JSONs)** : `public/data/agy/firecrawl_pdf_json/`
  - Contient **85 fichiers `.md`**
  - Contient **85 fichiers `.json`** (associant métadonnées, `char_count` et `full_text_markdown`)
  - Contient `summary.json` (récapitulatif global)

### C. Bonnes Pratiques d'Exécution avec Firecrawl
1. **Respect des Quotas (Rate Limit)** : Traiter les PDFs de manière séquentielle avec une temporisation d'au moins **5 à 7 secondes** entre deux appels afin de ne pas dépasser la limite API (10 à 15 req/min).
2. **Re-tentatives (Retries)** : En cas d'erreur `HTTP 499` ou `Gateway Timeout 504`, relancer l'extraction uniquement sur les sessions en échec sans écraser les fichiers JSON déjà générés et valides.
3. **Synchronisation Multi-Agents** : Le skill `mineru` et les instructions `firecrawl` sont synchronisés dans `.config/opencode`, `.config/kilo`, `.config/freebuff`, `.gemini` et `.gemini/config` pour assurer la même capacité sur tous les assistants de codage.

