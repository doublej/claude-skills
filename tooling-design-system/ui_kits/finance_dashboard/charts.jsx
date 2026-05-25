// Charts — built to feel like lightweight-charts: thin grid, tabular axes, area fill.

function PriceChart({ data, height = 220, tone = "pos" }) {
  const [hover, setHover] = useState(null);
  const ref = useRef(null);
  const width = 800;  // virtual viewBox width — scales responsively via preserveAspectRatio
  const padL = 0, padR = 0, padT = 16, padB = 24;
  const innerW = width - padL - padR;
  const innerH = height - padT - padB;

  const min = Math.min(...data), max = Math.max(...data);
  const span = max - min || 1;
  const n = data.length;
  const xStep = innerW / (n - 1);
  const pts = data.map((v, i) => [padL + i * xStep, padT + innerH - ((v - min) / span) * innerH]);
  const path = pts.map((p, i) => `${i === 0 ? "M" : "L"}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(" ");
  const fill = `${path} L${padL + innerW},${padT + innerH} L${padL},${padT + innerH} Z`;
  const stroke = tone === "pos" ? "var(--color-pos)" : tone === "neg" ? "var(--color-neg)" : "var(--color-accent)";

  const yTicks = 4;
  const yLines = Array.from({ length: yTicks + 1 }, (_, i) => {
    const v = min + (span * i) / yTicks;
    const y = padT + innerH - ((v - min) / span) * innerH;
    return { v, y };
  });

  const onMove = (e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * width;
    let i = Math.round((x - padL) / xStep);
    i = Math.max(0, Math.min(n - 1, i));
    setHover({ i, x: pts[i][0], y: pts[i][1], v: data[i] });
  };

  return (
    <div ref={ref} style={{ position: "relative", width: "100%" }}>
      <svg
        viewBox={`0 0 ${width} ${height}`}
        width="100%"
        height={height}
        preserveAspectRatio="none"
        onMouseMove={onMove}
        onMouseLeave={() => setHover(null)}
        style={{ display: "block", cursor: "crosshair" }}
      >
        {/* Grid */}
        {yLines.map((g, i) => (
          <line key={i} x1={padL} x2={padL + innerW} y1={g.y} y2={g.y} stroke="var(--color-border)" strokeDasharray={i === yTicks ? "0" : "2 3"} strokeWidth="1" vectorEffect="non-scaling-stroke"/>
        ))}
        {/* Area + line */}
        <path d={fill} fill={stroke} opacity="0.10"/>
        <path d={path} fill="none" stroke={stroke} strokeWidth="1.5" vectorEffect="non-scaling-stroke" strokeLinecap="round" strokeLinejoin="round"/>
        {/* Crosshair */}
        {hover && (
          <g>
            <line x1={hover.x} x2={hover.x} y1={padT} y2={padT + innerH} stroke="var(--color-border-strong)" strokeDasharray="2 3" vectorEffect="non-scaling-stroke"/>
            <circle cx={hover.x} cy={hover.y} r="3.5" fill="var(--color-bg-elev)" stroke={stroke} strokeWidth="1.5" vectorEffect="non-scaling-stroke"/>
          </g>
        )}
      </svg>
      {/* Y labels */}
      <div style={{ position: "absolute", left: 8, top: 0, bottom: 0, pointerEvents: "none", display: "flex", flexDirection: "column", justifyContent: "space-between", paddingTop: 8, paddingBottom: 28 }}>
        {[...yLines].reverse().map((g, i) => (
          <span key={i} className="money" style={{ fontSize: 10, color: "var(--color-muted)" }}>{fmt.money(g.v, { decimals: 0 })}</span>
        ))}
      </div>
      {/* Hover tooltip */}
      {hover && (
        <div style={{
          position: "absolute",
          left: `${(hover.x / width) * 100}%`,
          top: 0,
          transform: "translate(-50%, -100%)",
          marginTop: -8,
          padding: "6px 8px",
          background: "var(--color-bg-elev)",
          border: "0.5px solid var(--color-border)",
          borderRadius: 6,
          boxShadow: "var(--shadow-sm)",
          fontSize: 11,
          whiteSpace: "nowrap",
          pointerEvents: "none",
        }}>
          <div className="t-eyebrow" style={{ fontSize: 9, marginBottom: 2 }}>Day {hover.i + 1}</div>
          <div className="money" style={{ fontSize: 12, fontWeight: 500 }}>{fmt.money(hover.v)}</div>
        </div>
      )}
      {/* X axis ticks */}
      <div style={{ display: "flex", justifyContent: "space-between", marginTop: -20, fontSize: 10, color: "var(--color-muted)", paddingLeft: 8, paddingRight: 8 }}>
        <span>90d ago</span><span>60d</span><span>30d</span><span>Today</span>
      </div>
    </div>
  );
}

// Allocation donut — proportional segments
function AllocationDonut({ items, size = 140 }) {
  const total = items.reduce((s, i) => s + i.value, 0);
  const r = size / 2 - 12;
  const c = size / 2;
  const circ = 2 * Math.PI * r;
  let offset = 0;
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle cx={c} cy={c} r={r} fill="none" stroke="var(--color-card-2)" strokeWidth="14"/>
        {items.map((it, i) => {
          const len = (it.value / total) * circ;
          const dash = `${len} ${circ - len}`;
          const arc = (
            <circle key={i} cx={c} cy={c} r={r} fill="none"
              stroke={`var(--chart-${(i % 8) + 1})`} strokeWidth="14"
              strokeDasharray={dash} strokeDashoffset={-offset}
              transform={`rotate(-90 ${c} ${c})`}
              strokeLinecap="butt"/>
          );
          offset += len;
          return arc;
        })}
        <text x={c} y={c - 6} textAnchor="middle" fontSize="10" fill="var(--color-muted)" letterSpacing="0.06em" style={{ fontFamily: "var(--font-sans)" }}>TOTAL</text>
        <text x={c} y={c + 18} textAnchor="middle" fontSize="22" fill="var(--color-fg)" fontWeight="400" style={{ fontFamily: "var(--font-display)", fontVariantNumeric: "tabular-nums lining-nums", letterSpacing: "-0.01em" }}>{fmt.money(total, { decimals: 0 })}</text>
      </svg>
      <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 6 }}>
        {items.map((it, i) => (
          <div key={i} style={{ display: "flex", alignItems: "center", gap: 8, fontSize: 13 }}>
            <span style={{ width: 8, height: 8, borderRadius: 2, background: `var(--chart-${(i % 8) + 1})` }}/>
            <span>{it.label}</span>
            <span className="money" style={{ marginLeft: "auto", color: "var(--color-muted)" }}>{((it.value / total) * 100).toFixed(0)}%</span>
            <span className="money" style={{ width: 80, textAlign: "right" }}>{fmt.money(it.value, { decimals: 0 })}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

Object.assign(window, { PriceChart, AllocationDonut });
