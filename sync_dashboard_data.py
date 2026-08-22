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
    # Preserve the manually curated KPI and sector catalogue while replacing
    # the stale 85-session series with the audited 88-session source.
    for key in ("sectors", "kpis", "catalogueSource", "qualityNote"):
        if key in old:
            new[key] = old[key]
    totals = new["meta"]
    labels = int(totals["totalLabels"])
    pre = int(totals["totalPreLabels"])
    candidates = int(totals["totalCandidatures"])
    sessions = int(totals["totalSessions"])
    accepted = labels + pre
    replacements = {
        "KPI-03": f"{candidates:,}".replace(",", " "),
        "KPI-04": f"{pre:,}".replace(",", " "),
        "KPI-05": f"{labels / candidates * 100:.1f} %",
        "KPI-41": str(sessions),
        "KPI-42": f"{labels / sessions:.1f}".replace(".", ","),
        "KPI-43": f"{pre / sessions:.1f}".replace(".", ","),
        "KPI-47": f"{labels / accepted * 100:.1f} %".replace(".", ","),
        "KPI-48": f"{pre / accepted * 100:.1f} %".replace(".", ","),
        "KPI-49": str(sum(1 for row in new["sessions"] if int(row.get("retraits") or 0) > 0)),
    }
    for kpi in new.get("kpis", []):
        if kpi.get("id") in replacements:
            kpi["valeur"] = replacements[kpi["id"]]
        if kpi.get("id") == "KPI-03":
            kpi["interp"] = "3 079 candidatures officielles publiées par session; à distinguer des 3 528 lignes détaillées."
        if kpi.get("id") == "KPI-05":
            kpi["interp"] = "Taux descriptif = 1 356 labels / 3 079 candidatures officielles; les lignes détaillées ne servent pas de dénominateur."
    new["catalogueSource"] = "40 KPI repris du catalogue GitHub + 10 KPI dérivés explicitement documentés; série 88 sessions auditée le 22 août 2026"
    new["qualityNote"] = "Compteurs officiels: 3 079 candidatures, 1 356 labels, 641 prélabels. Registre détaillé: 3 528 lignes. Quatre lignes Reporté confirmées (S11, S12, S28, S67); ITMMA/06-2024 reste Pitch décalé et n'est pas Reporté."
    TS.write_text("export const dashboardData = " + json.dumps(new, ensure_ascii=False, indent=2) + " as const;\n", encoding="utf-8")
    print(json.dumps({"sessions": sessions, "candidatures": candidates, "labels": labels, "preLabels": pre, "detailedEntries": totals.get("detailedEntries"), "updated": sorted(replacements)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
