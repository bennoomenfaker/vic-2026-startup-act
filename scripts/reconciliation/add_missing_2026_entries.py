#!/usr/bin/env python3
"""Ajoute les 11 lignes PDF 2026 manquantes dans le corpus canonique.

Les informations sont reprises des PDF versionnés et des contrôles manuels fournis.
Le script est idempotent par nom normalisé + session.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "public" / "data"
SESSION_DIR = DATA / "session-pdfs-json"
CANONICAL_PATH = DATA / "reextraction_88_canonical.json"

MISSING = [
    # 04/2026 — bloc principal
    {"session": "04/2026", "session_id": "S85", "societe": "Mathix Academy", "fondateurs": "Khalil Ben Ali; Zied Ben Mansour; Zahra Ideba", "secteur": "EdTech", "decision": "Label Non Accordé au 2 ème Tour", "resultat_normalise": "Label non accordé", "type_label": "Label", "tour_moment": "2ème tour", "anchor": "PolstarAI"},
    {"session": "04/2026", "session_id": "S85", "societe": "SURUS", "fondateurs": "Aymen Zghibi; Stefan Simon", "secteur": "Transportation", "decision": "Label Accordé au 3 ème Tour", "resultat_normalise": "Label accordé", "type_label": "Label", "tour_moment": "3ème tour", "anchor": "Hotelgenius.app"},
    {"session": "04/2026", "session_id": "S85", "societe": "Tunisia transfert", "fondateurs": "Ghaith Gharsalli; Haithem Gharsalli", "secteur": "TravelTech", "decision": "Prélabel Non Accordé au 2 ème Tour", "resultat_normalise": "Prélabel non accordé", "type_label": "Prélabel", "tour_moment": "2ème tour", "anchor": "EcomEyes"},
    # 05/2026 — bloc principal
    {"session": "05/2026", "session_id": "S86", "societe": "Deep SaaS", "fondateurs": "Mehrez SLAIMIA; Hlali Manel; Riadh Abidi; Mohamed Ben Amor", "secteur": "RH", "decision": "Prélabel Non Accordé au 3 ème Tour", "resultat_normalise": "Prélabel non accordé", "type_label": "Prélabel", "tour_moment": "3ème tour", "anchor": "neptune.tn"},
    {"session": "05/2026", "session_id": "S86", "societe": "Carbon Zero Tech", "fondateurs": "Mohamed Ben Nasr; Adnen Cherif; Aloui Noureddine; Nader Rachid", "secteur": "Energy", "decision": "Prélabel Non Accordé au 2 ème Tour", "resultat_normalise": "Prélabel non accordé", "type_label": "Prélabel", "tour_moment": "2ème tour", "anchor": "INOVENTIS"},
    {"session": "05/2026", "session_id": "S86", "societe": "NFASS - نفس", "fondateurs": "Mohamed Dhib; Omar Smati; Fourat Khelifi", "secteur": "HealthTech", "decision": "Prélabel Non Accordé au 2 ème Tour", "resultat_normalise": "Prélabel non accordé", "type_label": "Prélabel", "tour_moment": "2ème tour", "anchor": "cleanoov"},
    {"session": "05/2026", "session_id": "S86", "societe": "FIXITECHPRO", "fondateurs": "Zghida Khalil; Ahmed Ben; Elghali", "secteur": "ERP", "decision": "Prélabel Accordé au 2 ème Tour", "resultat_normalise": "Prélabel accordé", "type_label": "Prélabel", "tour_moment": "2ème tour", "anchor": "Komein"},
    {"session": "05/2026", "session_id": "S86", "societe": "Cuber", "fondateurs": "Neila Chtourou; Mohamed Ben Saad; Safwen Karoui; Mohamed Anis; Bach Tobj", "secteur": "Other", "decision": "Prélabel Accordé au 3 ème Tour", "resultat_normalise": "Prélabel accordé", "type_label": "Prélabel", "tour_moment": "3ème tour", "anchor": "SIROCCO (Jobinterview.live)"},
    {"session": "05/2026", "session_id": "S86", "societe": "shopyia", "fondateurs": "Daoud Cherif; Seifeddine Daoud; Ahmed Elyakoubi; Ahmed Mahouchi; Nadhir Ben Mohamed; Abdelnacer", "secteur": "Marketplace / e-commerce", "decision": "Prélabel Non Accordé au 2 ème Tour", "resultat_normalise": "Prélabel non accordé", "type_label": "Prélabel", "tour_moment": "2ème tour", "anchor": "ALCURA"},
    # 06/2026 — bloc principal
    {"session": "06/2026", "session_id": "S87", "societe": "Nvitee", "fondateurs": "Zeineb Hadj Ali; Ala Assali; Meriem Benzid", "secteur": "Websites and mobile apps", "decision": "Label Non Accordé au 2 ème Tour", "resultat_normalise": "Label non accordé", "type_label": "Label", "tour_moment": "2ème tour", "anchor": "SAVE YOUR ENERGY"},
    {"session": "06/2026", "session_id": "S87", "societe": "Creedex", "fondateurs": "Ala Guidara; Achraf Chabbouh", "secteur": "Other", "decision": "Prélabel Non Accordé au 2 ème Tour", "resultat_normalise": "Prélabel non accordé", "type_label": "Prélabel", "tour_moment": "2ème tour", "anchor": "Verdolive"},
]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def key(session: str, name: str) -> tuple[str, str]:
    return session, " ".join(name.casefold().split())


def make_entry(row: dict, decision_id: str, line: int) -> dict:
    return {
        "societe": row["societe"],
        "projet": "Non renseigné",
        "fondateurs": row["fondateurs"],
        "decision": row["decision"],
        "type_label": row["type_label"],
        "secteur": row["secteur"],
        "tour_moment": row["tour_moment"],
        "apres_pitching": "Non renseigné",
        "session_obtention_retrait": "Décision",
        "commentaires": row["decision"],
        "controle_qualite": "Extraction tabulaire PDF vérifiée; ligne ajoutée après audit manuel du PDF 2026",
        "resultat_normalise": row["resultat_normalise"],
        "section_pdf": "candidature",
        "source_pdf": f"session_{row['session'].split('/')[1]}_{row['session'].split('/')[0]}.pdf",
        "_displayDecision": row["resultat_normalise"].lower().replace("é", "e").replace(" ", "_"),
        "session": row["session"],
        "session_id": row["session_id"],
        "line": line,
        "decision_id": decision_id,
    }


def integrate_session(session: str, rows: list[dict]) -> list[dict]:
    path = SESSION_DIR / f"session_{session.split('/')[1]}_{session.split('/')[0]}.json"
    bundle = load(path)
    entries = bundle["entries"]
    existing = {key(e.get("session", session), e.get("societe", "")) for e in entries}
    max_id = max((int(str(e.get("decision_id", "")).split("_D")[-1].rstrip("b")) for e in entries if "_D" in str(e.get("decision_id", ""))), default=0)
    additions = [r for r in rows if key(session, r["societe"]) not in existing]
    by_anchor = {e.get("societe"): e for e in entries}
    for offset, r in enumerate(additions, start=1):
        line = next((int(e.get("line") or 0) for e in entries if e.get("societe") == r["anchor"]), len(entries) + offset) - 0.5
        entry = make_entry(r, f"{r['session_id']}_D{max_id + offset:04d}", int(line * 2) // 2)
        # Store temporary order; actual line numbers are normalized below.
        entry["_insert_before"] = r["anchor"]
        entries.append(entry)
    ordered = []
    additions_by_anchor = {e.get("_insert_before"): e for e in entries if e.get("_insert_before")}
    for e in entries:
        add = additions_by_anchor.get(e.get("societe"))
        if add:
            ordered.append(add)
        e.pop("_insert_before", None)
        ordered.append(e)
    # Preserve the PDF order created by insertion anchors and renumber documentary lines.
    for i, e in enumerate(ordered, start=1):
        e["line"] = i
    bundle["entries"] = ordered
    sd = bundle.get("session_data", {})
    sd["entries_detaillees"] = len(ordered)
    sd["candidatures_reexamen_pdf"] = len(ordered)
    sd["candidatures_corrigees"] = len(ordered) + int(sd.get("ajournes_hors_pdf") or 0)
    bundle["session_data"] = sd
    dump(path, bundle)
    return ordered


def main():
    all_entries = load(CANONICAL_PATH)
    by_session = {}
    for session in sorted({r["session"] for r in MISSING}):
        rows = [r for r in MISSING if r["session"] == session]
        updated = integrate_session(session, rows)
        by_session[session] = updated
    existing_keys = {key(e.get("session", ""), e.get("societe", "")) for e in all_entries["entries"]}
    for session, rows in by_session.items():
        for e in rows:
            k = key(session, e.get("societe", ""))
            if k not in existing_keys:
                all_entries["entries"].append(e)
                existing_keys.add(k)
        s = next(s for s in all_entries["sessions"] if s["session"] == session)
        s["entries"] = len(rows)
    all_entries["meta"]["detailed_entries"] = len(all_entries["entries"])
    all_entries["meta"]["detailedEntries"] = len(all_entries["entries"])
    all_entries["meta"]["lastUpdated"] = "2026-08-24T00:00:00+00:00"
    dump(CANONICAL_PATH, all_entries)
    print(json.dumps({"added_expected": len(MISSING), "canonical_entries": len(all_entries["entries"]), "sessions": {k: len(v) for k, v in by_session.items()}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
