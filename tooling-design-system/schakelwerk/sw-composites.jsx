/* Schakelwerk domain composites — built from sw-components atoms + Tooling DS.
 * These are the trust-story components: AuditEntryRow, ProposalCard,
 * CalculationSnapshotCard, CostSummaryPanel, plus the pickers.
 */

const SWC = {};

/* ───────────────────────── Customer / Project pickers ───────────────────────── */

SWC.CustomerPicker = function CustomerPicker({ value, open = false }) {
  return (
    <div style={{ position: "relative", width: 320 }}>
      <div className={`sw-input ${open ? "is-focus" : ""}`}>
        <I.Building size={14}/>
        <span className="val left" style={{ textAlign: "left", fontFamily: "var(--font-sans)" }}>
          {value || <span style={{ color: "var(--color-muted-2)" }}>Search customers…</span>}
        </span>
        <I.Chevron size={14}/>
      </div>
      {open && (
        <div style={{
          position: "absolute", top: "calc(100% + 4px)", left: 0, right: 0,
          background: "var(--color-bg-elev)",
          border: "var(--hairline) solid var(--color-border-strong)",
          borderRadius: 8,
          boxShadow: "var(--shadow-md), var(--hairline-highlight)",
          padding: 4, zIndex: 5,
          fontSize: 13,
        }}>
          {[
            { name: "Bouwbedrijf Van Dijk", id: "cust-018", projects: 4 },
            { name: "Aannemingsmij De Boer", id: "cust-022", projects: 2 },
            { name: "Installatie Jansen B.V.", id: "cust-007", projects: 1 },
          ].map((c, i) => (
            <div key={c.id} style={{
              display: "grid", gridTemplateColumns: "1fr max-content",
              padding: "8px 10px", borderRadius: 6,
              background: i === 0 ? "var(--color-card-2)" : "transparent",
              cursor: "pointer", gap: 8, alignItems: "center"
            }}>
              <div>
                <div style={{ fontWeight: 500 }}>{c.name}</div>
                <div style={{ fontSize: 11, color: "var(--color-muted)", fontFamily: "var(--font-mono)" }}>{c.id}</div>
              </div>
              <span className="sw-pill">{c.projects} projects</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

SWC.ProjectPicker = function ProjectPicker({ value, open = false }) {
  const items = [
    { name: "Renovatie Stationsplein", cust: "Bouwbedrijf Van Dijk", id: "prj-114", rule: "v3", status: "ACTIVE" },
    { name: "Onderhoud Distributielocatie A", cust: "Aannemingsmij De Boer", id: "prj-097", rule: null, status: "DRAFT" },
    { name: "Installatie Centrum Zuid",  cust: "Installatie Jansen B.V.", id: "prj-088", rule: "v1", status: "PAUSED" },
  ];
  return (
    <div style={{ position: "relative", width: 380 }}>
      <div className={`sw-input ${open ? "is-focus" : ""}`}>
        <I.Layers size={14}/>
        <span className="val left" style={{ textAlign: "left", fontFamily: "var(--font-sans)" }}>
          {value || <span style={{ color: "var(--color-muted-2)" }}>Pick a project…</span>}
        </span>
        <I.Chevron size={14}/>
      </div>
      {open && (
        <div style={{
          position: "absolute", top: "calc(100% + 4px)", left: 0, right: 0,
          background: "var(--color-bg-elev)",
          border: "var(--hairline) solid var(--color-border-strong)",
          borderRadius: 8,
          boxShadow: "var(--shadow-md), var(--hairline-highlight)",
          padding: 4, zIndex: 5,
          fontSize: 13,
        }}>
          {items.map((p, i) => (
            <div key={p.id} style={{
              display: "grid", gridTemplateColumns: "1fr max-content max-content",
              padding: "8px 10px", borderRadius: 6,
              background: i === 0 ? "var(--color-card-2)" : "transparent",
              cursor: "pointer", gap: 10, alignItems: "center"
            }}>
              <div style={{ minWidth: 0 }}>
                <div style={{ fontWeight: 500, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{p.name}</div>
                <div style={{ fontSize: 11, color: "var(--color-muted)" }}>{p.cust} · <span style={{ fontFamily: "var(--font-mono)" }}>{p.id}</span></div>
              </div>
              {p.rule
                ? <span className="sw-pill info">rule {p.rule}</span>
                : <span className="sw-pill warn">no rule</span>}
              <StatusBadge namespace="project" value={p.status} showNs={false}/>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

SWC.WorkerIdField = function WorkerIdField({ value }) {
  return (
    <div style={{ width: 320 }}>
      <Field label="Worker ID" hint="Opaque string. No user-directory lookup — recent values are remembered locally.">
        <div className="sw-input">
          <I.Search size={14}/>
          <span className="val left" style={{ fontFamily: "var(--font-mono)", textAlign: "left" }}>{value}</span>
          {value && <Identicon id={value} size="sm"/>}
        </div>
      </Field>
      <div style={{ display: "flex", gap: 4, marginTop: 6, flexWrap: "wrap" }}>
        <span style={{ fontSize: 10, color: "var(--color-muted)", letterSpacing: "0.06em", textTransform: "uppercase", marginRight: 4 }}>Recent</span>
        {["w-42", "w-115", "w-007", "w-86"].map((id) => (
          <span key={id} className="sw-pill"><Identicon id={id} size="sm"/>{id}</span>
        ))}
      </div>
    </div>
  );
};

SWC.SessionTypeSelector = function SessionTypeSelector({ value = "ON_SITE", lg = true }) {
  return (
    <Segmented
      size={lg ? "lg" : "md"}
      full={lg}
      value={value}
      options={[
        { value: "TRAVEL",  label: "Travel",   icon: <I.ArrowLeftRight size={lg ? 16 : 14}/> },
        { value: "ON_SITE", label: "On site",  icon: <I.Building       size={lg ? 16 : 14}/> },
      ]}
    />
  );
};

/* ───────────────────────── ReasonPrompt — re-export from sw-components ───────────────────────── */

SWC.ReasonPrompt = ReasonPrompt;

/* ───────────────────────── RuleParamsForm fragment ───────────────────────── */

SWC.RuleParamsForm = function RuleParamsForm() {
  return (
    <div className="sw-stack-4">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h3 style={{ fontSize: 14 }}>Rule params · draft</h3>
          <div style={{ fontSize: 11, color: "var(--color-muted)" }}>Publishing creates rule v4. Old versions remain referenced by closed sessions.</div>
        </div>
        <span className="sw-pill warn">unpublished draft</span>
      </div>
      <hr className="sw-divider"/>
      <Field label="Travel rate · per minute" hint="Stored as integer cents. Engine expects min ≥ 1.">
        <CurrencyInput cents={42}/>
      </Field>
      <Field label="On-site rate · per minute">
        <CurrencyInput cents={75}/>
      </Field>
      <Field label="Daily unbillable lunch deduction"
             hint="Engine subtracts this from on-site duration before billing."
             audit>
        <DurationInput minutes={30}/>
      </Field>
      <Field label="Round to nearest">
        <Segmented value="5"
          options={[
            { value: "1",  label: "1 min" },
            { value: "5",  label: "5 min" },
            { value: "15", label: "15 min" },
          ]}/>
      </Field>
      <div style={{
        display: "flex", gap: 8, padding: "10px 12px",
        background: "var(--color-warn-soft)", borderRadius: 6, fontSize: 12, color: "var(--color-warn)"
      }}>
        <I.Alert size={14}/> Publish creates a new version. Sessions closed before publish keep rule v3.
      </div>
      <div style={{ display: "flex", gap: 6, justifyContent: "flex-end" }}>
        <Button variant="ghost">Discard draft</Button>
        <Button variant="primary">Publish v4</Button>
      </div>
    </div>
  );
};

/* ───────────────────────── CalculationSnapshotCard ─────────────────────────
 * Renders the deterministic engine output: engine_version, rule_version,
 * inputs, ordered steps, output.
 */
SWC.CalculationSnapshotCard = function CalculationSnapshotCard() {
  const snapshot = {
    engine_version: "calc-engine 2.4.1",
    rule_version: "rule:prj-114:v3",
    inputs: {
      worker_id: "w-42",
      session_type: "ON_SITE",
      clock_in_utc:  "2026-05-24T07:32:00Z",
      clock_out_utc: "2026-05-24T15:02:00Z",
    },
    steps: [
      { i: 1, op: "duration_minutes",          out: 450 },
      { i: 2, op: "subtract_lunch_deduction",  in_: 450, by: 30, out: 420 },
      { i: 3, op: "round_to_5min",             in_: 420, out: 420 },
      { i: 4, op: "rate · 75c/min",            in_: 420, out: 31500 },
    ],
    output: { billable_minutes: 420, nonbillable_minutes: 30, total_cents: 31500 },
  };
  return (
    <div className="card" style={{ padding: 0 }}>
      <div className="card-head">
        <div>
          <h3>Calculation snapshot</h3>
          <div className="sub">Deterministic. Same inputs + same versions → same output, forever.</div>
        </div>
        <div className="actions">
          <span className="sw-pill"><I.Refresh size={10}/> immutable</span>
        </div>
      </div>
      <div className="card-body" style={{ padding: 20 }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, fontSize: 12 }}>
          <div>
            <div className="sw-eyebrow">Engine</div>
            <div style={{ fontFamily: "var(--font-mono)", marginTop: 4 }}>{snapshot.engine_version}</div>
          </div>
          <div>
            <div className="sw-eyebrow">Rule</div>
            <div style={{ fontFamily: "var(--font-mono)", marginTop: 4 }}>{snapshot.rule_version}</div>
          </div>
        </div>
        <hr className="sw-divider" style={{ margin: "14px 0" }}/>
        <div className="sw-eyebrow" style={{ marginBottom: 8 }}>Steps</div>
        <ol style={{ listStyle: "none", padding: 0, margin: 0, fontFamily: "var(--font-mono)", fontSize: 11.5 }}>
          {snapshot.steps.map((s) => (
            <li key={s.i} style={{
              display: "grid", gridTemplateColumns: "20px 1fr max-content",
              gap: 8, padding: "6px 0",
              backgroundImage: "var(--grad-divider)", backgroundRepeat: "no-repeat",
              backgroundPosition: "bottom", backgroundSize: "100% var(--hairline)"
            }}>
              <span style={{ color: "var(--color-muted)" }}>{s.i}.</span>
              <span style={{ color: "var(--color-fg-2)" }}>
                {s.op}
                {s.in_ != null && <span style={{ color: "var(--color-muted)" }}>  in={s.in_}</span>}
                {s.by  != null && <span style={{ color: "var(--color-muted)" }}>  by={s.by}</span>}
              </span>
              <span style={{ color: "var(--color-fg)" }}>→ {s.out}</span>
            </li>
          ))}
        </ol>
        <hr className="sw-divider" style={{ margin: "14px 0" }}/>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10 }}>
          <StatTile label="Billable" value={<span style={{ fontFamily: "var(--font-mono)", fontSize: 22 }}>{fmtDuration(420)}</span>}/>
          <StatTile label="Non-billable" value={<span style={{ fontFamily: "var(--font-mono)", fontSize: 22, color: "var(--color-muted)" }}>+{fmtDuration(30)}</span>}/>
          <StatTile label="Total" cents={31500}/>
        </div>
      </div>
    </div>
  );
};

/* ───────────────────────── ProposalCard ─────────────────────────
 * Proposals do NOT mutate canonical state. Approve/Reject is the boundary.
 */
SWC.ProposalCard = function ProposalCard() {
  const diff = [
    { kind: " ", text: '"session_id": "ses-3098",', indent: 1 },
    { kind: "-", text: '"clock_out_utc": "2026-05-24T15:02:00Z",', indent: 1 },
    { kind: "+", text: '"clock_out_utc": "2026-05-24T15:48:00Z",', indent: 1 },
    { kind: "-", text: '"billable_minutes": 420,', indent: 1 },
    { kind: "+", text: '"billable_minutes": 466,', indent: 1 },
    { kind: "-", text: '"total_cents": 31500', indent: 1 },
    { kind: "+", text: '"total_cents": 34950', indent: 1 },
  ];
  return (
    <div className="sw-proposal sw-stack-4">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 10 }}>
        <div>
          <span className="sw-proposal-tag"><I.Star size={10}/> automation proposal · clock_out_correction</span>
          <h3 style={{ fontSize: 14, marginTop: 6 }}>Late clock-out detected from gate-scan capture</h3>
          <div style={{ fontSize: 12, color: "var(--color-muted)", marginTop: 4 }}>
            Session <span style={{ fontFamily: "var(--font-mono)" }}>ses-3098</span> · worker <span style={{ fontFamily: "var(--font-mono)" }}>w-42</span> · Renovatie Stationsplein
          </div>
        </div>
        <StatusBadge namespace="proposal" value="PENDING"/>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
        <div className="sw-tile">
          <div className="lbl">Confidence</div>
          <div className="sw-conf" style={{ marginTop: 8 }}>
            <span className="bar"><i style={{ width: "82%" }}/></span>
            <span>82%</span>
          </div>
          <div className="sub" style={{ marginTop: 4 }}>capture: gate_scan · proc 2026-05-24T16:12Z</div>
        </div>
        <div className="sw-tile">
          <div className="lbl">Cost delta · if approved</div>
          <div className="val"><span className="cur">€</span>+34,50</div>
          <div className="sub">+46m billable · rule v3</div>
        </div>
      </div>

      <div>
        <div className="sw-eyebrow" style={{ marginBottom: 6 }}>Rationale</div>
        <div style={{ fontSize: 12, color: "var(--color-fg-2)", lineHeight: 1.5 }}>
          Gate-scan event at 15:48Z matches worker w-42 on site prj-114; logged clock_out was 15:02Z. Capture confidence raised because two independent scanners agreed within 90s.
        </div>
      </div>

      <DiffViewer
        title="canonical → proposed"
        subtitle="work_sessions/ses-3098"
        rows={diff}/>

      <div className="sw-alert info" style={{ fontSize: 12 }}>
        <span className="ico"><I.Info size={14}/></span>
        <div>
          <b>Proposal is read-only.</b>
          <p>Canonical state is unchanged until you Approve. Rejecting writes a permanent audit_entry.</p>
        </div>
      </div>

      <div style={{ display: "flex", justifyContent: "flex-end", gap: 6 }}>
        <Button variant="ghost">View source capture</Button>
        <Button variant="secondary">Reject</Button>
        <Button variant="primary"><I.Check size={14}/> Approve · writes audit</Button>
      </div>
    </div>
  );
};

/* ───────────────────────── AuditEntryRow ───────────────────────── */

SWC.AuditEntryRow = function AuditEntryRow({ expanded = false }) {
  return (
    <div className="sw-card flush">
      <div style={{
        display: "grid", gridTemplateColumns: "36px 1fr max-content max-content",
        gap: 10, padding: "12px 14px", alignItems: "center",
        backgroundImage: expanded ? "var(--grad-divider)" : "none",
        backgroundRepeat: "no-repeat", backgroundPosition: "bottom",
        backgroundSize: "100% var(--hairline)",
        cursor: "pointer", fontSize: 12,
      }}>
        <Identicon id="admin-7"/>
        <div style={{ minWidth: 0 }}>
          <div style={{ display: "flex", gap: 6, alignItems: "center" }}>
            <b>admin-7</b>
            <span className="sw-pill info" style={{ fontSize: 10 }}>APPROVE_PROPOSAL</span>
            <span style={{ color: "var(--color-muted)" }}>on</span>
            <span style={{ fontFamily: "var(--font-mono)", fontSize: 11 }}>work_sessions/ses-3098</span>
          </div>
          <div style={{ marginTop: 3, fontSize: 11, color: "var(--color-muted)" }}>
            “Gate-scan correction confirmed by ops manager.”
          </div>
        </div>
        <DateTimeDisplay iso="2026-05-24T17:04:22Z" tz="UTC" rel="14m ago"/>
        <Button variant="ghost" size="sm">
          {expanded ? <I.Chevron size={12}/> : <I.ChevronRight size={12}/>}
        </Button>
      </div>
      {expanded && (
        <div style={{ padding: 14 }}>
          <div className="sw-eyebrow" style={{ marginBottom: 6 }}>Effective diff</div>
          <DiffViewer rows={[
            { kind: " ", text: '"session_id": "ses-3098",', indent: 1 },
            { kind: "-", text: '"clock_out_utc": "2026-05-24T15:02:00Z",', indent: 1 },
            { kind: "+", text: '"clock_out_utc": "2026-05-24T15:48:00Z",', indent: 1 },
            { kind: " ", text: '"status": "APPROVED",', indent: 1 },
          ]}/>
          <div className="sw-eyebrow" style={{ marginTop: 12, marginBottom: 6 }}>Provenance</div>
          <dl className="sw-kv">
            <dt>audit_id</dt><dd>aud-90211</dd>
            <dt>parent_proposal</dt><dd>prop-1408</dd>
            <dt>engine_revision</dt><dd>calc-engine 2.4.1</dd>
            <dt>rule_version</dt><dd>rule:prj-114:v3</dd>
            <dt>request_id</dt><dd>req-c4f1…</dd>
          </dl>
        </div>
      )}
    </div>
  );
};

/* ───────────────────────── CostSummaryPanel ───────────────────────── */

SWC.CostSummaryPanel = function CostSummaryPanel() {
  return (
    <div className="card" style={{ padding: 0 }}>
      <div className="card-head">
        <div>
          <h3>Cost summary</h3>
          <div className="sub">Renovatie Stationsplein · period 2026-05-01 → 2026-05-24 · UTC</div>
        </div>
        <div className="actions">
          <span className="sw-pill">rule v3</span>
        </div>
      </div>
      <div className="card-body" style={{ padding: 20, display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: 10 }}>
        <StatTile label="Budget"   cents={450000} sub="locked at project start"/>
        <StatTile label="Actual" noRate sub="travel rate missing for w-115"/>
        <StatTile label="Billable" value={<span style={{ fontFamily: "var(--font-mono)", fontSize: 22 }}>{fmtDuration(2820)}</span>} sub="47 sessions · 12 workers"/>
        <StatTile label="Non-bill." value={<span style={{ fontFamily: "var(--font-mono)", fontSize: 22, color: "var(--color-muted)" }}>+{fmtDuration(420)}</span>} sub="lunch + travel idle"/>
      </div>
      <div style={{ padding: "0 20px 20px" }}>
        <div className="sw-alert warn">
          <span className="ico"><I.Alert size={14}/></span>
          <div>
            <b>Actual total is intentionally not shown.</b>
            <p>One or more sessions reference a worker without a configured travel rate. Configure the rate on the worker rule, or exclude those sessions from this period.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

window.SWC = SWC;
