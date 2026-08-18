#!/usr/bin/env python3
"""
Synchronise les 85 JSON du projet (session-pdfs-json) vers .firecrawl/
en fusionnant le texte brut PyMuPDF (pages_text) déjà présent dans .firecrawl/.
Vérifie les totaux : 1311 labels, 623 pré-labels, 2958 candidatures.
"""
import json, glob, os

PROJECT_DIR = os.path.join(os.path.dirname(__file__), '..', '..')
SESSION_PDFS_JSON = os.path.join(PROJECT_DIR, 'public', 'data', 'session-pdfs-json')
FIRECRAWL_DIR = os.path.join(PROJECT_DIR, '.firecrawl')

def main():
    files = sorted(glob.glob(os.path.join(SESSION_PDFS_JSON, 'session_*.json')))
    print(f"📂 Projet : {len(files)} sessions dans session-pdfs-json/")
    print(f"📂 Cible  : {FIRECRAWL_DIR}/")
    print(f"\n{'='*60}")

    total_l = total_p = total_c = 0
    updated = 0

    for fpath in files:
        fname = os.path.basename(fpath)
        fc_path = os.path.join(FIRECRAWL_DIR, fname)

        with open(fpath) as f:
            proj = json.load(f)

        # Load existing .firecrawl/ file for pages_text
        fc = {}
        if os.path.exists(fc_path):
            with open(fc_path) as f:
                fc = json.load(f)

        # Merge: project structured data + freebuff pages_text
        result = {
            'session': proj.get('session', ''),
            'annee': proj.get('annee', 0),
            'mois': proj.get('mois', 0),
            'pdf': proj.get('pdf', ''),
            'nb_entrees': proj.get('nb_entrees', 0),
            'source': 'session_pdfs_json_sync',
            'entrees': proj.get('entrees', []),
            'session_data': proj.get('session_data', {}),
        }
        # Keep pages_text from freebuff if present
        if 'pages_text' in fc:
            result['pages_text'] = fc['pages_text']

        sd = result['session_data']
        total_l += sd.get('labels', 0)
        total_p += sd.get('preLabels', 0)
        total_c += sd.get('candidatures', 0)

        with open(fc_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        updated += 1

    print(f"✅ {updated}/{len(files)} sessions synchronisées")
    print(f"\n  Labels       : {total_l}")
    print(f"  Pré-Labels   : {total_p}")
    print(f"  Candidatures : {total_c}")

    ok_l = total_l == 1311
    ok_p = total_p == 623
    ok_c = total_c == 2958

    print(f"\n  {'✅' if ok_l else '❌'} labels: {total_l} {'=' if ok_l else '≠'} 1311")
    print(f"  {'✅' if ok_p else '❌'} preLabels: {total_p} {'=' if ok_p else '≠'} 623")
    print(f"  {'✅' if ok_c else '❌'} candidatures: {total_c} {'=' if ok_c else '≠'} 2958")

    if ok_l and ok_p and ok_c:
        print(f"\n🎉 Toutes les données sont correctes !")
    else:
        print(f"\n⚠️  Des écarts ont été détectés.")

if __name__ == '__main__':
    main()
