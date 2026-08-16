# Relevés manuels des Comptes-Rendus de sessions

La vérité de terrain. Chaque fichier `MM_AAAA.json` ici **remplace totalement** le parse
PDF automatique de la session (voir `scripts/build_founder_db.py` → `load_manual_sessions()`).
Une session relevée sort du rapport QA (`founder_db_qa_report.json`).

## Comment ajouter une session

1. Ouvre le Compte-Rendu officiel (PDF dans `public/data/session-pdfs/` ou en ligne sur
   startup.gov.tn, onglet `/sessions`).
2. Colle-moi le tableau des décisions (comme pour la Session 81 / 12-2025), de préférence
   en incluant pour chaque ligne : société · fondateurs · secteur · Label/Prélabel ·
   Recevabilité · votes des tours · Pitching · Conflit · Résultat.
3. Je structure en JSON au format ci-dessous et je relance la base.

Pas de format imposé pour ton copier-coller : texte brut = parfait (l'extraction `pdftotext
-layout` m'aide aussi à vérifier). Les conversions de prélabels→labels et les retraits
se mettent dans `conversions` et `retraits` (pas dans `rows`).

## Format du JSON

```json
{
  "session": "MM/AAAA",
  "intitule": "Startup Act | Session N | Mois Année | Compte-Rendu",
  "source": "Copier-coller manuel du Compte-Rendu officiel",
  "verifie_le": "AAAA-MM-JJ",
  "nb_rows": 41,
  "meta": {
    "candidatures_officielles": 41,
    "labels_officiels": 16,
    "prelabels_officiels": 6,
    "conflit_declare_par": ["Hassen Aarfaoui"]
  },
  "conversions": [
    { "societe": "...", "fondateurs": ["..."], "secteur": "...", "prelabel_session": "...", "resultat": "Label accordé" }
  ],
  "retraits": [
    { "societe": "...", "secteur": "...", "label_session": "MM/AAAA", "resultat": "Retrait du Label", "motif": "..." }
  ],
  "rows": [
    {
      "societe": "EVIMO",
      "fondateurs": ["Achraf GHARSALLI", "Seif SASSI"],
      "secteur": "Mobility",
      "type": "Label",
      "decision": "label_accorde",
      "resultat": "Label Accordé au 2 ème Tour",
      "recevable": "Oui",
      "votes": {"1er": 7, "2eme": 0, "3eme": 0, "resultat": 0},
      "pitching": "N.A",
      "conflit": "N.A"
    }
  ]
}
```

## Décisions acceptées

`label_accorde` · `prelabel_accorde` · `label_refuse` · `prelabel_refuse` · `irrecevable`

## Sessions les plus prioritaires (rapport QA)

12/2025 ✅ fait · 03/2026 · 10/2025 · 11/2025 · 02/2026 · 08/2025 · 04/2019 · 07/2025 · 01/2026
