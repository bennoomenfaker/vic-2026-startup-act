"""Civic Ledger: synchronise les sessions 88 officielles sans perdre le catalogue KPI."""
from pathlib import Path
import json, re

PROJECT = Path(__file__).parent
TS = PROJECT / "client/src/data/dashboardData.ts"
SOURCE = Path("/home/ubuntu/vic-2026-startup-act-88-remote/public/data/dashboard_data.json")

def load_ts(path: Path):
    text = path.read_text(encoding="utf-8")
    match = re.search(r"export const dashboardData = (\{.*\}) as const;\s*$", text, flags=re.S)
    if not match:
        raise RuntimeError(f"Structure dashboardData.ts non reconnue: {path}")
    return json.loads(match.group(1))

def main():
    old = load_ts(TS)
    new = json.loads(SOURCE.read_text(encoding="utf-8"))
    # Preserve only the curated sector catalogue; rebuild every KPI from the
    # audited 88-session source so the catalogue cannot mix 85-session values.
    if "sectors" in old:
        new["sectors"] = old["sectors"]
    if "kpis" in old:
        new["kpis"] = old["kpis"]
    totals = new["meta"]
    labels = int(totals["totalLabels"])
    pre = int(totals["totalPreLabels"])
    candidates = int(totals["totalCandidatures"])
    sessions = int(totals["totalSessions"])
    detailed = int(totals.get("detailedEntries") or len(new.get("pdfExtracted", [])))
    accepted = labels + pre
    session_rows = new.get("sessions", [])
    conversions = sum(int(row.get("conversions") or 0) for row in session_rows)
    retraits = sum(int(row.get("retraits") or 0) for row in session_rows)
    sessions_with_retraits = sum(1 for row in session_rows if int(row.get("retraits") or 0) > 0)
    sessions_with_conversions = sum(1 for row in session_rows if int(row.get("conversions") or 0) > 0)
    total_startups = int(new.get("database", {}).get("totalStartups") or 0)
    labels_directs = max(0, labels - conversions)
    pre_restants = max(0, pre - conversions)
    replacements = {
        "KPI-01": str(total_startups),
        "KPI-02": f"{labels:,}".replace(",", " ") + " (corrigé)",
        "KPI-03": f"{candidates:,}".replace(",", " "),
        "KPI-04": f"{pre:,}".replace(",", " "),
        "KPI-05": f"{labels / candidates * 100:.1f} %" if candidates else "—",
        "KPI-13": f"{conversions:,}".replace(",", " "),
        "KPI-14": f"{conversions / pre * 100:.1f} %".replace(".", ",") if pre else "—",
        "KPI-15": f"{pre:,}".replace(",", " "),
        "KPI-16": f"{retraits:,}".replace(",", " "),
        "KPI-17": f"{conversions / labels * 100:.1f} %".replace(".", ",") if labels else "—",
        "KPI-18": str(sessions),
        "KPI-20": f"1 311 → {labels:,}".replace(",", " "),
        "KPI-21": f"617 → {pre:,}".replace(",", " "),
        "KPI-27": f"{labels:,}".replace(",", " ") + " / " + f"{pre:,}".replace(",", " "),
        "KPI-28": f"{candidates / sessions:.1f}".replace(".", ",") if sessions else "—",
        "KPI-41": str(sessions),
        "KPI-42": f"{labels / sessions:.1f}".replace(".", ",") if sessions else "—",
        "KPI-43": f"{pre / sessions:.1f}".replace(".", ",") if sessions else "—",
        "KPI-47": f"{labels / accepted * 100:.1f} %".replace(".", ",") if accepted else "—",
        "KPI-48": f"{pre / accepted * 100:.1f} %".replace(".", ",") if accepted else "—",
        "KPI-49": str(sessions_with_retraits),
    }
    interps = {
        "KPI-01": f"{total_startups} startups dans le registre de base; ce registre est distinct des {detailed} décisions détaillées. Une variation de −100 % dans une année filtrée signifie 0 observation dans ce sous-ensemble, pas la disparition du corpus total.",
        "KPI-02": f"{labels} labels officiels cumulés sur les {sessions} sessions.",
        "KPI-03": f"{candidates} candidatures officielles; à distinguer des {detailed} lignes détaillées des PDF.",
        "KPI-04": f"{pre} pré-labels officiels; le taux de conversion est un KPI distinct.",
        "KPI-05": f"Taux descriptif = {labels} labels / {candidates} candidatures officielles; les lignes détaillées ne servent pas de dénominateur.",
        "KPI-13": f"{conversions} conversions documentées pré-label → label sur {sessions_with_conversions} sessions.",
        "KPI-14": f"{conversions} / {pre} = {conversions / pre * 100:.1f} %; ce ratio compare un flux cumulé aux pré-labels accordés.",
        "KPI-15": f"{pre} pré-labels accordés servent de dénominateur au taux de conversion.",
        "KPI-16": f"{retraits} retraits officiels sur {sessions_with_retraits} sessions; ils sont séparés des candidatures.",
        "KPI-17": f"{conversions} / {labels} = {conversions / labels * 100:.1f} % des labels officiels correspondent au compteur de conversions.",
        "KPI-18": f"Le périmètre final couvre {sessions} sessions S0–S87.",
        "KPI-20": f"Le socle historique de 85 sessions est comparé au corpus final de {sessions} sessions: 1 311 → {labels} labels.",
        "KPI-21": f"Le compteur historique 617 est comparé au compteur final de {pre} pré-labels.",
        "KPI-27": f"Cumul final: {labels} labels et {pre} pré-labels.",
        "KPI-28": f"{candidates} / {sessions} = {candidates / sessions:.1f} candidatures officielles par session; aucune division par NaN.",
        "KPI-49": f"{sessions_with_retraits} sessions comportent au moins un retrait documenté.",
    }
    for kpi in new.get("kpis", []):
        kid = kpi.get("id")
        if kid in replacements:
            kpi["valeur"] = replacements[kid]
        if kid in interps:
            kpi["interp"] = interps[kid]
    new["catalogueSource"] = "50 KPI: catalogue repris et valeurs recalculées sur la série canonique 88 sessions auditée le 22 août 2026"
    new["qualityNote"] = f"Compteurs officiels: {candidates} candidatures, {labels} labels, {pre} prélabels. Registre détaillé: {detailed} lignes. Quatre lignes Reporté confirmées (S11, S12, S28, S67); ITMMA/06-2024 reste Pitch décalé et n'est pas Reporté."
    TS.write_text("export const dashboardData = " + json.dumps(new, ensure_ascii=False, indent=2) + " as const;\n", encoding="utf-8")
    print(json.dumps({"sessions": sessions, "candidatures": candidates, "labels": labels, "preLabels": pre, "detailedEntries": totals.get("detailedEntries"), "updated": sorted(replacements)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
