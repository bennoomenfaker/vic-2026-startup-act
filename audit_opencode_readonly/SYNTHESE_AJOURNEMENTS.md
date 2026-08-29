# Audit — Cas ajournés / reportés sur les 88 sessions (03/2019 → 06/2026)

Audit en lecture seule — aucune source modifiée. Généré le 23/08/2026.
Périmètre : `public/data/session-pdfs-json/session_*.json` (88 fichiers), `public/data/sessions.json`, recoupements `corrections.json` et `manual_sessions/`.

## Méthodologie

1. Scan des 88 fichiers session : champs `decision`, `resultat_normalise`, `commentaires` (mots-clés « report », « ajourn », puis « suivante/décalé/différé/suspendu ») + champ `session_obtention_retrait`.
2. Vérification du champ `_displayDecision == "reporte"` (étiquette dédiée du corpus).
3. Croisement avec `sessions.json` (champs `ajournes`, `reportes`, `commentaires`) pour les 88 sessions.
4. Traçabilité : recherche de chaque société reportée dans les 87 autres sessions.

## Résultat global

| Catégorie | Nombre | Sessions |
|---|---|---|
| **Décisions « Reporté » nominatives** (PDF) | **4** | 02/2020, 03/2020, 07/2021, 10/2024 |
| **Cas « ajournés » comptabilisés sans nom** (tableau officiel startup.gov.tn) | **4** | 03/2019 (2), 04/2019 (1), 06/2019 (1) |
| Statut administratif proche (pitch décalé, hors périmètre officiel « Reporté ») | 1 | ITMMA, 06/2024 |

Total officiel déclaré dans `sessions.json` : **8 cas** (4 `reportes`=1 + 4 `ajournes` cumulés).

## Les 4 décisions « Reporté » confirmées (cas nommés)

| Session | Société | Fondateurs | Issue retracée |
|---|---|---|---|
| 02/2020 | Tunisia Biotech | Oualid Sebai | **Non retracée** — aucune réapparition dans les 88 sessions ; sort du corpus |
| 03/2020 | Campus Numérique des métiers | Fethi Zoghlami | 04/2020 : Label non accordé ; nouvelle demande refusée en 05/2023 (2ème tour). Motif : problèmes techniques lors du pitching |
| 07/2021 | TN Smartbot | Sofienne Mallek ; Assil Salah | 08/2021 : Label non accordé (désistement suite à la cession de la société) |
| 10/2024 | RYBSEN | Yassine Rezgui ; Adnene Rezgui | 11/2024 : **Label accordé au 3ème tour** (« après le report de la session d'octobre 2024 ») |

## Les 4 ajournements « compteur » de 2019 (sans identification nominative)

- **03/2019 : 2 ajournés** — commentaire officiel « 2 ajourné à la session suivante » (`ajournes=2`).
- **04/2019 : 1 ajourné** — écart documenté : le CR liste 52 décisions (33 labels exacts) vs 51 candidatures affichées ; l'une des 52 lignes correspond probablement au dossier ajourné, non identifiable par recoupement des noms (voir `manual_sessions/2019_04.json` → `meta.ecart_a_documenter` et `corrections.json`). Ne pas recalculer le taux officiel 64,7 % sur 52.
- **06/2019 : 1 ajourné** — commentaire officiel « 1 ajourné à la session suivante » (`ajournes=1`).

Aucune ligne nominative « ajourné » n'existe dans les JSON détaillés de ces sessions ni champ `ajournes` au niveau fichier : les noms ne sont pas restituables depuis les sources disponibles.

## Cas limite exclu du périmètre

- **ITMMA (06/2024)** : « Pitch décalé pour la session de juillet 2024 ». L'annotation du corpus précise que ce statut administratif ne constitue pas une décision « Reporté ». Issue : 07/2024 Label non accordé au 3ème tour. Consigné dans le CSV à titre informatif.

## Points d'attention méthodologiques

1. **Le critère « `session_obtention_retrait` non vide = reporté » est invalide** : ce champ porte le mois d'obtention/retrait du label pour les conversions et retraits (ex. « Avril 2021 », « Décision », « Conversion », « Retrait »). ~370 entrées non vides, toutes conversions/retraits/décisions normales — aucune ne signale un report.
2. Les 7 KPI du dashboard ne sont pas impactés : les reports sont exclus des labels/refus et les compteurs officiels (`candidatures`) intègrent déjà les ajustements documentés.
3. Cohérence vérifiée : le champ `_displayDecision="reporte"` marque exactement les 4 mêmes lignes que la détection textuelle ; `sessions.json` déclare `reportes=1` pour exactement ces 4 sessions.
4. Faux positifs écartés : NEFEL EDUCATION (02/2022), Relead (03/2022), MIGsens (03/2023) (« session suivante » hors contexte report) ; Domaine El Htouba (12/2023, « décalré » = typo de « déclaré ») ; RYBSEN 11/2024 (mention rétrospective du report, décision = Label accordé).

## Fichiers produits

- `audit_opencode_readonly/ajournements_reports.csv` — 8 lignes (4 Reporté + 1 ITMMA + 3 compteurs 2019).
- `audit_opencode_readonly/SYNTHESE_AJOURNEMENTS.md` — ce fichier.

## Vérification des cas connus demandés

- ✅ Tunisia Biotech (02/2020) — trouvé, reporté, issue non retracée
- ✅ Campus Numérique (03/2020) — trouvé, reporté → refus 04/2020 (et 05/2023)
- ✅ TN Smartbot (07/2021) — trouvé, reporté → désistement 08/2021
- ✅ RYBSEN (10/2024) — trouvé, pitch reporté → Label accordé 11/2024
