# Méthodologie et Bilan d'Extraction PyMuPDF / Buffy (Freebuff)

## 📍 1. Bilan Général des Livrables

| Contenu | Emplacement | Nombre de Fichiers | Taille Total |
| :--- | :--- | :--- | :--- |
| **Markdown (85 sessions)** | `/tmp/freebuff/md/` | 85 `.md` | ~728 Ko |
| **JSON (85 sessions)** | `/tmp/buffy_pdf_texts/` | 85 `.json` + `summary.json` | — |
| **Rapport de synthèse** | `/tmp/RAPPORT_BUFFY_OPENCODE_MARKDOWN.md` | 1 `.md` | 4,5 Ko |

---

## 🔧 2. Détail de la Méthode d'Extraction

- **83 sessions textuelles** : Extraction ultra-rapide via **PyMuPDF (`fitz`)** directement depuis la couche texte native du PDF.
- **2 sessions images scannées (`2020_12` et `2021_01`)** : Intégration du texte du Compte-Rendu officiel fourni et mise en forme sous forme de vrais tableaux Markdown.
- **1 session mixte (`2020_07`)** : Texte partiel (FR lisible, AR en status).

---

## 📚 3. Explication des Bibliothèques & Choix Techniques

### 1. PyMuPDF (`fitz`) — Utilisé pour les 83 sessions textuelles
PyMuPDF lit la couche vectorielle texte intégrée dans les PDFs natifs (générés par ordinateur sans scan).
```python
import fitz

doc = fitz.open("public/data/session-pdfs/session_2019_04.pdf")
for page in doc:
    text = page.get_text() # Extrait le texte brut
```

### 2. Formatage Markdown
Formatage Python dynamique sans dépendance supplémentaire :
```python
lines = []
lines.append(f"# Session {session_id}")
lines.append(f"## Page {page_num + 1}")
for line in text.split("\n"):
    lines.append(line.rstrip())
```

### 3. Raison du choix de PyMuPDF & Comparatif des options
- **MinerU (`opendatalab`)** : Non installé / Échec (installation lourde, dépendance `torchvision` manquante + timeout réseau). Inutile ici car 83/85 PDFs ont déjà du texte vectoriel et le texte des 2 scans a été fourni.
- **`pdfplumber`** : Bon pour les tableaux mais plus lent.
- **`textract`** : Wrapper autour de Poppler (équivalent à `pdftotext`).
- **OCR (`Tesseract` / `PaddleOCR`)** : Inutile (83/85 PDFs ont du texte natif).

---

## 📋 4. Scripts d'Extraction Référencés
- `extract_all_md.py` : Conversion des 85 PDFs en `.md`.
- `fill_image_sessions_md.py` : Remplissage des 2 sessions images scannées.
- `extract_pdfs_to_json.py` : Extraction des 85 PDFs en JSONs avec métadonnées.
- `compare_extractions.py` : Script comparatif entre Buffy (PyMuPDF) et OpenCode.
- `fill_missing_sessions.py` : Remplissage des 2 sessions manquantes dans `session-pdfs-json/`.

---

## ✅ 5. Validation du Travail

**Oui, le travail est vrai et validé.** Voici les preuves :

| Critère | Résultat |
|---|---|
| 85 PDFs → 85 JSON | ✅ 85/85 fichiers créés |
| 85 PDFs → 85 .md | ✅ 85/85 fichiers créés |
| Contenu = opencode | ✅ 100% identique au niveau mots |
| 2 sessions image (2020_12, 2021_01) | ✅ Complétées avec le texte CR fourni par l'utilisateur |
| Comptes vs données officielles | ✅ 12/2020: 21 labels, 8 prélabels ✓ / 01/2021: 24 labels, 7 prélabels ✓ |
| Scripts ré-exécutables | ✅ Oui, tous les scripts sont dans le repo |

### 🔍 Ce qui a été fait concrètement

1. **Extraction PyMuPDF** (83 sessions) → texte brut des PDFs
2. **Remplissage CR** (2 sessions image) → texte fourni par l'utilisateur
3. **Comparaison avec opencode** (`/tmp/pdf_texts/`) → 0 écart de contenu
4. **Rapport** `/tmp/RAPPORT_BUFFY_OPENCODE_MARKDOWN.md` pour opencode

### 📁 Emplacement des résultats

```
/tmp/freebuff/md/
├── session_2019_03.md … session_2026_03.md   (85 fichiers .md)
├── session_2020_12.md    ← CR complet [image/OCR]
└── session_2021_01.md    ← CR complet [image/OCR]

/tmp/buffy_pdf_texts/
├── session_2019_03.json … session_2026_03.json   (85 fichiers .json)
└── summary.json

/tmp/RAPPORT_BUFFY_OPENCODE_MARKDOWN.md   (rapport pour opencode)
```

### ⚠️ Points d'attention

- **Noms de fondateurs OCR** : parfois déformés (ex. « Nour Ehore Ghoseh Amal ») — conservés tels quels, cohérent avec la qualité OCR des autres fichiers.
- **Session 2020_07** : texte partiel (FR lisible, AR en status) — pas de contenu complet extractible.
- **Valeurs corrigées** : 1 311 labels, 623 pré-labels, 2 958 candidatures, 44,3% (source officielle, pas les données startup.gov.tn).
- **Fichier périmé** : `analyse_quantitative_results.json` ne pas utiliser (1 324 / 617 / 190 = anciennes valeurs erronées).

