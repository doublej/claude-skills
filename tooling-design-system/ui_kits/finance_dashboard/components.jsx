// Core components — Button, Badge, Money, Stat, Card, EmptyState, PageHeader, DataTable
// Sized to fit within 400 LOC. Larger compositions live in screens.jsx.

const { useState, useEffect, useRef, useMemo, useCallback } = React;

// ----- Button -----
function Button({ variant = "secondary", size = "md", icon, children, className, ...rest }) {
  const cls = ["btn", `btn-${variant}`, size !== "md" && `btn-${size}`, !children && "btn-icon", className].filter(Boolean).join(" ");
  return (
    <button className={cls} {...rest}>
      {icon && <span className="ico">{icon}</span>}
      {children}
    </button>
  );
}

// ----- Badge -----
function Badge({ tone = "neutral", dot, children }) {
  return (
    <span className={`badge badge-${tone}`}>
      {dot && <span className="dot" style={{ background: "currentColor" }} />}
      {children}
    </span>
  );
}

function Tag({ children }) {
  return <span className="tag">{children}</span>;
}

// ----- Money -----
// Wraps a number (or formatted string) with .money + tabular-nums.
// Reads window.privacyMode via a state hook; when active body has .privacy-mode applied.
function Money({ value, signed, decimals = 2, tone, className = "", ...rest }) {
  const text = typeof value === "string" ? value : fmt.money(value, { signed, decimals });
  const colorStyle = tone === "pos" ? { color: "var(--color-pos)" } :
                     tone === "neg" ? { color: "var(--color-neg)" } : undefined;
  return (
    <span className={`money ${className}`} style={colorStyle} {...rest}>{text}</span>
  );
}

// Pct helper — same family
function Pct({ value, signed = true, decimals = 1, className = "" }) {
  const tone = value > 0 ? "pos" : value < 0 ? "neg" : null;
  const color = tone === "pos" ? "var(--color-pos)" : tone === "neg" ? "var(--color-neg)" : "var(--color-muted)";
  return (
    <span className={`money ${className}`} style={{ color }}>{fmt.pct(value, { signed, decimals })}</span>
  );
}

// ----- Sparkline -----
function Sparkline({ data, width = 80, height = 24, tone = "pos", filled = true }) {
  const min = Math.min(...data), max = Math.max(...data);
  const span = max - min || 1;
  const n = data.length;
  const xStep = width / (n - 1);
  const pts = data.map((v, i) => [i * xStep, height - ((v - min) / span) * height]);
  const path = pts.map((p, i) => `${i === 0 ? "M" : "L"}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(" ");
  const fillPath = `${path} L${width},${height} L0,${height} Z`;
  const stroke = tone === "pos" ? "var(--color-pos)" : tone === "neg" ? "var(--color-neg)" : "var(--color-accent)";
  return (
    <svg className="spark" width={width} height={height} viewBox={`0 0 ${width} ${height}`} aria-hidden="true">
      {filled && <path className="fill" d={fillPath} fill={stroke} />}
      <path d={path} fill="none" stroke={stroke} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

// ----- Card -----
function Card({ title, sub, actions, flush, children, className = "" }) {
  return (
    <section className={`card ${className}`}>
      {(title || actions) && (
        <header className="card-head">
          <div>
            {title && <h3>{title}</h3>}
            {sub && <div className="sub">{sub}</div>}
          </div>
          {actions && <div className="actions">{actions}</div>}
        </header>
      )}
      <div className={`card-body ${flush ? "flush" : ""}`}>{children}</div>
    </section>
  );
}

// ----- Stat -----
function Stat({ label, value, delta, deltaPct, sub, spark, sparkTone = "pos" }) {
  const tone = (delta ?? deltaPct) > 0 ? "pos" : (delta ?? deltaPct) < 0 ? "neg" : null;
  return (
    <div className="card" style={{ padding: 24 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
        <span className="stat-label">{label}</span>
        {spark && <span style={{ marginLeft: "auto" }}><Sparkline data={spark} width={64} height={20} tone={sparkTone} /></span>}
      </div>
      <div className="stat-value">
        {typeof value === "number"
          ? <><span className="sym">$</span>{fmt.money(value).replace(/^\$/, "")}</>
          : value}
      </div>
      {(delta !== undefined || deltaPct !== undefined || sub) && (
        <div className="stat-sub">
          {delta !== undefined && (
            <span className={`stat-delta ${tone || ""}`}>{fmt.money(delta, { signed: true })}</span>
          )}
          {deltaPct !== undefined && (
            <span className={`stat-delta ${tone || ""}`}>{fmt.pct(deltaPct)}</span>
          )}
          {sub && <span>{sub}</span>}
        </div>
      )}
    </div>
  );
}

// ----- EmptyState -----
function EmptyState({ icon, title, body, action }) {
  return (
    <div className="empty">
      {icon && <span className="ico">{icon}</span>}
      {title && <h3>{title}</h3>}
      {body && <p>{body}</p>}
      {action && <div style={{ marginTop: 8 }}>{action}</div>}
    </div>
  );
}

// ----- PageHeader -----
function PageHeader({ crumb, title, sub, actions, tabs, activeTab, onTab }) {
  return (
    <div className="page-header">
      {crumb && (
        <div className="crumb">
          {crumb.map((c, i) => (
            <React.Fragment key={i}>
              {i > 0 && <span className="sep">/</span>}
              {c.href ? <a onClick={c.onClick}>{c.label}</a> : <span>{c.label}</span>}
            </React.Fragment>
          ))}
        </div>
      )}
      <div className="row">
        <div>
          <h1>{title}</h1>
          {sub && <div className="sub">{sub}</div>}
        </div>
        {actions && <div className="actions">{actions}</div>}
      </div>
      {tabs && (
        <div className="tabs">
          {tabs.map((t) => (
            <button key={t} className={`tab ${activeTab === t ? "active" : ""}`} onClick={() => onTab && onTab(t)}>{t}</button>
          ))}
        </div>
      )}
    </div>
  );
}

// ----- DataTable -----
// columns: [{ key, label, align, render?(row), num? }]
// mobileCard: (row) => <ReactNode>
function DataTable({ columns, rows, mobileCard, getRowKey }) {
  return (
    <div className={`table-wrap ${mobileCard ? "has-mobile-card" : ""}`}>
      <table className="table">
        <thead>
          <tr>{columns.map((c) => <th key={c.key} className={c.num ? "num" : ""}>{c.label}</th>)}</tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={getRowKey ? getRowKey(r) : i}>
              {columns.map((c) => (
                <td key={c.key} className={c.num ? "num" : ""}>{c.render ? c.render(r) : r[c.key]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {mobileCard && (
        <div className="mobile-card-list">
          {rows.map((r, i) => (
            <div className="mc" key={getRowKey ? getRowKey(r) : i}>{mobileCard(r)}</div>
          ))}
        </div>
      )}
    </div>
  );
}

// ----- Toast -----
function Toast({ msg, onDismiss }) {
  useEffect(() => {
    const t = setTimeout(onDismiss, 2400);
    return () => clearTimeout(t);
  }, [msg]);
  if (!msg) return null;
  return (
    <div className="toast-wrap" role="status" aria-live="polite">
      <div className="toast">
        <span className="ico"><I.CircleCheck size={14}/></span>
        {msg}
      </div>
    </div>
  );
}

// ----- Theme + Privacy toggle hooks -----
function useTheme() {
  const [dark, setDark] = useState(false);
  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
  }, [dark]);
  return [dark, setDark];
}

function usePrivacy() {
  const [on, setOn] = useState(false);
  useEffect(() => {
    document.body.classList.toggle("privacy-mode", on);
  }, [on]);
  useEffect(() => {
    const handler = (e) => {
      if (e.metaKey && e.shiftKey && (e.key === "p" || e.key === "P")) {
        e.preventDefault();
        setOn(v => !v);
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);
  return [on, setOn];
}

Object.assign(window, {
  Button, Badge, Tag, Money, Pct, Sparkline,
  Card, Stat, EmptyState, PageHeader, DataTable, Toast,
  useTheme, usePrivacy,
});
