/* Civic Ledger: editorial public-sector dashboard, ink navy + archive saffron, provenance-first data UI. */
// Civic Ledger: registre analytique clair, fond ivoire, encre marine et accents saffran ; les notes de provenance restent visibles et sobres.
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
const REPORT_SESSIONS = new Set(["S11", "S12", "S28", "S30", "S67"]);

const moneyFmt = new Intl.NumberFormat("fr-FR");
const decimalFmt = new Intl.NumberFormat("fr-FR", { minimumFractionDigits: 1, maximumFractionDigits: 1 });
const fmt = (value: number) => moneyFmt.format(value);
const fmtDecimal = (value: number) => decimalFmt.format(value);

type View = "overview" | "sessions" | "catalogue" | "quality" | "study";

type SessionRow = Record<string, any>;

type KpiRow = { id: string; nom: string; valeur: string; statut: string; page: string; interp?: string; desc?: string; util?: string; source?: string; calcul?: string };

const KPI_CALCUL: Record<string, string> = {
  'KPI-01': 'Comptage des startups uniques après normalisation des noms.',
  'KPI-02': 'Labels officiels = somme des Labels publiés ; corrigés = nouveaux Labels + conversions Prélabel → Label.',
  'KPI-03': 'Somme des compteurs institutionnels de candidatures des 88 sessions.',
  'KPI-04': 'Somme des Prélabels publiés ; la série corrigée est contrôlée sur les lignes PDF.',
  'KPI-05': 'Labels ÷ candidatures × 100, avec le même périmètre au numérateur et au dénominateur.',
  'KPI-06': 'HHI = Σ(part du secteur en %)².',
  'KPI-07': 'Secteur dominant = secteur ayant l’effectif maximal ; part = effectif ÷ total × 100.',
  'KPI-08': 'Top 4 = effectif des quatre premiers secteurs ÷ total × 100.',
  'KPI-09': 'Startups du Grand Tunis ÷ startups géolocalisées × 100.',
  'KPI-10': 'Startups de Sousse ÷ startups géolocalisées × 100.',
  'KPI-11': 'Startups de Kairouan ÷ startups géolocalisées × 100.',
  'KPI-12': 'Startups de Kasserine ÷ startups géolocalisées × 100.',
  'KPI-13': 'Comptage des parcours Prélabel → Label documentés.',
  'KPI-14': 'Conversions ÷ Prélabels accordés × 100.',
  'KPI-15': 'Comptage des Prélabels accordés sans les compter comme Labels.',
  'KPI-16': 'Comptage des décisions de retrait de Label publiées.',
  'KPI-17': 'Conversions ÷ Labels accordés × 100.',
  'KPI-18': 'Comptage des sessions présentes dans le corpus.',
  'KPI-19': 'Comptage des sessions ayant une correction documentée.',
  'KPI-20': 'Comparaison Labels institutionnels avant correction / Labels corrigés PDF.',
  'KPI-21': 'Comparaison Prélabels institutionnels avant correction / Prélabels corrigés PDF.',
  'KPI-22': 'Valeur reprise du rapport annuel cité ; non recalculée depuis les lignes de session.',
  'KPI-23': 'Valeur reprise du rapport annuel cité, avec son unité et son année.',
  'KPI-24': 'Valeur reprise du rapport annuel cité ; aucune conversion sans source de change.',
  'KPI-25': 'Fondatrices femmes ÷ fondateurs dont le genre est connu × 100.',
  'KPI-26': '(Candidatures t − candidatures t−1) ÷ candidatures t−1 × 100.',
  'KPI-27': 'Somme progressive des Labels et Prélabels par année.',
  'KPI-28': 'Candidatures du périmètre ÷ nombre de sessions du même périmètre.',
  'KPI-29': 'Moyenne de la différence entre date du Prélabel et date du Label pour les parcours appariés.',
  'KPI-30': 'Comptage des retraits par motif réglementaire publié.',
  'KPI-31': 'Moyenne de (année de labellisation − année de création).',
  'KPI-32': 'Histogramme des âges individuels calculés à partir des deux dates.',
  'KPI-33': 'Moyenne de (2026 − année de création) pour les startups datées.',
  'KPI-34': 'Comptage des startups par forme juridique renseignée.',
  'KPI-35': 'Comptage des fondateurs identifiés et dédoublonnés.',
  'KPI-36': 'Fondateurs d’un genre ÷ fondateurs dont le genre est connu × 100.',
  'KPI-37': 'Distribution descriptive des variables disponibles, sans imputation.',
  'KPI-38': 'Comptage des startups par gouvernorat renseigné.',
  'KPI-39': 'Comptage des startups par secteur et par année.',
  'KPI-40': 'Startups DeepTech/PI identifiées ÷ startups documentées × 100.',
  'KPI-41': 'Comptage des sessions présentes dans le corpus final.',
  'KPI-42': 'Labels accordés ÷ nombre de sessions.',
  'KPI-43': 'Prélabels accordés ÷ nombre de sessions.',
  'KPI-44': 'Maximum du compteur Labels parmi les sessions.',
  'KPI-45': 'Maximum du compteur Prélabels parmi les sessions.',
  'KPI-46': 'Maximum de la somme annuelle des Labels.',
  'KPI-47': 'Labels ÷ (Labels + Prélabels) × 100.',
  'KPI-48': 'Prélabels ÷ (Labels + Prélabels) × 100.',
  'KPI-49': 'Comptage des sessions dont le nombre de retraits documentés est supérieur à zéro.',
  'KPI-50': 'Comptage des KPI dont la source principale est externe ou dont le calcul est encore à compléter.',
};

function getKpiCalculation(kpi: KpiRow): string {
  return kpi.calcul || KPI_CALCUL[kpi.id] || 'Méthode non calculable avec les données actuelles ; consulter la source indiquée.';
}

function normalizeSession(session: SessionRow, index: number): SessionRow {
  return {
    ...session,
    id: `S${index}`,
    candidaturesOfficielles: Number(session.candidaturesOfficielles ?? session.candidatures ?? 0),
    labelsOfficiels: Number(session.labelsOfficiels ?? session.labels ?? 0),
    preLabelsOfficiels: Number(session.preLabelsOfficiels ?? session.preLabels ?? 0),
    candidaturesCorrigees: Number(session.candidaturesCorrigees ?? session.entries ?? session.candidatures ?? 0),
    labelsCorriges: Number(session.labelsCorriges ?? session.labels ?? 0),
    preLabelsCorriges: Number(session.preLabelsCorriges ?? session.preLabels ?? 0),
    accepted: Number(session.labelsCorriges ?? session.labels ?? 0) + Number(session.preLabelsCorriges ?? session.preLabels ?? 0),
    rate: Number(session.candidaturesCorrigees) ? Number(session.labelsCorriges) / Number(session.candidaturesCorrigees) * 100 : 0,
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
  const totals = useMemo<{ applications: number; officialApplications: number; detailedEntries: number; labels: number; preLabels: number; accepted: number; sessions: number; averageApplications: number; conversions: number }>(() => {
    const calculated = filteredSessions.reduce<{ applications: number; officialApplications: number; detailedEntries: number; labels: number; preLabels: number; accepted: number; conversions: number }>(
      (acc, s) => ({
        applications: acc.applications + Number(s.candidaturesCorrigees || 0),
        officialApplications: acc.officialApplications + Number(s.candidaturesOfficielles || 0),
        detailedEntries: acc.detailedEntries + Number(s.detailedEntries || s.entries || 0),
        labels: acc.labels + Number(s.labelsCorriges || 0),
        preLabels: acc.preLabels + Number(s.preLabelsCorriges || 0),
        accepted: acc.accepted + s.accepted,
        conversions: acc.conversions + Number(s.conversions || 0),
      }),
      { applications: 0, officialApplications: 0, detailedEntries: 0, labels: 0, preLabels: 0, accepted: 0, conversions: 0 },
    );
    const sessionCount = filteredSessions.length;
    return { ...calculated, sessions: sessionCount, averageApplications: sessionCount ? calculated.applications / sessionCount : 0 };
  }, [filteredSessions, year]);
  const qualityKpis = dashboardData.kpis.filter((k) => k.statut !== "ok");
  const catalogue = dashboardData.kpis.filter((k) => {
    const haystack = `${k.id} ${k.nom} ${k.page}`.toLowerCase();
    return haystack.includes(query.toLowerCase());
  });
  const yearlyRows = useMemo(() => (year === "all" ? dashboardData.yearly : dashboardData.yearly.filter((row) => String(row.year) === year)), [year]);
  const decisionRows = useMemo(() => [
    { name: "Labels accordés", value: filteredSessions.reduce((sum: number, session: SessionRow) => sum + Number(session.labelsCorriges || 0), 0) },
    { name: "Prélabels accordés", value: filteredSessions.reduce((sum: number, session: SessionRow) => sum + Number(session.preLabelsCorriges || 0), 0) },
    { name: "Conversions", value: filteredSessions.reduce((sum: number, session: SessionRow) => sum + Number(session.conversions || 0), 0) },
    { name: "Retraits", value: filteredSessions.reduce((sum: number, session: SessionRow) => sum + Number(session.retraits || 0), 0) },
  ].filter((row) => row.value > 0), [filteredSessions]);
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
    { id: "study" as View, label: "Étude quantitative", icon: BookOpen },
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
          <div className="source-stamp"><Database size={14} /><span><strong>88 sessions</strong><br />Excel + JSON contrôlés</span></div>
          <div className="source-stamp"><ShieldCheck size={14} /><span><strong>Provenance visible</strong><br />Compteurs signalés</span></div>
        </div>
      </aside>

      <main className="main-canvas">
        <header className="topbar">
          <div><div className="breadcrumb">TABLEAU DE BORD <span>/</span> {nav.find((item) => item.id === view)?.label.toUpperCase()}</div><h1>{view === "overview" ? "88 sessions, une vue traçable." : nav.find((item) => item.id === view)?.label}</h1></div>
          <div className="topbar-actions"><label className="year-control"><CalendarDays size={15} /><span>Période</span><select value={year} onChange={(e) => setYear(e.target.value)}><option value="all">Toutes les années</option>{years.map((y) => <option key={y} value={String(y)}>{y}</option>)}</select></label><span className="status-pill"><span className="status-dot" /> Données synchronisées</span></div>
        </header>

        {view === "overview" && <Overview totals={totals} yearlyRows={yearlyRows} sectorRows={sectorRows} decisionRows={decisionRows} setView={setView} />}
        {view === "study" && <StudyView sessions={filteredSessions} />}
        {view === "sessions" && <SessionsView sessions={filteredSessions} />}
        {view === "catalogue" && <CatalogueView catalogue={catalogue} query={query} setQuery={setQuery} onSelect={setSelectedKpi} />}
        {view === "quality" && <QualityView qualityKpis={qualityKpis} />}

        <footer className="footer-note"><span>Source de travail: <strong>dashboard_data.json</strong> + classeur Excel corrigé</span><span>Dernière mise à jour: 22 août 2026 · 88 sessions auditées</span></footer>
      </main>
      {selectedKpi && <div className="modal-backdrop" onClick={() => setSelectedKpi(null)}><div className="kpi-modal" onClick={(e) => e.stopPropagation()}><button className="modal-close" onClick={() => setSelectedKpi(null)} aria-label="Fermer">×</button><div className="kpi-modal-id">{selectedKpi.id} · {selectedKpi.page}</div><h2>{selectedKpi.nom}</h2><div className="modal-value">{selectedKpi.valeur}</div><p><strong>Interprétation :</strong> {selectedKpi.interp || selectedKpi.desc || "Ce KPI est repris du catalogue du dépôt ou calculé de manière dérivée à partir des données des 88 sessions."}</p><p className="modal-support"><strong>Calcul / méthode :</strong> {getKpiCalculation(selectedKpi)}</p>{selectedKpi.util && <p className="modal-support"><strong>Utilité :</strong> {selectedKpi.util}</p>}{selectedKpi.source && <p className="modal-support"><strong>Source :</strong> {selectedKpi.source}</p>}<div className={`catalogue-badge ${selectedKpi.statut}`}>{selectedKpi.statut === "ok" ? "Calculé" : selectedKpi.statut === "warn" ? "Donnée externe" : "À collecter"}</div></div></div>}
    </div>
  );
}

function Overview({ totals, yearlyRows, sectorRows, decisionRows, setView }: { totals: { applications: number; officialApplications: number; detailedEntries: number; labels: number; preLabels: number; accepted: number; sessions: number; averageApplications: number; conversions: number }; yearlyRows: readonly any[]; sectorRows: readonly { name: string; value: number }[]; decisionRows: readonly { name: string; value: number }[]; setView: (view: View) => void }) {
  const cards = [
    { label: "Candidatures corrigées", value: totals.applications, note: "3 555 lignes PDF + 3 ajournés hors PDF · officiel : 3 079", accent: "ink", icon: BookOpen },
    { label: "Labels corrigés PDF", value: totals.labels, note: "Correction : 1 343 · officiel : 1 356", accent: "saffron", icon: CheckCircle2 },
    { label: "Prélabels corrigés PDF", value: totals.preLabels, note: "Correction : 647 · officiel : 641", accent: "moss", icon: Sparkles },
    { label: "Décisions positives corrigées", value: totals.accepted, note: "Labels + Prélabels · série corrigée", accent: "terracotta", icon: BarChart3 },
    { label: "Moyenne candidatures / session", value: fmtDecimal(totals.averageApplications), note: `${fmt(totals.applications)} / ${fmt(totals.sessions)} sessions`, accent: "ink", icon: CalendarDays },
  ];
  return <>
    <section className="hero-strip"><div><div className="section-kicker">SIGNAL PRINCIPAL</div><p>Le dispositif a enregistré <strong>{fmt(totals.accepted)}</strong> décisions positives sur <strong>{fmt(totals.applications)}</strong> candidatures dans le périmètre sélectionné.</p></div><div className="hero-meta"><span>88 SESSIONS</span><span>2019 — 2026</span><span>TRACE EXCEL + JSON</span></div></section>
    <section className="metric-grid">{cards.map(({ label, value, note, accent, icon: Icon }, index) => <div className={`metric-card ${accent}`} key={label}><div className="metric-index">0{index + 1}</div><div className="metric-head"><span>{label}</span><Icon size={18} /></div><div className="metric-value">{typeof value === "number" ? fmt(value) : value}</div><div className="metric-note">{note} · 88 sessions · qualité contrôlée</div><div className="metric-rule" /></div>)}</section>
    <section className="insight-grid"><article className="panel wide-panel"><div className="panel-head"><div><div className="panel-kicker">TRAJECTOIRE</div><h2>La cadence de labellisation s’installe dans le temps</h2></div><button className="text-button" onClick={() => setView("sessions")}>Voir les sessions <ArrowUpRight size={14} /></button></div><div className="chart-wrap"><ResponsiveContainer width="100%" height={300}><LineChart data={yearlyRows as any[]}><CartesianGrid stroke="#D7D0C3" strokeDasharray="3 5" vertical={false} /><XAxis dataKey="year" tick={{ fill: "#667085", fontSize: 12 }} axisLine={false} tickLine={false} /><YAxis tick={{ fill: "#667085", fontSize: 12 }} axisLine={false} tickLine={false} width={36} /><Tooltip contentStyle={{ border: "1px solid #D7D0C3", borderRadius: 4, background: "#FFFDF8", fontSize: 12 }} /><Line type="monotone" dataKey="labels" name="Labels" stroke={INK} strokeWidth={3} dot={{ r: 3, fill: SAFFRON, strokeWidth: 2, stroke: INK }} /><Line type="monotone" dataKey="preLabels" name="Prélabels" stroke={MOSS} strokeWidth={2} dot={false} /></LineChart></ResponsiveContainer></div><div className="chart-legend"><span><i className="legend-dot ink" />Labels accordés</span><span><i className="legend-dot moss" />Prélabels accordés</span></div></article>
      <article className="panel signal-panel"><div className="panel-kicker">COMPOSITION</div><h2>Le parcours positif reste lisible</h2><div className="donut-wrap"><ResponsiveContainer width="100%" height={190}><PieChart><Pie data={[{ name: "Labels", value: totals.labels }, { name: "Prélabels", value: totals.preLabels }]} dataKey="value" innerRadius={54} outerRadius={78} paddingAngle={4}><Cell fill={INK} /><Cell fill={MOSS} /></Pie><Tooltip contentStyle={{ border: "1px solid #D7D0C3", borderRadius: 4, background: "#FFFDF8", fontSize: 12 }} /></PieChart></ResponsiveContainer><div className="donut-center"><strong>{Math.round((totals.labels / Math.max(1, totals.accepted)) * 100)}%</strong><span>Labels</span></div></div><div className="mini-stat"><span>Prélabels dans le positif</span><strong>{Math.round((totals.preLabels / Math.max(1, totals.accepted)) * 100)}%</strong></div></article></section>
    <section className="lower-grid"><article className="panel"><div className="panel-head"><div><div className="panel-kicker">SECTEURS</div><h2>Les cinq verticales les plus visibles</h2></div></div>{sectorRows.length ? <div className="chart-wrap compact"><ResponsiveContainer width="100%" height={240}><BarChart data={sectorRows as any[]} layout="vertical" margin={{ left: 18, right: 12 }}><CartesianGrid stroke="#E4DED4" strokeDasharray="3 5" horizontal={false} /><XAxis type="number" axisLine={false} tickLine={false} tick={{ fill: "#667085", fontSize: 11 }} /><YAxis type="category" dataKey="name" axisLine={false} tickLine={false} width={110} tick={{ fill: INK, fontSize: 11 }} /><Tooltip contentStyle={{ border: "1px solid #D7D0C3", borderRadius: 4, background: "#FFFDF8", fontSize: 12 }} /><Bar dataKey="value" name="Startups" fill={MOSS} radius={[0, 3, 3, 0]} /></BarChart></ResponsiveContainer></div> : <div className="empty-state">La structure sectorielle n’est pas disponible dans le périmètre sélectionné.</div>}</article><article className="panel"><div className="panel-head"><div><div className="panel-kicker">INDICATEURS DE PARCOURS</div><h2>Les statuts publiés restent distincts</h2></div></div><div className="chart-wrap compact"><ResponsiveContainer width="100%" height={240}><BarChart data={decisionRows as any[]} layout="vertical" margin={{ left: 18, right: 12 }}><CartesianGrid stroke="#E4DED4" strokeDasharray="3 5" horizontal={false} /><XAxis type="number" axisLine={false} tickLine={false} tick={{ fill: "#667085", fontSize: 11 }} /><YAxis type="category" dataKey="name" axisLine={false} tickLine={false} width={145} tick={{ fill: INK, fontSize: 10 }} /><Tooltip contentStyle={{ border: "1px solid #D7D0C3", borderRadius: 4, background: "#FFFDF8", fontSize: 12 }} /><Bar dataKey="value" name="Occurrences sessionnelles" fill={SAFFRON} radius={[0, 3, 3, 0]} /></BarChart></ResponsiveContainer></div></article></section>
    <section className="insight-grid"><article className="panel wide-panel"><div className="panel-head"><div><div className="panel-kicker">LECTURE AVANCÉE · PÉRIMÈTRE ACTIF</div><h2>Le parcours institutionnel et documentaire ne sont pas la même unité</h2></div><button className="text-button" onClick={() => setView("study")}>Méthode <ArrowUpRight size={14} /></button></div><div className="funnel-grid"><div className="funnel-step"><span>Officiel</span><strong>{fmt(totals.officialApplications)}</strong><small>compteurs publiés</small></div><div className="funnel-step corrected"><span>PDF détaillé</span><strong>{fmt(totals.detailedEntries)}</strong><small>lignes extraites</small></div><div className="funnel-step accent"><span>Corrigé</span><strong>{fmt(totals.applications)}</strong><small>PDF + ajournés hors PDF</small></div><div className="funnel-step moss"><span>Conversions</span><strong>{fmt(totals.conversions)}</strong><small>ne pas recompter comme candidature</small></div></div></article><article className="panel notes-panel"><div className="panel-kicker">GARDE-FOU</div><h2>Une page, plusieurs lectures</h2><div className="note-row"><ShieldCheck size={16} /><span>Le Dashboard rassemble désormais les meilleurs graphiques du registre et de l’analyse avancée.</span></div><div className="note-row"><AlertTriangle size={16} /><span>S62 conserve 39 candidatures officielles contre 46 enregistrements PDF documentaires.</span></div><div className="note-row"><Table2 size={16} /><span>Les 3 ajournés hors PDF sont distincts des candidatures reportées.</span></div></article>    </section>
  </>;
}

function SessionsView({ sessions }: { sessions: ReturnType<typeof normalizeSession>[] }) {
  return <section className="content-stack"><div className="view-intro"><div><div className="section-kicker">REGISTRE SESSIONNEL</div><p>La vue principale utilise la série corrigée : 3 555 lignes PDF documentaires complétées par 3 ajournés hors PDF explicitement signalés ; elles constituent la mesure corrigée de l’étude. Le compteur officiel publié par session reste affiché séparément pour comparaison. Le classeur 1–88 confirme les volumes des huit sessions signalées ; ses champs individuels incomplets ne remplacent pas les informations PDF contrôlées.</p></div><div className="source-stamp large"><Database size={15} /><span>{sessions.length} sessions visibles</span></div></div><div className="report-legend"><span>3 558 candidatures corrigées · 3 555 lignes PDF + 3 ajournés hors PDF · officiel : 3 079</span><span className="report-legend-note">Volumes Excel confirmés : S16 · S19 · S24 · S28 · S30 · S33 · S46 · S62</span></div><div className="report-legend"><span className="report-legend-note">S62 : 39 candidatures / 46 entrées = 39 lignes du bloc + 5 conversions + 2 retraits</span></div><div className="report-legend"><span className="report-legend-note">Ajournés hors PDF : 03/2019 (+2) et 06/2019 (+1), noms d’entreprises non identifiés dans les commentaires disponibles</span></div><div className="panel session-chart"><ResponsiveContainer width="100%" height={340}><BarChart data={sessions}><CartesianGrid stroke="#E4DED4" strokeDasharray="3 5" vertical={false} /><XAxis dataKey="id" interval={Math.max(0, Math.floor(sessions.length / 14))} tick={{ fill: "#667085", fontSize: 11 }} axisLine={false} tickLine={false} /><YAxis axisLine={false} tickLine={false} tick={{ fill: "#667085", fontSize: 11 }} /><Tooltip contentStyle={{ border: "1px solid #D7D0C3", borderRadius: 4, background: "#FFFDF8", fontSize: 12 }} /><Legend /><Bar dataKey="labelsCorriges" name="Labels corrigés PDF" stackId="a" fill={INK} /><Bar dataKey="preLabelsCorriges" name="Prélabels corrigés PDF" stackId="a" fill={SAFFRON} /></BarChart></ResponsiveContainer></div><div className="panel table-panel"><div className="report-legend"><span className="report-key" aria-hidden="true" /> Ligne avec candidature reportée <span className="report-legend-note">02/2020 · 03/2020 · 07/2021 · 09/2021 · 10/2024</span></div><div className="table-scroll"><table><thead><tr><th>Session</th><th>Période</th><th>Candidatures officiel</th><th>Candidatures corrigé</th><th>Ajournés hors PDF</th><th>Labels officiel</th><th>Labels corrigé</th><th>Prélabels officiel</th><th>Prélabels corrigé</th><th>Reportés</th><th>Taux</th><th>Statut</th></tr></thead><tbody>{sessions.map((s) => { const isReport = REPORT_SESSIONS.has(s.id); return <tr key={s.id} className={isReport ? "report-row" : undefined}><td className="strong-cell">{s.id}</td><td>{s.month}/{s.year}</td><td>{fmt(Number(s.candidaturesOfficielles || 0))}</td><td className="corrected-cell">{fmt(Number(s.candidaturesCorrigees || 0))}</td><td className={Number(s.ajournesHorsPdf || 0) > 0 ? "deferred-cell" : undefined}>{fmt(Number(s.ajournesHorsPdf || 0))}</td><td><span className="table-number ink-text">{fmt(Number(s.labelsOfficiels || 0))}</span></td><td className="corrected-cell"><span className="table-number ink-text">{fmt(Number(s.labelsCorriges || 0))}</span></td><td><span className="table-number saffron-text">{fmt(Number(s.preLabelsOfficiels || 0))}</span></td><td className="corrected-cell"><span className="table-number saffron-text">{fmt(Number(s.preLabelsCorriges || 0))}</span></td><td>{fmt(Number(s.reportes || 0))}</td><td>{s.rate.toFixed(1)}%</td><td>{isReport ? <span className="report-badge">Reporté</span> : <span className="status-empty">—</span>}</td></tr>; })}</tbody></table></div></div></section>;
}

function StudyView({ sessions }: { sessions: ReturnType<typeof normalizeSession>[] }) {
  const official = sessions.reduce((sum, s) => sum + Number(s.candidaturesOfficielles || 0), 0);
  const pdf = sessions.reduce((sum, s) => sum + Number(s.detailedEntries || s.entries || 0), 0);
  const corrected = sessions.reduce((sum, s) => sum + Number(s.candidaturesCorrigees || 0), 0);
  const ajournes = sessions.reduce((sum, s) => sum + Number(s.ajournesHorsPdf || 0), 0);
  const reportes = sessions.reduce((sum, s) => sum + Number(s.reportes || 0), 0);
  return <section className="content-stack"><div className="view-intro"><div><div className="section-kicker">ÉTUDE QUANTITATIVE · NOTE MÉTHODOLOGIQUE</div><p>Cette étude ne force pas un chiffre unique lorsque les sources ne mesurent pas la même unité. Elle conserve le compteur institutionnel, le détail PDF et la série corrigée dans trois colonnes séparées.</p></div><div className="source-stamp large"><BookOpen size={15} /><span>{sessions.length} sessions dans le périmètre</span></div></div><div className="method-grid"><article className="panel method-card"><div className="panel-kicker">01 · COMPTEUR OFFICIEL</div><strong>{fmt(official)}</strong><p>Somme des candidatures publiées sur startup.gov.tn. Ce chiffre est reproduit comme série institutionnelle, même lorsqu’une session présente une discordance avec les lignes du PDF.</p></article><article className="panel method-card"><div className="panel-kicker">02 · LIGNES PDF</div><strong>{fmt(pdf)}</strong><p>Somme des enregistrements documentaires extraits des 88 comptes-rendus. Une ligne peut représenter une conversion, un retrait ou un dossier administratif sans décision précisée.</p></article><article className="panel method-card"><div className="panel-kicker">03 · SÉRIE CORRIGÉE</div><strong>{fmt(corrected)}</strong><p>Mesure de travail retenue pour l’analyse détaillée : lignes PDF contrôlées, plus {fmt(ajournes)} ajournés hors PDF identifiés en 03/2019 et 06/2019.</p></article></div><article className="panel provenance-panel"><div className="panel-kicker">PÉRIMÈTRES ET RÈGLES DE COMPTAGE</div><h2>Pourquoi les trois séries doivent rester visibles</h2><p>Une candidature est un dossier présenté au dispositif ; une ligne PDF est une trace documentaire. La relation « lignes moins reportés » n’est donc pas universelle. Dans S62 (05/2024), le PDF contient 46 enregistrements : 39 candidatures du bloc principal, 5 conversions Prélabel → Label et 2 retraits. Les 4 dossiers portant le motif administratif de non-présentation des états financiers restent des candidatures documentées, mais avec une décision non précisée ; ils ne sont ni supprimés ni transformés en Reporté. Les {fmt(reportes)} candidatures Reporté sont signalées séparément dans la vue Sessions, car elles peuvent apparaître dans une session de départ et revenir dans une session ultérieure.</p><div className="report-legend"><span>Ajourné = décision différée dans le compteur corrigé, hors PDF identifié.</span><span>Reporté = candidature explicitement renvoyée à une session ultérieure.</span></div></article><article className="panel provenance-panel"><div className="panel-kicker">LIMITES ET REPRODUCTIBILITÉ</div><h2>Ce qui est vérifiable et ce qui doit rester prudent</h2><p>Les agrégats par session, les décisions publiées et les écarts de périmètre sont recalculés depuis le JSON canonique synchronisé avec les exports Excel, CSV et SQL. Les noms de startups et de fondateurs issus de l’OCR ou de l’extraction automatique peuvent comporter des approximations ; ils ne doivent pas être utilisés comme preuve supérieure au PDF source. Toute correction manuelle conserve son statut, son motif et sa provenance afin d’être auditée séparément.</p></article></section>;
}

function CatalogueView({ catalogue, query, setQuery, onSelect }: { catalogue: readonly KpiRow[]; query: string; setQuery: (q: string) => void; onSelect: (kpi: KpiRow) => void }) {
  return <section className="content-stack"><div className="view-intro"><div><div className="section-kicker">CATALOGUE DE MESURE</div><p>Les 50 KPI du catalogue sont vérifiés sur la série canonique des 88 sessions; les dérivés et les données externes restent explicitement signalés.</p></div><div className="kpi-count-badge"><strong>{dashboardData.kpis.length}</strong><span>KPI catalogués</span></div></div><div className="search-row"><div className="search-box"><Search size={16} /><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Rechercher un KPI, une page, un thème…" /></div><span className="filter-label"><Filter size={14} /> {catalogue.length} résultats</span></div><div className="kpi-catalogue-grid">{catalogue.map((kpi) => <button className={`catalogue-card ${kpi.statut}`} key={kpi.id} onClick={() => onSelect(kpi)}><div className="catalogue-card-top"><span className="kpi-id">{kpi.id}</span><span className={`catalogue-badge ${kpi.statut}`}>{kpi.statut === "ok" ? "Calculé" : kpi.statut === "warn" ? "Externe" : "Manquant"}</span></div><h3>{kpi.nom}</h3><div className="catalogue-value">{kpi.valeur}</div><div className="catalogue-meta">{kpi.page}<ChevronRight size={13} /></div></button>)}</div></section>;
}

function QualityView({ qualityKpis }: { qualityKpis: readonly KpiRow[] }) {
  return <section className="content-stack"><div className="view-intro"><div><div className="section-kicker">PROVENANCE & QUALITÉ</div><p>Une vue de contrôle pour distinguer les indicateurs calculés, externes et à collecter.</p></div><div className="quality-summary"><span><i className="quality-dot ok" /> calculés</span><span><i className="quality-dot warn" /> externes</span><span><i className="quality-dot miss" /> à collecter</span></div></div><div className="quality-grid">{qualityKpis.map((kpi) => <article className="quality-card" key={kpi.id}><div className="kpi-id">{kpi.id}</div><h2>{kpi.nom}</h2><p>{kpi.valeur}</p><div className={`catalogue-badge ${kpi.statut}`}>{kpi.statut === "warn" ? "Donnée externe" : "À collecter"}</div></article>)}</div><div className="panel provenance-panel"><div className="panel-kicker">MÉTHODE</div><h2>Les chiffres ne sont pas tous du même type</h2><p>Les compteurs Labels et Prélabels sont issus des 88 sessions. Les KPI géographiques, économiques ou de propriété intellectuelle peuvent dépendre de rapports externes. Le statut reste affiché pour éviter de confondre une donnée calculée et une donnée à actualiser.</p></div><div className="panel provenance-panel"><div className="panel-kicker">CORRECTION S62 · 05/2024</div><h2>39 candidatures, 46 enregistrements documentaires</h2><p>Le PDF officiel distingue 39 candidatures du bloc principal, 5 conversions historiques visibles dans le détail et 2 retraits. Les enregistrements détaillés ne doivent donc pas être transformés mécaniquement en candidatures par la formule « entries − reportés ». À l’échelle du corpus, le dashboard affiche 3 555 lignes PDF, 3 ajournés hors PDF (03/2019 : 2 ; 06/2019 : 1) et donc 3 558 candidatures corrigées, face aux 3 079 candidatures officielles. Les ajournés hors PDF sont conservés sans nom d’entreprise, car le commentaire source ne permet pas une identification fiable. Les cinq reports confirmés sont signalés en terracotta dans le tableau : Tunisia Biotech (02/2020), Campus Numérique des métiers (03/2020), TN Smartbot (07/2021), SHYK (09/2021, Reporté documenté dans S30) et RYBSEN (10/2024, reporté à novembre 2024). Les 45 faux positifs historiques S17–S20 ont été reclassés ; ITMMA (06/2024) reste un pitch décalé et n’est pas une candidature Reporté.</p></div></section>;
}
