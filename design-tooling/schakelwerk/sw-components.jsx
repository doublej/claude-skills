/* Schakelwerk components — built on top of the Tooling DS (Button, Badge,
 * Money, Card, DataTable already exist on window). This file adds the
 * Schakelwerk-specific atoms + utilities the canvas pulls in.
 */

const { useState, useMemo, useEffect } = React;

/* ───────────────────────── Utilities ───────────────────────── */

// Money — cents in, Dutch euro string out. Float-free; integer cents arithmetic only.
function fmtMoneyCents(cents, { withSymbol = true } = {}) {
  if (cents == null) return "—";
  const neg = cents < 0;
  const abs = Math.abs(cents);
  const euros = Math.trunc(abs / 100);
  const remainder = abs - euros * 100;
  // Dutch formatting: thousand-separator ".", decimal ",", e.g. 4.500,00
  const eurosStr = String(euros).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  const centsStr = String(remainder).padStart(2, "0");
  const body = `${eurosStr},${centsStr}`;
  return `${neg ? "−" : ""}${withSymbol ? "€ " : ""}${body}`;
}

// Duration — minutes in, "7h 30m" out.
function fmtDuration(minutes, { compact = false } = {}) {
  if (minutes == null) return "—";
  const neg = minutes < 0;
  const m = Math.abs(minutes);
  const h = Math.floor(m / 60);
  const rem = m - h * 60;
  if (compact) return `${neg ? "−" : ""}${h}:${String(rem).padStart(2, "0")}`;
  if (h === 0) return `${neg ? "−" : ""}${rem}m`;
  if (rem === 0) return `${neg ? "−" : ""}${h}h`;
  return `${neg ? "−" : ""}${h}h ${String(rem).padStart(2, "0")}m`;
}

/* ───────────────────────── Status registry ─────────────────────────
 * Five namespaces. Same label can mean different things across them —
 * the registry forces a `(namespace, label)` lookup at the call site,
 * never just a `label`.
 */
const STATUS = {
  work_session: {
    OPEN:                { tone: "open",      label: "OPEN",       ico: "play" },
    CLOSED:              { tone: "closed",    label: "CLOSED",     ico: "stop" },
    CORRECTION_PROPOSED: { tone: "proposed",  label: "CORRECTION_PROPOSED", ico: "alert" },
    APPROVED:            { tone: "approved",  label: "APPROVED",   ico: "check" },
    REJECTED:            { tone: "rejected",  label: "REJECTED",   ico: "x" },
  },
  proposal: {
    PENDING:  { tone: "pending",  label: "PENDING",  ico: "clock" },
    APPROVED: { tone: "approved", label: "APPROVED", ico: "check" },
    REJECTED: { tone: "rejected", label: "REJECTED", ico: "x" },
  },
  bookkeeping: {
    DRAFT:    { tone: "draft",    label: "DRAFT",    ico: "doc" },
    READY:    { tone: "ready",    label: "READY",    ico: "send" },
    EXPORTED: { tone: "exported", label: "EXPORTED", ico: "check" },
    FAILED:   { tone: "failed",   label: "FAILED",   ico: "alert" },
  },
  capture: {
    RECEIVED:  { tone: "received",  label: "RECEIVED",  ico: "inbox" },
    PROCESSED: { tone: "processed", label: "PROCESSED", ico: "check" },
    SKIPPED:   { tone: "skipped",   label: "SKIPPED",   ico: "skip" },
    FAILED:    { tone: "failed",    label: "FAILED",    ico: "alert" },
  },
  project: {
    DRAFT:     { tone: "draft",     label: "DRAFT",     ico: "doc" },
    ACTIVE:    { tone: "active",    label: "ACTIVE",    ico: "circle" },
    PAUSED:    { tone: "paused",    label: "PAUSED",    ico: "pause" },
    COMPLETED: { tone: "completed", label: "COMPLETED", ico: "check" },
    ARCHIVED:  { tone: "archived",  label: "ARCHIVED",  ico: "archive" },
  },
};

const SVG = (paths) => (
  <svg className="ico" width="12" height="12" viewBox="0 0 24 24" fill="none"
       stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    {paths}
  </svg>
);
const StatusIco = {
  play:    <path d="M6 4l14 8-14 8z"/>,
  stop:    <rect x="6" y="6" width="12" height="12" rx="1"/>,
  alert:   <><circle cx="12" cy="12" r="9"/><path d="M12 8v4M12 16h.01"/></>,
  check:   <polyline points="20 6 9 17 4 12"/>,
  x:       <><path d="M18 6L6 18"/><path d="M6 6l12 12"/></>,
  clock:   <><circle cx="12" cy="12" r="9"/><path d="M12 8v4l3 2"/></>,
  doc:     <><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6"/></>,
  send:    <><path d="M22 2 11 13"/><path d="M22 2l-7 20-4-9-9-4z"/></>,
  inbox:   <><path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></>,
  skip:    <><polygon points="5 4 15 12 5 20 5 4"/><line x1="19" y1="5" x2="19" y2="19"/></>,
  circle:  <circle cx="12" cy="12" r="4" fill="currentColor"/>,
  pause:   <><rect x="6" y="5" width="4" height="14"/><rect x="14" y="5" width="4" height="14"/></>,
  archive: <><rect x="2" y="3" width="20" height="5"/><path d="M4 8v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8"/><path d="M10 12h4"/></>,
};

function StatusBadge({ namespace, value, showNs = true, mono = false }) {
  const def = STATUS[namespace]?.[value];
  if (!def) return <span className="sw-stat">{namespace}:{value}</span>;
  return (
    <span className={`sw-stat sw-stat-${def.tone}`}>
      {showNs && <span className="ns">{namespace}</span>}
      <span className="dot"/>
      <span className="lbl">{def.label}</span>
    </span>
  );
}

/* ───────────────────────── Identicon ─────────────────────────
 * Deterministic 5x5 symmetric pattern derived from a worker_id /
 * actor_id string. Never a profile photo.
 */
function Identicon({ id, size = "md" }) {
  const cells = useMemo(() => {
    // Cheap hash
    let h = 0;
    for (let i = 0; i < id.length; i++) h = (h * 31 + id.charCodeAt(i)) | 0;
    const hue = Math.abs(h) % 360;
    const out = [];
    for (let y = 0; y < 5; y++) {
      for (let x = 0; x < 5; x++) {
        // mirror around column 2
        const xm = x < 3 ? x : 4 - x;
        const k = (h ^ (y * 7 + xm * 13 + 17)) & 0xff;
        const on = (k % 3) !== 0;
        out.push({ on, hue });
      }
    }
    return { cells: out, hue };
  }, [id]);
  return (
    <span className={`sw-identicon ${size === "lg" ? "lg" : size === "sm" ? "sm" : ""}`}
          aria-label={`identicon for ${id}`} title={id}>
      {cells.cells.map((c, i) => (
        <span key={i} style={{
          background: c.on
            ? `oklch(0.55 0.08 ${cells.hue})`
            : "transparent"
        }}/>
      ))}
    </span>
  );
}

/* ───────────────────────── Money / Duration / DateTime ───────────────────────── */

function MoneyDisplay({ cents, large = false, noRate = false, signed = false }) {
  if (noRate) return <span className="sw-money no-rate">no_rate_configured</span>;
  if (cents == null) return <span className="sw-money no-rate">no_rate_configured</span>;
  const txt = fmtMoneyCents(cents, { withSymbol: false });
  return (
    <span className={`sw-money ${large ? "large" : ""}`}>
      <span className="cur">€</span>{txt}
    </span>
  );
}

function DurationDisplay({ minutes, billable, nonBillable }) {
  if (billable != null || nonBillable != null) {
    return (
      <span className="sw-duration">
        <span className="billable">{fmtDuration(billable || 0)}</span>
        <span className="sep">·</span>
        <span className="nonbill">+{fmtDuration(nonBillable || 0)} non-bill</span>
      </span>
    );
  }
  return <span className="sw-duration billable">{fmtDuration(minutes)}</span>;
}

function DateTimeDisplay({ iso, tz = "UTC", rel }) {
  return (
    <span className="sw-dt">
      <span className="iso">{iso}</span>
      <span className="tz">{tz}</span>
      {rel && <span className="rel">{rel}</span>}
    </span>
  );
}

/* ───────────────────────── Form atoms ───────────────────────── */

function Field({ label, hint, error, audit, children }) {
  return (
    <div className="sw-field">
      {label && <label>{label}</label>}
      {children}
      {audit && (
        <span className="audit-note">
          <I.Alert size={11}/> will be recorded in audit
        </span>
      )}
      {hint && !error && <span className="help">{hint}</span>}
      {error && <span className="err"><I.Alert size={11}/> {error}</span>}
    </div>
  );
}

function TextInput({ value, placeholder, focus, error, disabled, prefix, suffix }) {
  return (
    <div className={`sw-input ${focus ? "is-focus" : ""} ${error ? "is-error" : ""} ${disabled ? "is-disabled" : ""}`}>
      {prefix && <span className="prefix">{prefix}</span>}
      <span className="val left" style={{ fontFamily: "var(--font-sans)", textAlign: "left" }}>{value || <span style={{ color: "var(--color-muted-2)" }}>{placeholder}</span>}</span>
      {suffix && <span className="suffix">{suffix}</span>}
    </div>
  );
}

function CurrencyInput({ cents, placeholder = "0,00", focus, error }) {
  const display = cents != null ? fmtMoneyCents(cents, { withSymbol: false }) : "";
  return (
    <div className={`sw-input ${focus ? "is-focus" : ""} ${error ? "is-error" : ""}`}>
      <span className="prefix">€</span>
      <span className="val">{display || <span style={{ color: "var(--color-muted-2)" }}>{placeholder}</span>}</span>
      <span className="suffix">EUR</span>
    </div>
  );
}

function DurationInput({ minutes, focus }) {
  const display = minutes != null ? fmtDuration(minutes) : "0h 00m";
  return (
    <div className={`sw-input ${focus ? "is-focus" : ""}`} style={{ width: 160 }}>
      <I.Clock size={14}/>
      <span className="val">{display}</span>
      <span className="suffix">min</span>
    </div>
  );
}

function DateTimePicker({ iso = "2026-05-24T07:32:00Z", focus }) {
  return (
    <div className={`sw-input ${focus ? "is-focus" : ""}`} style={{ width: 280 }}>
      <I.Calendar size={14}/>
      <span className="val left" style={{ fontFamily: "var(--font-mono)", textAlign: "left" }}>{iso}</span>
      <span className="tz" style={{
        fontFamily: "var(--font-mono)", fontSize: 9.5, padding: "1px 4px",
        borderRadius: 3, background: "var(--color-card-2)", color: "var(--color-muted)",
        border: "var(--hairline) solid var(--color-border)", letterSpacing: "0.04em", textTransform: "uppercase"
      }}>UTC</span>
    </div>
  );
}

function Segmented({ options, value, onChange, size = "md", full = false }) {
  return (
    <div className={`sw-seg ${size === "lg" ? "lg" : ""} ${full ? "full" : ""}`}>
      {options.map((o) => (
        <button key={o.value} className={o.value === value ? "active" : ""}
                onClick={() => onChange && onChange(o.value)}>
          {o.icon}{o.label}
        </button>
      ))}
    </div>
  );
}

function Toggle({ on }) { return <span className={`sw-toggle ${on ? "on" : ""}`}/>; }
function Radio({ on }) { return <span className={`sw-radio ${on ? "on" : ""}`}/>; }

/* ───────────────────────── Diff + JSON viewers ───────────────────────── */

function JsonViewer({ value, highlights = {}, annotations = {} }) {
  // Render a static JSON tree with optional key-name highlighting + side annotations.
  const render = (v, indent, keyPath) => {
    const k = keyPath?.split(".").pop();
    const hl = highlights[k] || highlights[keyPath];
    const note = annotations[keyPath];
    const space = (n) => " ".repeat(n * 2);
    if (v === null) return <span className="b">null</span>;
    if (typeof v === "string") return <span className="s">"{v}"</span>;
    if (typeof v === "number") return <span className="n">{v}</span>;
    if (typeof v === "boolean") return <span className="b">{String(v)}</span>;
    if (Array.isArray(v)) {
      return (
        <>
          <span className="punc">[</span>
          {v.length === 0 ? <span className="punc">]</span> : (
            <>
              {v.map((item, i) => (
                <div key={i} className="row" style={{ paddingLeft: (indent + 1) * 16 }}>
                  {render(item, indent + 1, `${keyPath}.${i}`)}
                  {i < v.length - 1 && <span className="punc">,</span>}
                </div>
              ))}
              <div className="row" style={{ paddingLeft: indent * 16 }}><span className="punc">]</span></div>
            </>
          )}
        </>
      );
    }
    if (typeof v === "object") {
      const keys = Object.keys(v);
      return (
        <>
          <span className="punc">{"{"}</span>
          {keys.length === 0 ? <span className="punc">{"}"}</span> : (
            <>
              {keys.map((kk, i) => {
                const ann = annotations[kk];
                const nestedHl = highlights[kk];
                return (
                  <div key={kk} className="row" style={{ paddingLeft: (indent + 1) * 16 }}>
                    <span className={`k ${nestedHl ? "hl" : ""}`}>"{kk}"</span>
                    <span className="punc">: </span>
                    {render(v[kk], indent + 1, kk)}
                    {i < keys.length - 1 && <span className="punc">,</span>}
                    {ann && <span className="ann">// {ann}</span>}
                  </div>
                );
              })}
              <div className="row" style={{ paddingLeft: indent * 16 }}><span className="punc">{"}"}</span></div>
            </>
          )}
        </>
      );
    }
    return null;
  };
  return <div className="sw-json">{render(value, 0, "")}</div>;
}

function DiffViewer({ rows, title, subtitle }) {
  return (
    <div className="sw-diff">
      {(title || subtitle) && (
        <div className="hdr">
          <span>{title}</span>
          <span style={{ color: "var(--color-muted)" }}>{subtitle}</span>
        </div>
      )}
      {rows.map((r, i) => (
        <div key={i} className={`row ${r.kind === "+" ? "add" : r.kind === "-" ? "rem" : "ctx"}`}>
          <span className="mark">{r.kind === "+" ? "+" : r.kind === "-" ? "−" : " "}</span>
          <code style={{ whiteSpace: "pre", paddingLeft: (r.indent || 0) * 12 }}>{r.text}</code>
        </div>
      ))}
    </div>
  );
}

/* ───────────────────────── Timeline ───────────────────────── */

function Timeline({ items }) {
  return (
    <div className="sw-timeline">
      {items.map((it, i) => (
        <div key={i} className={`sw-tl-item is-${it.kind || "edit"}`}>
          <div className="sw-tl-head">
            {it.badge}
            <span className="who">{it.who}</span>
            <span style={{ color: "var(--color-muted)" }}>{it.verb}</span>
          </div>
          <div className="sw-tl-meta">
            <DateTimeDisplay iso={it.iso} tz="UTC" rel={it.rel}/>
          </div>
          {it.detail && <div style={{ marginTop: 6, fontSize: 12, color: "var(--color-fg-2)" }}>{it.detail}</div>}
        </div>
      ))}
    </div>
  );
}

/* ───────────────────────── Reason prompt ───────────────────────── */

function ReasonPrompt({ value }) {
  return (
    <div className="sw-reason">
      <div className="head"><I.Alert size={12}/> Reason · required</div>
      <textarea defaultValue={value} placeholder="Why is this change being made? Audit-visible, immutable."/>
      <div className="foot">This text becomes a permanent audit_entry attached to the resource.</div>
    </div>
  );
}

/* ───────────────────────── Tiles ───────────────────────── */

function StatTile({ label, cents, noRate, value, sub, large }) {
  return (
    <div className="sw-tile">
      <div className="lbl">{label}</div>
      <div className="val">
        {noRate
          ? <span style={{
              fontFamily: "var(--font-sans)", fontSize: 13,
              background: "var(--color-warn-soft)", color: "var(--color-warn)",
              padding: "2px 8px", borderRadius: 4
            }}>no_rate_configured</span>
          : cents != null
            ? <><span className="cur">€</span>{fmtMoneyCents(cents, { withSymbol: false })}</>
            : value}
      </div>
      {sub && <div className="sub">{sub}</div>}
    </div>
  );
}

/* ───────────────────────── ProgressTrail / Stepper ───────────────────────── */

function ProgressTrail({ steps }) {
  return (
    <div className="sw-trail">
      {steps.map((s, i) => (
        <React.Fragment key={i}>
          <div className={`step ${s.state || ""}`}>
            <StatusBadge namespace={s.ns} value={s.value} showNs={false}/>
            {s.label && <span style={{ color: "var(--color-muted)", marginLeft: 4 }}>{s.label}</span>}
          </div>
          {i < steps.length - 1 && <span className="arr">→</span>}
        </React.Fragment>
      ))}
    </div>
  );
}

/* ───────────────────────── Toasts / Alerts ───────────────────────── */

function InlineAlert({ tone = "info", title, body, action }) {
  const ico = tone === "info" ? <I.Info size={14}/>
            : tone === "warn" ? <I.Alert size={14}/>
            : tone === "error" ? <I.Alert size={14}/>
            : <I.CircleCheck size={14}/>;
  return (
    <div className={`sw-alert ${tone}`}>
      <span className="ico">{ico}</span>
      <div>
        {title && <b>{title}</b>}
        {body && <p>{body}</p>}
        {action && <div style={{ marginTop: 6 }}>{action}</div>}
      </div>
    </div>
  );
}

/* ───────────────────────── App-shell building blocks ───────────────────────── */

function PhoneFrame({ children }) {
  return (
    <div className="sw-phone">
      <div className="screen">{children}</div>
    </div>
  );
}

function DeskShell({ children }) {
  return <div className="sw-desk">{children}</div>;
}

/* ───────────────────────── Audit row ───────────────────────── */

function AuditRow({ actor, actorRole, action, ns = "work_session", when, rel, badgeTone = "info", detail }) {
  return (
    <div className="sw-audit">
      <Identicon id={actor}/>
      <div className="who">
        <b>{actor}</b>
        <span className="sub">{actorRole}</span>
      </div>
      <div className="action">
        <span className={`sw-pill ${badgeTone}`}>{action}</span>
      </div>
      <div className="when">
        <DateTimeDisplay iso={when} tz="UTC" rel={rel}/>
      </div>
    </div>
  );
}

/* ───────────────────────── Export to window ───────────────────────── */

Object.assign(window, {
  fmtMoneyCents, fmtDuration,
  STATUS, StatusBadge, Identicon,
  MoneyDisplay, DurationDisplay, DateTimeDisplay,
  Field, TextInput, CurrencyInput, DurationInput, DateTimePicker,
  Segmented, Toggle, Radio,
  JsonViewer, DiffViewer, Timeline,
  ReasonPrompt, StatTile, ProgressTrail,
  InlineAlert, PhoneFrame, DeskShell, AuditRow,
});
