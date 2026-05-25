/* Schakelwerk canvas sections — each section is a DCSection with DCArtboards.
 *
 * Artboards are static design frames at fixed pixel sizes. Width / height
 * are tuned so content sits comfortably without internal scrolling.
 */

const SEC = {};

/* ═══════════════════════════════════════════════════════════════
   01 · FOUNDATIONS
   ═══════════════════════════════════════════════════════════════ */

SEC.Foundations = function Foundations() {
  return (
    <DCSection id="foundations" title="01 · Foundations" subtitle="Tokens inherited from the Tooling Design System. Schakelwerk does not add new colors.">
      <DCArtboard id="palette" label="Color · semantic" width={420} height={520}>
        <div className="sw-art">
          <div className="sw-h">Surfaces</div>
          <div className="sw-swatch"><span className="chip" style={{ background: "var(--color-bg)" }}/>bg<code>#fafafa</code></div>
          <div className="sw-swatch"><span className="chip" style={{ background: "var(--color-card)" }}/>card<code>#ffffff</code></div>
          <div className="sw-swatch"><span className="chip" style={{ background: "var(--color-card-2)" }}/>card-2<code>#f4f4f5</code></div>
          <div className="sw-h" style={{ marginTop: 16 }}>Text</div>
          <div className="sw-swatch"><span className="chip" style={{ background: "var(--color-fg)" }}/>fg<code>#0a0a0a</code></div>
          <div className="sw-swatch"><span className="chip" style={{ background: "var(--color-fg-2)" }}/>fg-2<code>zinc-800</code></div>
          <div className="sw-swatch"><span className="chip" style={{ background: "var(--color-muted)" }}/>muted<code>zinc-500</code></div>
          <div className="sw-h" style={{ marginTop: 16 }}>Semantic</div>
          <div className="sw-swatch"><span className="chip" style={{ background: "var(--color-accent)" }}/>accent<code>indigo</code></div>
          <div className="sw-swatch"><span className="chip" style={{ background: "var(--color-pos)" }}/>pos · approved/exported<code>green-600</code></div>
          <div className="sw-swatch"><span className="chip" style={{ background: "var(--color-warn)" }}/>warn · proposed/pending<code>amber-600</code></div>
          <div className="sw-swatch"><span className="chip" style={{ background: "var(--color-neg)" }}/>neg · rejected/failed<code>red-600</code></div>
          <div className="sw-swatch"><span className="chip" style={{ background: "var(--color-info)" }}/>info · ready/received<code>blue-600</code></div>
          <div className="sw-note"><strong>Reject ≠ delete.</strong> The destructive red is reserved for irreversible audit-affecting actions: reject, fail, archive.</div>
        </div>
      </DCArtboard>

      <DCArtboard id="type" label="Type" width={420} height={520}>
        <div className="sw-art sw-stack-4">
          <div>
            <div className="sw-eyebrow">Display · Instrument Serif</div>
            <div style={{ fontFamily: "var(--font-display)", fontSize: 48, lineHeight: 1, letterSpacing: "-0.02em" }}>
              <span style={{ fontSize: "0.6em", verticalAlign: "0.25em", color: "var(--color-fg-2)" }}>€ </span>4.500,00
            </div>
            <div style={{ fontSize: 11, color: "var(--color-muted)", marginTop: 4 }}>Hero numerals only · StatTile, CalculationSnapshot total.</div>
          </div>
          <hr className="sw-divider"/>
          <div>
            <div className="sw-eyebrow">Headings · Geist</div>
            <h1 style={{ fontSize: 28, fontWeight: 600, letterSpacing: "-0.015em" }}>Sessions / 2026-05-24</h1>
            <h2 style={{ fontSize: 20, fontWeight: 600, letterSpacing: "-0.01em", marginTop: 6 }}>Renovatie Stationsplein</h2>
            <h3 style={{ fontSize: 16, fontWeight: 600, marginTop: 4 }}>Audit entries · 14</h3>
          </div>
          <hr className="sw-divider"/>
          <div>
            <div className="sw-eyebrow">Body / labels</div>
            <p style={{ fontSize: 14 }}>Body 14 — Sentence case. No trailing periods on labels or buttons.</p>
            <p style={{ fontSize: 13, color: "var(--color-muted)", marginTop: 2 }}>Small 13 — used inside cards, table cells.</p>
            <p style={{ fontSize: 12, color: "var(--color-muted)", marginTop: 2 }}>Caption 12 — table footers, hints.</p>
            <p className="sw-eyebrow" style={{ marginTop: 6 }}>Eyebrow 11 · uppercased</p>
          </div>
          <hr className="sw-divider"/>
          <div>
            <div className="sw-eyebrow">Mono · Geist Mono · tabular-nums</div>
            <div className="sw-mono">€ 4.500,00 · 7h 30m · 2026-05-24T07:32:00Z · w-42</div>
          </div>
        </div>
      </DCArtboard>

      <DCArtboard id="space-radius" label="Spacing · radius · density" width={420} height={520}>
        <div className="sw-art sw-stack-4">
          <div>
            <div className="sw-h">Spacing scale · 4px base</div>
            <div style={{ display: "flex", gap: 8, alignItems: "flex-end", marginTop: 8 }}>
              {[4,8,12,16,20,24,32,48].map((n) => (
                <div key={n} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>
                  <div style={{ width: n, height: n, background: "var(--color-accent-soft)", border: "var(--hairline) solid var(--color-accent)", borderRadius: 3 }}/>
                  <span style={{ fontSize: 10, color: "var(--color-muted)", fontFamily: "var(--font-mono)" }}>{n}</span>
                </div>
              ))}
            </div>
          </div>
          <hr className="sw-divider"/>
          <div>
            <div className="sw-h">Radius</div>
            <div style={{ display: "flex", gap: 12, alignItems: "flex-end", marginTop: 8 }}>
              {[4,6,8,12,16].map((n) => (
                <div key={n} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>
                  <div style={{ width: 48, height: 48, background: "var(--color-card)", border: "var(--hairline) solid var(--color-border-strong)", borderRadius: n }}/>
                  <span style={{ fontSize: 10, color: "var(--color-muted)", fontFamily: "var(--font-mono)" }}>{n}px</span>
                </div>
              ))}
              <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>
                <div style={{ width: 48, height: 48, background: "var(--color-card)", border: "var(--hairline) solid var(--color-border-strong)", borderRadius: 999 }}/>
                <span style={{ fontSize: 10, color: "var(--color-muted)", fontFamily: "var(--font-mono)" }}>pill</span>
              </div>
            </div>
            <div style={{ fontSize: 11, color: "var(--color-muted)", marginTop: 8 }}>Inputs / small buttons → 6 · Cards → 8–12 · Pills → full</div>
          </div>
          <hr className="sw-divider"/>
          <div>
            <div className="sw-h">Density</div>
            <div className="sw-kv">
              <dt>Field touch</dt><dd>≥ 44px</dd>
              <dt>Field button (primary)</dt><dd>≥ 56px</dd>
              <dt>Back-office row</dt><dd>32–36px</dd>
              <dt>Back-office table cell</dt><dd>8px vertical pad</dd>
              <dt>Mobile min font</dt><dd>14px</dd>
              <dt>Back-office min font</dt><dd>12px</dd>
            </div>
          </div>
          <hr className="sw-divider"/>
          <div>
            <div className="sw-h">Borders, not shadows</div>
            <p style={{ fontSize: 11, color: "var(--color-muted)", margin: 0 }}>Body chrome uses 0.5px hairlines. Shadows are reserved for floating elements: popovers, dropdowns, command palette, toasts.</p>
          </div>
        </div>
      </DCArtboard>

      <DCArtboard id="icons" label="Icons · Lucide 1.5px" width={420} height={300}>
        <div className="sw-art">
          <div className="sw-h">Icon style</div>
          <div style={{ display: "flex", gap: 14, padding: "8px 0", alignItems: "center", flexWrap: "wrap" }}>
            <I.Clock size={20}/><I.Calendar size={20}/><I.Building size={20}/><I.Layers size={20}/>
            <I.Search size={20}/><I.Filter size={20}/><I.Plus size={20}/><I.Check size={20}/>
            <I.X size={20}/><I.Alert size={20}/><I.Info size={20}/><I.Coins size={20}/>
            <I.Receipt size={20}/><I.Refresh size={20}/><I.Download size={20}/><I.Eye size={20}/>
            <I.ArrowLeftRight size={20}/><I.MoreH size={20}/>
          </div>
          <div style={{ marginTop: 12, display: "flex", gap: 8, fontSize: 11, color: "var(--color-muted)", flexWrap: "wrap" }}>
            <span className="sw-pill">stroke 1.5px</span>
            <span className="sw-pill">currentColor</span>
            <span className="sw-pill">14px inline · 16px button · 20px empty-state</span>
          </div>
          <div className="sw-note">No mixed icon libraries. If the needed glyph isn't in Lucide, flag it — don't reach for FontAwesome or invent SVG.</div>
        </div>
      </DCArtboard>

      <DCArtboard id="hairline" label="Hairline / card system" width={420} height={300}>
        <div className="sw-art">
          <div className="sw-h">Card · canonical (Diagonal halo)</div>
          <div className="card" style={{ padding: 16, marginTop: 8 }}>
            <div style={{ fontSize: 13, fontWeight: 600 }}>Light pools at the upper-left</div>
            <div style={{ fontSize: 12, color: "var(--color-muted)", marginTop: 4 }}>
              Every card carries a 135° accent gradient inner border + an up-and-left halo. Consistent across the system → reads as one signature.
            </div>
          </div>
          <div className="sw-note">Hover = background shift to <code>card-2</code>. Never a shadow lift or border-weight change.</div>
        </div>
      </DCArtboard>
    </DCSection>
  );
};

/* ═══════════════════════════════════════════════════════════════
   02 · CORE PRIMITIVES
   ═══════════════════════════════════════════════════════════════ */

SEC.Primitives = function Primitives() {
  return (
    <DCSection id="primitives" title="02 · Core primitives" subtitle="Atoms reused across both modes.">
      <DCArtboard id="buttons" label="Button · variants + states" width={520} height={360}>
        <div className="sw-art sw-stack-4">
          <div className="sw-eyebrow">Variants</div>
          <div className="sw-row">
            <Button variant="primary"><I.Check size={14}/> Approve</Button>
            <Button variant="secondary">Cancel</Button>
            <Button variant="ghost">Discard draft</Button>
            <Button variant="destructive"><I.X size={14}/> Reject proposal</Button>
          </div>
          <div className="sw-eyebrow">States</div>
          <div className="sw-row">
            <Button variant="primary"><span className="sw-spin"/> Saving…</Button>
            <Button variant="primary" disabled>Approve</Button>
            <Button variant="secondary" disabled>Cancel</Button>
          </div>
          <div className="sw-eyebrow">Size</div>
          <div className="sw-row">
            <Button variant="primary" size="sm">Small</Button>
            <Button variant="primary">Default</Button>
            <Button variant="primary" size="lg">Large</Button>
          </div>
          <div className="sw-eyebrow">Icon-only</div>
          <div className="sw-row">
            <Button variant="secondary"><I.Plus size={14}/></Button>
            <Button variant="secondary"><I.MoreH size={14}/></Button>
            <Button variant="ghost"><I.Eye size={14}/></Button>
            <Button variant="destructive"><I.X size={14}/></Button>
          </div>
          <div className="sw-note"><strong>Destructive ≠ delete.</strong> In Schakelwerk it means <em>reject</em>, <em>fail</em>, or <em>irreversible audit-impacting</em>. Delete is not a domain action.</div>
        </div>
      </DCArtboard>

      <DCArtboard id="badge-tag" label="Badge · Tag · Pill" width={420} height={300}>
        <div className="sw-art sw-stack-4">
          <div className="sw-eyebrow">Tooling DS Badge (generic)</div>
          <div className="sw-row">
            <Badge tone="pos" dot>Open</Badge>
            <Badge tone="warn" dot>Drift</Badge>
            <Badge tone="neg" dot>Stale</Badge>
            <Badge tone="info" dot>Capture</Badge>
            <Badge tone="neutral" dot>Draft</Badge>
          </div>
          <div className="sw-eyebrow">Tag · code-like</div>
          <div className="sw-row">
            <Tag>w-42</Tag>
            <Tag>prj-114</Tag>
            <Tag>ses-3098</Tag>
            <Tag>rule:v3</Tag>
          </div>
          <div className="sw-eyebrow">Pill · count / meta</div>
          <div className="sw-row">
            <span className="sw-pill">14</span>
            <span className="sw-pill info">3 proposals</span>
            <span className="sw-pill warn">no rule</span>
            <span className="sw-pill pos">ready</span>
          </div>
          <div className="sw-note">Generic <code>Badge</code> is for one-off UI state. Domain status uses the <strong>namespaced StatusBadge</strong> (§3) — never overload generic badges for enum values.</div>
        </div>
      </DCArtboard>

      <DCArtboard id="identicon" label="Identicon · opaque ID" width={420} height={260}>
        <div className="sw-art">
          <div className="sw-h">Worker / actor avatars</div>
          <div className="sw-row" style={{ marginTop: 8 }}>
            {["w-42", "w-115", "w-007", "admin-7", "admin-3", "automation-01"].map((id) => (
              <div key={id} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 4 }}>
                <Identicon id={id} size="lg"/>
                <span style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--color-muted)" }}>{id}</span>
              </div>
            ))}
          </div>
          <div className="sw-row" style={{ marginTop: 14, gap: 6 }}>
            <Identicon id="w-42"/><Identicon id="w-115"/><Identicon id="admin-7"/>
            <Identicon id="w-42" size="sm"/><Identicon id="w-115" size="sm"/><Identicon id="admin-7" size="sm"/>
          </div>
          <div className="sw-note"><strong>No profile photos.</strong> Identicons are derived deterministically from the opaque worker_id / actor_id and only that. Same ID → same pattern everywhere in the product.</div>
        </div>
      </DCArtboard>

      <DCArtboard id="kbd-spinner-skel" label="Kbd · Spinner · Skeleton · Divider · Tooltip" width={520} height={300}>
        <div className="sw-art sw-stack-4">
          <div className="sw-eyebrow">Keyboard hints · matter for field flow</div>
          <div className="sw-row">
            <div className="sw-row" style={{ gap: 4 }}><span className="sw-kbd">⌘</span><span className="sw-kbd">K</span><span style={{ fontSize: 12, color: "var(--color-muted)", marginLeft: 4 }}>open command palette</span></div>
            <div className="sw-row" style={{ gap: 4 }}><span className="sw-kbd">Space</span><span style={{ fontSize: 12, color: "var(--color-muted)", marginLeft: 4 }}>clock in/out</span></div>
            <div className="sw-row" style={{ gap: 4 }}><span className="sw-kbd">T</span><span style={{ fontSize: 12, color: "var(--color-muted)", marginLeft: 4 }}>travel</span></div>
            <div className="sw-row" style={{ gap: 4 }}><span className="sw-kbd">O</span><span style={{ fontSize: 12, color: "var(--color-muted)", marginLeft: 4 }}>on-site</span></div>
          </div>
          <div className="sw-eyebrow">Spinner · Loading</div>
          <div className="sw-row">
            <span className="sw-spin"/>
            <span style={{ fontSize: 12, color: "var(--color-muted)" }}>14px, accent rim</span>
          </div>
          <div className="sw-eyebrow">Skeleton</div>
          <div className="sw-stack-2" style={{ width: 280 }}>
            <div className="sw-skel" style={{ height: 12, width: "70%" }}/>
            <div className="sw-skel" style={{ height: 12, width: "92%" }}/>
            <div className="sw-skel" style={{ height: 28, width: "100%", borderRadius: 6 }}/>
          </div>
          <div className="sw-eyebrow">Divider · Tooltip</div>
          <hr className="sw-divider"/>
          <div className="sw-row">
            <span style={{ position: "relative", display: "inline-block" }}>
              <span style={{
                position: "absolute", bottom: "calc(100% + 6px)", left: "50%", transform: "translateX(-50%)",
                background: "var(--color-fg)", color: "var(--color-bg)",
                fontSize: 11, padding: "4px 8px", borderRadius: 4, whiteSpace: "nowrap",
              }}>Recorded as ISO UTC</span>
              <span style={{
                position: "absolute", bottom: "calc(100% + 2px)", left: "50%", transform: "translateX(-50%)",
                width: 0, height: 0, borderLeft: "4px solid transparent", borderRight: "4px solid transparent", borderTop: "4px solid var(--color-fg)",
              }}/>
              <span className="sw-kbd">UTC</span>
            </span>
          </div>
        </div>
      </DCArtboard>
    </DCSection>
  );
};

/* ═══════════════════════════════════════════════════════════════
   03 · STATUS & ENUM NAMESPACES
   ═══════════════════════════════════════════════════════════════ */

SEC.Status = function StatusSection() {
  const renderNs = (ns, title, sub) => (
    <div className="sw-stack-3">
      <div>
        <div className="sw-eyebrow">{ns}</div>
        <div style={{ fontSize: 13, fontWeight: 600, marginTop: 2 }}>{title}</div>
        <div style={{ fontSize: 11, color: "var(--color-muted)", marginTop: 2 }}>{sub}</div>
      </div>
      <div className="sw-row">
        {Object.keys(STATUS[ns]).map((v) => (
          <StatusBadge key={v} namespace={ns} value={v} showNs={false}/>
        ))}
      </div>
      <div className="sw-row">
        {Object.keys(STATUS[ns]).slice(0, 3).map((v) => (
          <StatusBadge key={v} namespace={ns} value={v} showNs/>
        ))}
      </div>
    </div>
  );

  return (
    <DCSection id="status" title="03 · Status namespaces" subtitle="Same label means different things in different namespaces. The component takes (namespace, value) — never just value.">
      <DCArtboard id="ns-work" label="work_session" width={420} height={300}>
        <div className="sw-art">
          {renderNs("work_session", "Work session lifecycle", "Field clock-in/out plus correction lifecycle.")}
        </div>
      </DCArtboard>
      <DCArtboard id="ns-prop" label="proposal" width={420} height={260}>
        <div className="sw-art">
          {renderNs("proposal", "Automation proposal", "Approve = writes audit. Reject = writes audit. Pending = no canonical mutation.")}
        </div>
      </DCArtboard>
      <DCArtboard id="ns-book" label="bookkeeping" width={420} height={300}>
        <div className="sw-art">
          {renderNs("bookkeeping", "Bookkeeping export", "DRAFT mutates freely. READY locks for export. EXPORTED is immutable.")}
          <div className="sw-note" style={{ marginTop: 8 }}><span className="sw-needs-api">needs API</span> &nbsp; READY/EXPORTED transitions show in this canvas but the corresponding endpoints don't exist yet.</div>
        </div>
      </DCArtboard>
      <DCArtboard id="ns-cap" label="capture" width={420} height={300}>
        <div className="sw-art">
          {renderNs("capture", "Capture pipeline", "Gate-scan / timesheet imports / device events. SKIPPED ≠ FAILED — explicit guardrail decision.")}
        </div>
      </DCArtboard>
      <DCArtboard id="ns-prj" label="project" width={420} height={300}>
        <div className="sw-art">
          {renderNs("project", "Project lifecycle", "ARCHIVED hides from default queries but never deletes audit history.")}
        </div>
      </DCArtboard>

      <DCArtboard id="ns-collision" label="Same label · different meaning" width={680} height={360}>
        <div className="sw-art">
          <div className="sw-h">FAILED in three places — three different meanings</div>
          <table className="desk-table" style={{ width: "100%", fontSize: 12 }}>
            <thead>
              <tr>
                <th>Namespace</th><th>Badge</th><th>Means</th><th>Recoverable?</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><span className="sw-mono">bookkeeping</span></td>
                <td><StatusBadge namespace="bookkeeping" value="FAILED"/></td>
                <td>Export to external system rejected.</td>
                <td><span className="sw-pill pos">retryable</span></td>
              </tr>
              <tr>
                <td><span className="sw-mono">capture</span></td>
                <td><StatusBadge namespace="capture" value="FAILED"/></td>
                <td>Incoming event couldn't be parsed.</td>
                <td><span className="sw-pill pos">retryable</span></td>
              </tr>
            </tbody>
          </table>
          <hr className="sw-divider" style={{ margin: "12px 0" }}/>
          <div className="sw-h">APPROVED — two namespaces, two consequences</div>
          <table className="desk-table" style={{ width: "100%", fontSize: 12 }}>
            <thead>
              <tr><th>Namespace</th><th>Badge</th><th>Effect</th></tr>
            </thead>
            <tbody>
              <tr>
                <td><span className="sw-mono">work_session</span></td>
                <td><StatusBadge namespace="work_session" value="APPROVED"/></td>
                <td>Locks billable_minutes. Counts toward cost.</td>
              </tr>
              <tr>
                <td><span className="sw-mono">proposal</span></td>
                <td><StatusBadge namespace="proposal" value="APPROVED"/></td>
                <td>Mutates target session canonically. Writes audit_entry. Locks proposal.</td>
              </tr>
            </tbody>
          </table>
          <div className="sw-note" style={{ marginTop: 12 }}>
            <strong>Lookup contract:</strong> <code>statusRegistry(namespace, value)</code> → <code>{`{ label, tone, icon }`}</code>. There is no <code>statusRegistry(value)</code>.
          </div>
        </div>
      </DCArtboard>

      <DCArtboard id="ns-variants" label="Table & compact variants" width={680} height={240}>
        <div className="sw-art">
          <div className="sw-h">Inline · Table cell · Filter pill</div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12 }}>
            <div className="sw-tile">
              <div className="lbl">Inline (default)</div>
              <div style={{ marginTop: 8 }}><StatusBadge namespace="work_session" value="CORRECTION_PROPOSED"/></div>
            </div>
            <div className="sw-tile">
              <div className="lbl">Compact · table cell</div>
              <div style={{ marginTop: 8 }}><StatusBadge namespace="work_session" value="CORRECTION_PROPOSED" showNs={false}/></div>
            </div>
            <div className="sw-tile">
              <div className="lbl">Filter pill · active</div>
              <div style={{ marginTop: 8 }}>
                <span className="sw-pill warn" style={{ padding: "3px 8px" }}>
                  <I.Filter size={10}/> CORRECTION_PROPOSED <I.X size={10}/>
                </span>
              </div>
            </div>
          </div>
        </div>
      </DCArtboard>
    </DCSection>
  );
};

window.SEC = SEC;
