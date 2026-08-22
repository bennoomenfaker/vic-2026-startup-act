/* Civic Ledger: editorial public-sector dashboard, ink navy + archive saffron, provenance-first data UI. */
import { useMemo, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import {
  AlertTriangle,
  ArrowDownRight,
  ArrowUpRight,
  BarChart3,
  BookOpen,
  CalendarDays,
  CheckCircle2,
  ChevronRight,
  CircleHelp,
  Database,
  Filter,
  LayoutDashboard,
  ListFilter,
  Search,
  ShieldCheck,
  Sparkles,
  Table2,
} from "lucide-react";
import { dashboardData } from "@/data/dashboardData";

const INK = "#18263D";
const SAFFRON = "#E9A23B";
const MOSS = "#4F7D68";
const TERRACOTTA = "#BD6B52";
const PALETTE = [INK, SAFFRON, MOSS, "#6B8EAE", TERRACOTTA];

const moneyFmt = new Intl.NumberFormat("fr-FR");
const fmt = (value: number) => moneyFmt.format(value);

type View = "overview" | "sessions" | "catalogue" | "quality";

type SessionRow = Record<string, any>;

type KpiRow = { id: string; nom: string; valeur: string; statut: string; page: string };

function normalizeSession(session: SessionRow, index: number): SessionRow {
  return {
    ...session,
    id: `S${index}`,
    accepted: Number(session.labels || 0) + Number(session.preLabels || 0),
    rate: Number(session.tauxAcceptationExact || session.tauxAcceptation || 0),
  };
}

export default function Home() {
  const [view, setView] = useState<View>("overview");
  const [year, setYear] = useState("all");
  const [query, setQuery] = useState("");
  const [selectedKpi, setSelectedKpi] = useState<KpiRow | null>(null);

  const sessions = useMemo(() => (dashboardData.sessions as readonly SessionRow[]).map(normalizeSession), []);
  const years = useMemo(() => Array.from(new Set(sessions.map((s) => s.year))).sort((a, b) => b - a), [sessions]);
  const filteredSessions = useMemo(
    () => sessions.filter((s) => year === "all" || String(s.year) === year),
    [sessions, year],
  );
  const totals = useMemo<{ applications: number; labels: number; preLabels: number; accepted: number }>(() => {
    const calculated = filteredSessions.reduce<{ applications: number; labels: number; preLabels: number; accepted: number }>(
      (acc, s) => ({
        applications: acc.applications + Number(s.candidatures || 0),
        labels: acc.labels + Number(s.labels || 0),
        preLabels: acc.preLabels + Number(s.preLabels || 0),
        accepted: acc.accepted + s.accepted,
      }),
      { applications: 0, labels: 0, preLabels: 0, accepted: 0 },
    );
    return calculated;
  }, [filteredSessions, year]);
  const qualityKpis = dashboardData.kpis.filter((k) => k.statut !== "ok");
  const catalogue = dashboardData.kpis.filter((k) => {
    const haystack = `${k.id} ${k.nom} ${k.page}`.toLowerCase();
    return haystack.includes(query.toLowerCase());
  });
  const yearlyRows = useMemo(() => (year === "all" ? dashboardData.yearly : dashboardData.yearly.filter((row) => String(row.year) === year)), [year]);
  const sectorRows = useMemo(() => {
    return (dashboardData.sectors as readonly any[])
      .map((s) => ({ name: String(s.sector || s.name || s.label || "Non renseigné"), value: Number(s.count ?? s.value ?? s.total ?? 0) }))
      .filter((s) => s.value > 0)
      .sort((a, b) => b.value - a.value)
      .slice(0, 5);
  }, []);

  const nav = [
    { id: "overview" as View, label: "Vue d’ensemble", icon: LayoutDashboard },
    { id: "sessions" as View, label: "Sessions", icon: CalendarDays },
    { id: "catalogue" as View, label: "Catalogue KPI", icon: ListFilter },
    { id: "quality" as View, label: "Qualité & sources", icon: ShieldCheck },
  ];

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-lockup">
          <div className="brand-mark" aria-hidden="true"><span /><span /><span /></div>
          <div><div className="eyebrow">Startup Act</div><div className="brand-name">Civic Ledger</div></div>
        </div>
        <div className="rail-rule" />
        <div className="rail-caption">OPERATING PICTURE · 2026</div>
        <nav className="nav-list" aria-label="Navigation principale">
          {nav.map(({ id, label, icon: Icon }) => <button key={id} className={`nav-item ${view === id ? "active" : ""}`} onClick={() => setView(id)}><Icon size={16} strokeWidth={1.8} /><span>{label}</span>{view === id && <ChevronRight size={14} className="nav-chevron" />}</button>)}
        </nav>
        <div className="sidebar-bottom">
          <div className="source-stamp"><Database size={14} /><span><strong>85 sessions</strong><br />Excel + JSON contrôlés</span></div>
          <div className="source-stamp"><ShieldCheck size={14} /><span><strong>Provenance visible</strong><br />Compteurs signalés</span></div>
        </div>
      </aside>

      <main className="main-canvas">
        <header className="topbar">
          <div><div className="breadcrumb">TABLEAU DE BORD <span>/</span> {nav.find((item) => item.id === view)?.label.toUpperCase()}</div><h1>{view === "overview" ? "85 sessions, une vue traçable." : nav.find((item) => item.id === view)?.label}</h1></div>
          <div className="topbar-actions"><label className="year-control"><CalendarDays size={15} /><span>Période</span><select value={year} onChange={(e) => setYear(e.target.value)}><option value="all">Toutes les années</option>{years.map((y) => <option key={y} value={String(y)}>{y}</option>)}</select></label><span className="status-pill"><span className="status-dot" /> Données synchronisées</span></div>
        </header>

        {view === "overview" && <Overview totals={totals} yearlyRows={yearlyRows} sectorRows={sectorRows} setView={setView} />}
        {view === "sessions" && <SessionsView sessions={filteredSessions} />}
        {view === "catalogue" && <CatalogueView catalogue={catalogue} query={query} setQuery={setQuery} onSelect={setSelectedKpi} />}
        {view === "quality" && <QualityView qualityKpis={qualityKpis} />}

        <footer className="footer-note"><span>Source de travail: <strong>dashboard_data.json</strong> + classeur Excel corrigé</span><span>Dernière mise à jour: 21 août 2026</span></footer>
      </main>
      {selectedKpi && <div className="modal-backdrop" onClick={() => setSelectedKpi(null)}><div className="kpi-modal" onClick={(e) => e.stopPropagation()}><button className="modal-close" onClick={() => setSelectedKpi(null)} aria-label="Fermer">×</button><div className="kpi-modal-id">{selectedKpi.id} · {selectedKpi.page}</div><h2>{selectedKpi.nom}</h2><div className="modal-value">{selectedKpi.valeur}</div><p>Ce KPI est repris du catalogue du dépôt ou calculé de manière dérivée à partir des données des 85 sessions. Les chiffres externes ou non calculables restent marqués.</p><div className={`catalogue-badge ${selectedKpi.statut}`}>{selectedKpi.statut === "ok" ? "Calculé" : selectedKpi.statut === "warn" ? "Donnée externe" : "À collecter"}</div></div></div>}
    </div>
  );
}

function Overview({ totals, yearlyRows, sectorRows, setView }: { totals: { applications: number; labels: number; preLabels: number; accepted: number }; yearlyRows: readonly any[]; sectorRows: readonly { name: string; value: number }[]; setView: (view: View) => void }) {
  const cards = [
    { label: "Candidatures déposées", value: totals.applications, note: "Périmètre sélectionné", accent: "ink", icon: BookOpen },
    { label: "Labels accordés", value: totals.labels, note: "Compteur officiel corrigé", accent: "saffron", icon: CheckCircle2 },
    { label: "Prélabels accordés", value: totals.preLabels, note: "Parcours à suivre", accent: "moss", icon: Sparkles },
    { label: "Décisions positives", value: totals.accepted, note: "Label + Prélabel", accent: "terracotta", icon: BarChart3 },
  ];
  return <>
    <section className="hero-strip"><div><div className="section-kicker">SIGNAL PRINCIPAL</div><p>Le dispositif a enregistré <strong>{fmt(totals.accepted)}</strong> décisions positives sur <strong>{fmt(totals.applications)}</strong> candidatures dans le périmètre sélectionné.</p></div><div className="hero-meta"><span>85 SESSIONS</span><span>2019 — 2026</span><span>TRACE EXCEL + JSON</span></div></section>
    <section className="metric-grid">{cards.map(({ label, value, note, accent, icon: Icon }) => <div className={`metric-card ${accent}`} key={label}><div className="metric-head"><span>{label}</span><Icon size={18} /></div><div className="metric-value">{fmt(value)}</div><div className="metric-note">{note}</div><div className="metric-rule" /></div>)}</section>
    <section className="insight-grid"><article className="panel wide-panel"><div className="panel-head"><div><div className="panel-kicker">TRAJECTOIRE</div><h2>La cadence de labellisation s’installe dans le temps</h2></div><button className="text-button" onClick={() => setView("sessions")}>Voir les sessions <ArrowUpRight size={14} /></button></div><div className="chart-wrap"><ResponsiveContainer width="100%" height={300}><LineChart data={yearlyRows as any[]}><CartesianGrid stroke="#D7D0C3" strokeDasharray="3 5" vertical={false} /><XAxis dataKey="year" tick={{ fill: "#667085", fontSize: 12 }} axisLine={false} tickLine={false} /><YAxis tick={{ fill: "#667085", fontSize: 12 }} axisLine={false} tickLine={false} width={36} /><Tooltip contentStyle={{ border: "1px solid #D7D0C3", borderRadius: 4, background: "#FFFDF8", fontSize: 12 }} /><Line type="monotone" dataKey="labels" name="Labels" stroke={INK} strokeWidth={3} dot={{ r: 3, fill: SAFFRON, strokeWidth: 2, stroke: INK }} /><Line type="monotone" dataKey="preLabels" name="Prélabels" stroke={MOSS} strokeWidth={2} dot={false} /></LineChart></ResponsiveContainer></div><div className="chart-legend"><span><i className="legend-dot ink" />Labels accordés</span><span><i className="legend-dot moss" />Prélabels accordés</span></div></article>
      <article className="panel signal-panel"><div className="panel-kicker">COMPOSITION</div><h2>Le parcours positif reste lisible</h2><div className="donut-wrap"><ResponsiveContainer width="100%" height={190}><PieChart><Pie data={[{ name: "Labels", value: totals.labels }, { name: "Prélabels", value: totals.preLabels }]} dataKey="value" innerRadius={54} outerRadius={78} paddingAngle={4}><Cell fill={INK} /><Cell fill={SAFFRON} /></Pie><Tooltip contentStyle={{ border: "1px solid #D7D0C3", borderRadius: 4, background: "#FFFDF8", fontSize: 12 }} /></PieChart></ResponsiveContainer><div className="donut-center"><strong>{Math.round((totals.labels / Math.max(1, totals.accepted)) * 100)}%</strong><span>Labels</span></div></div><div className="mini-stat"><span>Prélabels dans le positif</span><strong>{Math.round((totals.preLabels / Math.max(1, totals.accepted)) * 100)}%</strong></div></article></section>
    <section className="lower-grid"><article className="panel"><div className="panel-head"><div><div className="panel-kicker">SECTEURS</div><h2>Les cinq verticales les plus visibles</h2></div></div>{sectorRows.length ? <div className="chart-wrap compact"><ResponsiveContainer width="100%" height={240}><BarChart data={sectorRows as any[]} layout="vertical" margin={{ left: 18, right: 12 }}><CartesianGrid stroke="#E4DED4" strokeDasharray="3 5" horizontal={false} /><XAxis type="number" axisLine={false} tickLine={false} tick={{ fill: "#667085", fontSize: 11 }} /><YAxis type="category" dataKey="name" axisLine={false} tickLine={false} width={110} tick={{ fill: INK, fontSize: 11 }} /><Tooltip contentStyle={{ border: "1px solid #D7D0C3", borderRadius: 4, background: "#FFFDF8", fontSize: 12 }} /><Bar dataKey="value" name="Startups" fill={SAFFRON} radius={[0, 3, 3, 0]} /></BarChart></ResponsiveContainer></div> : <div className="empty-state">La structure sectorielle n’est pas disponible dans le périmètre sélectionné.</div>}</article><article className="panel notes-panel"><div className="panel-kicker">À RETENIR</div><h2>Lire le chiffre avant de le partager</h2><div className="note-row"><ShieldCheck size={16} /><span>Les compteurs Labels et Prélabels sont séparés pour éviter les doubles comptes.</span></div><div className="note-row"><AlertTriangle size={16} /><span>Les KPI externes restent visibles comme tels, sans substitution silencieuse.</span></div><div className="note-row"><Table2 size={16} /><span>Le détail session est accessible depuis la vue dédiée.</span></div></article></section>
  </>;
}

function SessionsView({ sessions }: { sessions: ReturnType<typeof normalizeSession>[] }) {
  return <section className="content-stack"><div className="view-intro"><div><div className="section-kicker">REGISTRE SESSIONNEL</div><p>Comparer les décisions positives, les candidatures et le taux d’acceptation sans perdre la période source.</p></div><div className="source-stamp large"><Database size={15} /><span>{sessions.length} sessions visibles</span></div></div><div className="panel session-chart"><ResponsiveContainer width="100%" height={340}><BarChart data={sessions}><CartesianGrid stroke="#E4DED4" strokeDasharray="3 5" vertical={false} /><XAxis dataKey="id" interval={Math.max(0, Math.floor(sessions.length / 14))} tick={{ fill: "#667085", fontSize: 11 }} axisLine={false} tickLine={false} /><YAxis axisLine={false} tickLine={false} tick={{ fill: "#667085", fontSize: 11 }} /><Tooltip contentStyle={{ border: "1px solid #D7D0C3", borderRadius: 4, background: "#FFFDF8", fontSize: 12 }} /><Legend /><Bar dataKey="labels" name="Labels" stackId="a" fill={INK} /><Bar dataKey="preLabels" name="Prélabels" stackId="a" fill={SAFFRON} /></BarChart></ResponsiveContainer></div><div className="panel table-panel"><div className="table-scroll"><table><thead><tr><th>Session</th><th>Période</th><th>Candidatures</th><th>Labels</th><th>Prélabels</th><th>Taux</th></tr></thead><tbody>{sessions.map((s) => <tr key={s.id}><td className="strong-cell">{s.id}</td><td>{s.month}/{s.year}</td><td>{fmt(Number(s.candidatures || 0))}</td><td><span className="table-number ink-text">{fmt(Number(s.labels || 0))}</span></td><td><span className="table-number saffron-text">{fmt(Number(s.preLabels || 0))}</span></td><td>{s.rate.toFixed(1)}%</td></tr>)}</tbody></table></div></div></section>;
}

function CatalogueView({ catalogue, query, setQuery, onSelect }: { catalogue: readonly KpiRow[]; query: string; setQuery: (q: string) => void; onSelect: (kpi: KpiRow) => void }) {
  return <section className="content-stack"><div className="view-intro"><div><div className="section-kicker">CATALOGUE DE MESURE</div><p>Les 40 KPI repris du dépôt sont complétés par 10 KPI dérivés, explicitement marqués dans la source.</p></div><div className="kpi-count-badge"><strong>{dashboardData.kpis.length}</strong><span>KPI catalogués</span></div></div><div className="search-row"><div className="search-box"><Search size={16} /><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Rechercher un KPI, une page, un thème…" /></div><span className="filter-label"><Filter size={14} /> {catalogue.length} résultats</span></div><div className="kpi-catalogue-grid">{catalogue.map((kpi) => <button className={`catalogue-card ${kpi.statut}`} key={kpi.id} onClick={() => onSelect(kpi)}><div className="catalogue-card-top"><span className="kpi-id">{kpi.id}</span><span className={`catalogue-badge ${kpi.statut}`}>{kpi.statut === "ok" ? "Calculé" : kpi.statut === "warn" ? "Externe" : "Manquant"}</span></div><h3>{kpi.nom}</h3><div className="catalogue-value">{kpi.valeur}</div><div className="catalogue-meta">{kpi.page}<ChevronRight size={13} /></div></button>)}</div></section>;
}

function QualityView({ qualityKpis }: { qualityKpis: readonly KpiRow[] }) {
  return <section className="content-stack"><div className="view-intro"><div><div className="section-kicker">PROVENANCE & QUALITÉ</div><p>Une vue de contrôle pour distinguer les indicateurs calculés, externes et à collecter.</p></div><div className="quality-summary"><span><i className="quality-dot ok" /> calculés</span><span><i className="quality-dot warn" /> externes</span><span><i className="quality-dot miss" /> à collecter</span></div></div><div className="quality-grid">{qualityKpis.map((kpi) => <article className="quality-card" key={kpi.id}><div className="kpi-id">{kpi.id}</div><h2>{kpi.nom}</h2><p>{kpi.valeur}</p><div className={`catalogue-badge ${kpi.statut}`}>{kpi.statut === "warn" ? "Donnée externe" : "À collecter"}</div></article>)}</div><div className="panel provenance-panel"><div className="panel-kicker">MÉTHODE</div><h2>Les chiffres ne sont pas tous du même type</h2><p>Les compteurs Labels et Prélabels sont issus des 85 sessions. Les KPI géographiques, économiques ou de propriété intellectuelle peuvent dépendre de rapports externes. Le statut reste affiché pour éviter de confondre une donnée calculée et une donnée à actualiser.</p></div></section>;
}
