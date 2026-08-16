# Prompt — Relecture indépendante des Comptes-Rendus de sessions

Tu donnes ce prompt (texte ci-dessous) à un autre agent IA (ChatGPT, Claude, Gemini…),
ainsi que le fichier texte d'**une** session (sorti par `scripts/extract_pdf_text.py`,
ex. `session_2025_12.txt`) OU le PDF officiel correspondant.

But : produire une **extraction indépendante** du tableau de décisions, au format strict
ci-dessous, pour la comparer avec nos données (parse automatique + relevés manuels).
Les divergences détectées alimentent les corrections de `public/data/manual_sessions/`.

---

## TEXTE À COLLER À L'AGENT

Tu es un analyste de données spécialisé dans l'extraction de tableaux depuis des
comptes-rendus officiels du programme **Startup Act (Tunisie)**.

On te fournit le compte-rendu de la **Session {SESSION}** (Startup Act, Comité de
labellisation). Extrais **chaque startup examinée** (décisions de Label et de Prélabel,
y compris les refus et les irrecevabilités) sous forme de JSON valide uniquement.

### Schéma de sortie (respecte-le à la lettre)

```json
{
  "session": "MM/AAAA",
  "rows": [
    {
      "societe": "nom exact de la société",
      "fondateurs": ["Nom Prénom", "Nom Prénom"],
      "secteur": "secteur exact tel qu'écrit",
      "type": "Label | Prélabel",
      "decision": "label_accorde | prelabel_accorde | label_refuse | prelabel_refuse | irrecevable",
      "resultat": "texte exact de la case Résultat",
      "recevable": "Oui | Non",
      "votes_1er_tour": {"oui": 0, "non": 0},
      "pitching": "6/0 | N.A",
      "conflit": "nom du membre ayant déclaré un conflit d'intérêt, ou N.A"
    }
  ]
}
```

### Règles strictes

1. **Une ligne par startup** — même si le compte-rendu étale une startup sur plusieurs
   paragraphes (fondateurs sur plusieurs lignes, case Résultat décalée).
2. Ne **jamais** inventer : si un champ n'est pas lisible, mets `""` (champ vide) au
   lieu de deviner. Si le nom de société est absent mais le fondateur présent, mets
   `"societe": ""` et le fondateur.
3. `decision` à déduire uniquement du texte de la case Résultat :
   - « Label Accordé » → `label_accorde` ; « Label Non Accordé » → `label_refuse`
   - « Prélabel Accordé » → `prelabel_accorde` ; « Prélabel Non Accordé » → `prelabel_refuse`
   - mention d'article de loi / « Recevabilité : Non » / statuts non communiqués → `irrecevable`
4. « Recevabilité » : `Oui` ou `Non` selon la colonne du 1er tour ; vide si absent.
5. `conflit` : copie le texte exact du membre (ex. « Hassen Aarfaoui a déclaré avoir
   un conflit d'intérêt ») ; sinon `N.A`.
6. Compte les lignes **strictement** : donne à la fin `"nb_rows_extraites": <nombre>`
   et `"commentaire": "explication de toute ambiguïté rencontrée"`.

### Sortie attendue

Un seul bloc JSON (aucun texte avant/après). Pas de tableaux, pas de commentaires
hors du JSON.

---

## Comparaison

Après réponse, compare avec :

- `public/data/session-pdfs-json/session_YYYY_MM.json` (notre parse automatique) ;
- `public/data/manual_sessions/YYYY_MM.json` si la session y figure (relevé manuel).

Critères de divergence à signaler : nombre de lignes différent, société/orthographe
différente, décision inverse, secteur différent, fondateurs manquants/différents.
Toute divergence documentée → corriger/créer `public/data/manual_sessions/YYYY_MM.json`.
