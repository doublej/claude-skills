/* Extended primitives — generic, reusable across any tooling project.
 * Domain-agnostic by design. Pair with .flat-card, .status, .identicon,
 * .segmented, .toggle, .input-frame, .json-tree, .diff, .timeline,
 * .stepper, .stat-tile, .alert-inline, .reason-prompt, .phone-frame
 * in tokens.css.
 *
 * Consumers register their domain enums via `setStatusRegistry(namespace, defs)`
 * and the StatusBadge component looks them up automatically.
 */

const { useMemo: useMemoX } = React;

/* ───────────────────────── Status registry ─────────────────────────
 * The registry is a global keyed by namespace. Each entry maps domain
 * values → { tone, label, icon }. Consumers register their own:
 *
 *   setStatusRegistry('order', {
 *     PLACED:    { tone: 'info',  label: 'Placed'    },
 *     FULFILLED: { tone: 'pos',   label: 'Fulfilled' },
 *     CANCELLED: { tone: 'neg',   label: 'Cancelled' },
 *   });
 *
 *   <StatusBadge namespace="order" value="PLACED"/>
 *
 * Tones are visual buckets the CSS knows about:
 *   info · neutral · warn · pos · neg · muted · accent
 */
const __statusRegistries = {};
function setStatusRegistry(namespace, defs) {
  __statusRegistries[namespace] = defs;
}
function getStatus(namespace, value) {
  return __statusRegistries[namespace]?.[value];
}

function StatusBadge({ namespace, value, tone, label, icon, showNs = true }) {
  const def = (namespace && value != null) ? getStatus(namespace, value) : null;
  const resolvedTone  = def?.tone  ?? tone  ?? "neutral";
  const resolvedLabel = def?.label ?? label ?? value ?? "—";
  const resolvedIcon  = def?.icon  ?? icon;
  return (
    <span className={`status tone-${resolvedTone}`}>
      {showNs && namespace && <span className="ns">{namespace}</span>}
      {resolvedIcon
        ? <span className="ico">{resolvedIcon}</span>
        : <span className="dot"/>}
      <span className="lbl">{resolvedLabel}</span>
    </span>
  );
}

/* ───────────────────────── Identicon ─────────────────────────
 * Deterministic 5x5 symmetric pattern from any opaque string ID.
 * Use for opaque actors (worker IDs, API keys, anonymous accounts) — never
 * for users whose photo you actually have.
 */
function Identicon({ id, size = "md" }) {
  const data = useMemoX(() => {
    let h = 0;
    for (let i = 0; i < id.length; i++) h = (h * 31 + id.charCodeAt(i)) | 0;
    const hue = Math.abs(h) % 360;
    const cells = [];
    for (let y = 0; y < 5; y++) {
      for (let x = 0; x < 5; x++) {
        const xm = x < 3 ? x : 4 - x;
        const k = (h ^ (y * 7 + xm * 13 + 17)) & 0xff;
        cells.push((k % 3) !== 0);
      }
    }
    return { cells, hue };
  }, [id]);
  return (
    <span className={`identicon ${size === "lg" ? "lg" : size === "sm" ? "sm" : ""}`}
          aria-label={`identicon for ${id}`} title={id}>
      {data.cells.map((on, i) => (
        <span key={i} style={{ background: on ? `oklch(0.55 0.08 ${data.hue})` : "transparent" }}/>
      ))}
    </span>
  );
}

/* ───────────────────────── Money formatter ─────────────────────────
 * Cents-aware, locale-aware. Default is Dutch euros; pass `locale`
 * and `currency` to switch.
 *
 *   fmtMoneyCents(450000)
 *     → "€ 4.500,00"
 *   fmtMoneyCents(450000, { locale: 'en-US', currency: 'USD' })
 *     → "$4,500.00"
 */
function fmtMoneyCents(cents, { locale = "nl-NL", currency = "EUR", withSymbol = true } = {}) {
  if (cents == null) return "—";
  const amount = cents / 100;
  if (withSymbol) {
    return new Intl.NumberFormat(locale, { style: "currency", currency }).format(amount);
  }
  return new Intl.NumberFormat(locale, { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(amount);
}

function MoneyDisplay({ cents, large = false, noData = false, locale = "nl-NL", currency = "EUR", noDataLabel = "no data" }) {
  if (noData || cents == null) {
    return <span className="money no-data">{noDataLabel}</span>;
  }
  // Currency symbol rendered separately so it can use display font sizing in .large
  const symbol = new Intl.NumberFormat(locale, { style: "currency", currency, currencyDisplay: "narrowSymbol" })
    .formatToParts(0).find(p => p.type === "currency")?.value ?? "";
  const body = fmtMoneyCents(cents, { locale, currency, withSymbol: false });
  return (
    <span className={`money ${large ? "large" : ""}`}>
      <span className="cur">{symbol}</span>{body}
    </span>
  );
}

/* ───────────────────────── Duration ─────────────────────────
 * Integer-minute typed durations rendered "Hh Mm".
 */
function fmtDuration(minutes, { compact = false } = {}) {
  if (minutes == null) return "—";
  const neg = minutes < 0;
  const m = Math.abs(minutes);
  const h = Math.floor(m / 60);
  const rem = m - h * 60;
  if (compact) return `${neg ? "−" : ""}${h}:${String(rem).padStart(2, "0")}`;
  if (h === 0)   return `${neg ? "−" : ""}${rem}m`;
  if (rem === 0) return `${neg ? "−" : ""}${h}h`;
  return `${neg ? "−" : ""}${h}h ${String(rem).padStart(2, "0")}m`;
}

function DurationDisplay({ minutes, primary, secondary, secondaryLabel = "secondary" }) {
  if (primary != null || secondary != null) {
    return (
      <span className="duration">
        <span className="primary">{fmtDuration(primary || 0)}</span>
        {secondary != null && (
          <>
            <span className="sep">·</span>
            <span className="secondary">+{fmtDuration(secondary)} {secondaryLabel}</span>
          </>
        )}
      </span>
    );
  }
  return <span className="duration primary">{fmtDuration(minutes)}</span>;
}

/* ───────────────────────── DateTime display ───────────────────────── */
function DateTimeDisplay({ iso, tz = "UTC", rel }) {
  return (
    <span className="datetime">
      <span className="iso">{iso}</span>
      <span className="tz">{tz}</span>
      {rel && <span className="rel">{rel}</span>}
    </span>
  );
}

/* ───────────────────────── Form atoms ───────────────────────── */

function Field({ label, hint, error, audit, children }) {
  return (
    <div className="field">
      {label && <label>{label}</label>}
      {children}
      {audit && (
        <span className="audit-note">
          <I.Alert size={11}/> {typeof audit === "string" ? audit : "will be recorded"}
        </span>
      )}
      {hint && !error && <span className="help">{hint}</span>}
      {error && <span className="err"><I.Alert size={11}/> {error}</span>}
    </div>
  );
}

function InputFrame({ value, placeholder, focus, error, disabled, prefix, suffix, icon, mono = false, align = "left", width }) {
  const style = width ? { width } : undefined;
  const fontFamily = mono ? "var(--font-mono)" : "var(--font-sans)";
  return (
    <div className={`input-frame ${focus ? "is-focus" : ""} ${error ? "is-error" : ""} ${disabled ? "is-disabled" : ""}`} style={style}>
      {icon && <span className="ico">{icon}</span>}
      {prefix && <span className="prefix">{prefix}</span>}
      <span className={`val ${align === "left" ? "left" : ""}`} style={{ fontFamily }}>
        {value != null && value !== ""
          ? value
          : <span style={{ color: "var(--color-muted-2)" }}>{placeholder}</span>}
      </span>
      {suffix && <span className="suffix">{suffix}</span>}
    </div>
  );
}

function CurrencyInput({ cents, placeholder = "0,00", focus, error, locale = "nl-NL", currency = "EUR" }) {
  const symbol = new Intl.NumberFormat(locale, { style: "currency", currency, currencyDisplay: "narrowSymbol" })
    .formatToParts(0).find(p => p.type === "currency")?.value ?? "";
  const body = cents != null ? fmtMoneyCents(cents, { locale, currency, withSymbol: false }) : "";
  return (
    <div className={`input-frame ${focus ? "is-focus" : ""} ${error ? "is-error" : ""}`}>
      <span className="prefix">{symbol}</span>
      <span className="val">{body || <span style={{ color: "var(--color-muted-2)" }}>{placeholder}</span>}</span>
      <span className="suffix">{currency}</span>
    </div>
  );
}

function DurationInput({ minutes, focus, width = 160 }) {
  const display = minutes != null ? fmtDuration(minutes) : "0h 00m";
  return (
    <div className={`input-frame ${focus ? "is-focus" : ""}`} style={{ width }}>
      <span className="ico"><I.Clock size={14}/></span>
      <span className="val">{display}</span>
      <span className="suffix">min</span>
    </div>
  );
}

function DateTimePicker({ iso = "2026-05-24T07:32:00Z", tz = "UTC", focus, width = 280 }) {
  return (
    <div className={`input-frame ${focus ? "is-focus" : ""}`} style={{ width }}>
      <span className="ico"><I.Calendar size={14}/></span>
      <span className="val left" style={{ fontFamily: "var(--font-mono)" }}>{iso}</span>
      <span style={{
        fontFamily: "var(--font-mono)", fontSize: 9.5, padding: "1px 4px",
        borderRadius: 3, background: "var(--color-card-2)", color: "var(--color-muted)",
        border: "var(--hairline) solid var(--color-border)",
        letterSpacing: "0.04em", textTransform: "uppercase",
      }}>{tz}</span>
    </div>
  );
}

function Segmented({ options, value, onChange, size = "md", full = false }) {
  return (
    <div className={`segmented ${size === "lg" ? "lg" : ""} ${full ? "full" : ""}`}>
      {options.map((o) => (
        <button key={o.value} className={o.value === value ? "active" : ""}
                onClick={() => onChange && onChange(o.value)}>
          {o.icon}{o.label}
        </button>
      ))}
    </div>
  );
}

function Toggle({ on, onChange }) {
  return <span className={`toggle ${on ? "on" : ""}`} role="switch" aria-checked={!!on} onClick={() => onChange && onChange(!on)}/>;
}
function RadioDot({ on }) { return <span className={`radio-dot ${on ? "on" : ""}`}/>; }

/* ───────────────────────── JSON viewer ───────────────────────── */

function JsonViewer({ value, highlights = {}, annotations = {} }) {
  const render = (v, indent, keyPath) => {
    if (v === null) return <span className="b">null</span>;
    if (typeof v === "string")  return <span className="s">"{v}"</span>;
    if (typeof v === "number")  return <span className="n">{v}</span>;
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
                const hl  = highlights[kk];
                return (
                  <div key={kk} className="row" style={{ paddingLeft: (indent + 1) * 16 }}>
                    <span className={`k ${hl ? "hl" : ""}`}>"{kk}"</span>
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
  return <div className="json-tree">{render(value, 0, "")}</div>;
}

/* ───────────────────────── Diff viewer ───────────────────────── */

function DiffViewer({ rows, title, subtitle }) {
  return (
    <div className="diff">
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
    <div className="timeline">
      {items.map((it, i) => (
        <div key={i} className={`timeline-item ${it.tone ? `tone-${it.tone}` : ""}`}>
          <div className="timeline-head">
            {it.badge}
            {it.who && <span className="who">{it.who}</span>}
            {it.verb && <span style={{ color: "var(--color-muted)" }}>{it.verb}</span>}
          </div>
          {(it.iso || it.rel) && (
            <div className="timeline-meta">
              {it.iso && <DateTimeDisplay iso={it.iso} tz={it.tz || "UTC"} rel={it.rel}/>}
            </div>
          )}
          {it.detail && <div style={{ marginTop: 6, fontSize: 12, color: "var(--color-fg-2)" }}>{it.detail}</div>}
        </div>
      ))}
    </div>
  );
}

/* ───────────────────────── Stepper / progress trail ─────────────────────────
 * Render a horizontal trail of steps. Each step accepts either a `label`
 * + `state` or any custom React content via `children`.
 */
function Stepper({ steps }) {
  return (
    <div className="stepper">
      {steps.map((s, i) => (
        <React.Fragment key={i}>
          <div className={`step ${s.state || ""}`}>
            {s.badge ?? s.label}
            {s.suffix && <span style={{ color: "var(--color-muted)", marginLeft: 4 }}>{s.suffix}</span>}
          </div>
          {i < steps.length - 1 && <span className="arr">{s.connector || "→"}</span>}
        </React.Fragment>
      ))}
    </div>
  );
}

/* ───────────────────────── Stat tile (Stat + no-data state) ───────────────────────── */

function StatTile({ label, cents, value, sub, noData = false, noDataLabel = "no data" }) {
  return (
    <div className="stat-tile">
      <div className="lbl">{label}</div>
      <div className="val">
        {noData
          ? <span className="no-data">{noDataLabel}</span>
          : cents != null
            ? <MoneyDisplay cents={cents} large/>
            : value}
      </div>
      {sub && <div className="sub">{sub}</div>}
    </div>
  );
}

/* ───────────────────────── Confidence meter ───────────────────────── */

function Confidence({ value, tone = "warn", width = 80 }) {
  return (
    <div className={`confidence tone-${tone}`}>
      <span className="bar" style={{ width }}><i style={{ width: `${value}%` }}/></span>
      <span>{value}%</span>
    </div>
  );
}

/* ───────────────────────── Inline alert ───────────────────────── */

function InlineAlert({ tone = "info", title, body, action }) {
  const ico = tone === "info"  ? <I.Info size={14}/>
            : tone === "warn"  ? <I.Alert size={14}/>
            : tone === "error" ? <I.Alert size={14}/>
            : <I.CircleCheck size={14}/>;
  return (
    <div className={`alert-inline ${tone}`}>
      <span className="ico">{ico}</span>
      <div>
        {title && <b>{title}</b>}
        {body && <p>{body}</p>}
        {action && <div style={{ marginTop: 6 }}>{action}</div>}
      </div>
    </div>
  );
}

/* ───────────────────────── Reason prompt ───────────────────────── */

function ReasonPrompt({ value, label = "Reason · required", note = "This text becomes a permanent audit_entry attached to the resource." }) {
  return (
    <div className="reason-prompt">
      <div className="head"><I.Alert size={12}/> {label}</div>
      <textarea defaultValue={value} placeholder="Why is this change being made? Audit-visible, immutable."/>
      <div className="foot">{note}</div>
    </div>
  );
}

/* ───────────────────────── Phone frame ─────────────────────────
 * Generic mobile-mock chrome for prototypes. Use directly:
 *   <PhoneFrame><div className="screen">… </div></PhoneFrame>
 * Or use the convenience parts below.
 */
function PhoneFrame({ children }) {
  return (
    <div className="phone-frame">
      <div className="screen">{children}</div>
    </div>
  );
}

/* ───────────────────────── FlatCard convenience wrapper ─────────────────────── */

function FlatCard({ title, sub, actions, flush, children, className = "" }) {
  return (
    <section className={`flat-card ${className}`}>
      {(title || actions) && (
        <header className="head">
          <div>
            {title && <h3>{title}</h3>}
            {sub && <div className="sub">{sub}</div>}
          </div>
          {actions && <div className="actions">{actions}</div>}
        </header>
      )}
      <div className={`body ${flush ? "flush" : ""}`}>{children}</div>
    </section>
  );
}

/* ───────────────────────── Exports ───────────────────────── */
Object.assign(window, {
  // status
  setStatusRegistry, getStatus, StatusBadge,
  // identity
  Identicon,
  // formatting
  fmtMoneyCents, fmtDuration,
  // displays
  MoneyDisplay, DurationDisplay, DateTimeDisplay,
  // forms
  Field, InputFrame, CurrencyInput, DurationInput, DateTimePicker,
  Segmented, Toggle, RadioDot,
  // data views
  JsonViewer, DiffViewer, Timeline, Stepper,
  // composites
  StatTile, Confidence, InlineAlert, ReasonPrompt, FlatCard,
  // device
  PhoneFrame,
});
