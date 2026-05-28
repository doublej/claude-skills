/* Sections 07-10 — overlays, layout, composites, build-first utilities */

/* ═══════════════════════════════════════════════════════════════
   07 · OVERLAYS & CONTAINERS
   ═══════════════════════════════════════════════════════════════ */

SEC.Overlays = function OverlaysSection() {
  return (
    <DCSection id="overlays" title="07 · Overlays & containers" subtitle="Edit drawer bundles ReasonPrompt + audit warning. Modals never appear without one.">
      <DCArtboard id="edit-drawer" label="Edit Drawer · bundles ReasonPrompt + audit warning" width={460} height={620}>
        <div className="sw-art flush" style={{ background: "var(--color-bg-elev)" }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "14px 16px",
                        backgroundImage: "var(--grad-divider)", backgroundRepeat: "no-repeat", backgroundPosition: "bottom", backgroundSize: "100% var(--hairline)" }}>
            <div>
              <div className="sw-eyebrow">Drawer · edit work session</div>
              <div style={{ fontSize: 13, fontWeight: 600, marginTop: 2 }}>ses-3098 · w-42 · Renovatie Stationsplein</div>
            </div>
            <Button variant="ghost"><I.X size={14}/></Button>
          </div>
          <div style={{ padding: 16, display: "flex", flexDirection: "column", gap: 12 }}>
            <Field label="Clock-in (UTC)"><DateTimePicker iso="2026-05-24T07:32:00Z"/></Field>
            <Field label="Clock-out (UTC)"><DateTimePicker iso="2026-05-24T15:48:00Z" focus/></Field>
            <Field label="Session type"><SWC.SessionTypeSelector value="ON_SITE"/></Field>
            <SWC.ReasonPrompt value=""/>
            <div className="sw-alert warn">
              <span className="ico"><I.Alert size={14}/></span>
              <div>
                <b>Saving will:</b>
                <ul style={{ margin: "4px 0 0 16px", padding: 0, fontSize: 12, color: "var(--color-fg-2)" }}>
                  <li>append <code style={{ fontFamily: "var(--font-mono)" }}>audit_entry</code> attributed to admin-7</li>
                  <li>trigger calc engine rev under rule v3</li>
                  <li>recompute cost · cents</li>
                </ul>
              </div>
            </div>
          </div>
          <div style={{
            position: "absolute", bottom: 0, left: 0, right: 0,
            padding: 12, background: "var(--color-bg-elev)",
            backgroundImage: "var(--grad-divider)", backgroundRepeat: "no-repeat", backgroundPosition: "top", backgroundSize: "100% var(--hairline)",
            display: "flex", justifyContent: "space-between", gap: 6
          }}>
            <Button variant="ghost">Discard</Button>
            <div className="sw-row" style={{ gap: 6 }}>
              <Button variant="secondary">Save as draft</Button>
              <Button variant="primary"><I.Check size={14}/> Save · writes audit</Button>
            </div>
          </div>
        </div>
      </DCArtboard>

      <DCArtboard id="modal" label="Modal · compact confirm" width={460} height={360}>
        <div className="sw-art" style={{ background: "#00000022", display: "grid", placeItems: "center" }}>
          <div className="card" style={{ padding: 0, width: 380, background: "var(--color-bg-elev)" }}>
            <div style={{ padding: 18 }}>
              <h3 style={{ fontSize: 15 }}>Publish rule v4</h3>
              <p style={{ fontSize: 12.5, color: "var(--color-fg-2)", marginTop: 8, lineHeight: 1.5 }}>
                Creates a new immutable version. Sessions closed before publish keep rule v3. Open sessions adopt v4 on next clock-out.
              </p>
            </div>
            <div style={{ padding: 12,
              backgroundImage: "var(--grad-divider)", backgroundRepeat: "no-repeat", backgroundPosition: "top", backgroundSize: "100% var(--hairline)",
              display: "flex", justifyContent: "flex-end", gap: 6 }}>
              <Button variant="ghost">Cancel</Button>
              <Button variant="primary">Publish v4</Button>
            </div>
          </div>
        </div>
      </DCArtboard>

      <DCArtboard id="popover" label="Popover · DropdownMenu" width={460} height={360}>
        <div className="sw-art">
          <div className="sw-h">Row · kebab menu</div>
          <div style={{ position: "relative", marginTop: 8, display: "inline-block" }}>
            <Button variant="secondary"><I.MoreH size={14}/></Button>
            <div className="popover" style={{ position: "absolute", top: 36, left: 0, minWidth: 220 }}>
              <div className="item"><I.Eye/> View calculation snapshot <span className="meta">⌘↵</span></div>
              <div className="item"><I.Refresh/> Recompute under rule v3</div>
              <div className="item"><I.Receipt/> Add to bookkeeping draft</div>
              <hr className="sep"/>
              <div className="item" style={{ color: "var(--color-neg)" }}><I.X/> Reject session</div>
            </div>
          </div>
        </div>
      </DCArtboard>

      <DCArtboard id="tabs-accordion" label="Tabs · Accordion" width={520} height={420}>
        <div className="sw-art sw-stack-4">
          <div className="sw-eyebrow">Tabs · scoped to PageHeader</div>
          <div style={{
            display: "flex", gap: 16,
            backgroundImage: "var(--grad-divider)", backgroundRepeat: "no-repeat", backgroundPosition: "bottom", backgroundSize: "100% var(--hairline)"
          }}>
            {["Overview", "Sessions", "Audit", "Bookkeeping", "Settings"].map((t,i) => (
              <button key={t} className={`tab ${i === 1 ? "active" : ""}`} style={{
                fontSize: 13, padding: "10px 0", border: 0, background: "transparent",
                color: i === 1 ? "var(--color-fg)" : "var(--color-muted)",
                fontWeight: i === 1 ? 500 : 400, position: "relative", cursor: "pointer"
              }}>
                {t}
                {t === "Bookkeeping" && <span className="sw-pill warn" style={{ marginLeft: 6, fontSize: 9 }}>1</span>}
                {i === 1 && <span style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 2, background: "var(--color-fg)" }}/>}
              </button>
            ))}
          </div>
          <div className="sw-eyebrow">Accordion · expand for audit detail</div>
          <div className="card" style={{ padding: 0 }}>
            {[
              { title: "audit_entry · aud-90211", open: true,  meta: "APPROVE_PROPOSAL" },
              { title: "audit_entry · aud-90208", open: false, meta: "CREATE_PROPOSAL" },
              { title: "audit_entry · aud-90201", open: false, meta: "EDIT" },
            ].map((row, i) => (
              <div key={i} style={{
                padding: "10px 14px",
                backgroundImage: "var(--grad-divider)", backgroundRepeat: "no-repeat",
                backgroundPosition: "bottom", backgroundSize: "100% var(--hairline)"
              }}>
                <div className="sw-row" style={{ justifyContent: "space-between" }}>
                  <div className="sw-row" style={{ gap: 6 }}>
                    <I.ChevronRight size={12} style={{ transform: row.open ? "rotate(90deg)" : "none", transition: "transform 120ms" }}/>
                    <span style={{ fontFamily: "var(--font-mono)", fontSize: 12 }}>{row.title}</span>
                  </div>
                  <span className="sw-pill info" style={{ fontSize: 10 }}>{row.meta}</span>
                </div>
                {row.open && (
                  <div style={{ marginTop: 8, paddingLeft: 18, fontSize: 12, color: "var(--color-fg-2)" }}>
                    “Gate-scan correction confirmed by ops manager.”
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </DCArtboard>
    </DCSection>
  );
};

/* ═══════════════════════════════════════════════════════════════
   08 · LAYOUT & NAVIGATION
   ═══════════════════════════════════════════════════════════════ */

SEC.Layout = function LayoutSection() {
  return (
    <DCSection id="layout" title="08 · Layout & navigation" subtitle="Two app shells. Same components, different density rules.">
      <DCArtboard id="field-shell" label="Field-worker shell · mobile" width={380} height={760}>
        <div className="sw-art flush" style={{ background: "transparent", display: "grid", placeItems: "center" }}>
          <PhoneFrame>
            <div className="statusbar">
              <span>09:32</span>
              <span style={{ display: "flex", gap: 6, alignItems: "center" }}>
                <span style={{ fontSize: 10 }}>5G</span>
                <span style={{ width: 18, height: 9, border: "1px solid currentColor", borderRadius: 2, position: "relative" }}>
                  <span style={{ position: "absolute", inset: 1, background: "currentColor", borderRadius: 1, width: "70%" }}/>
                </span>
              </span>
            </div>
            <div className="topbar">
              <Identicon id="w-42" size="sm"/>
              <div>
                <div style={{ fontSize: 13, fontWeight: 600 }}>w-42</div>
                <div style={{ fontSize: 10, color: "var(--color-muted)" }}>Renovatie Stationsplein</div>
              </div>
              <div style={{ marginLeft: "auto" }}>
                <StatusBadge namespace="work_session" value="OPEN" showNs={false}/>
              </div>
            </div>
            <div className="body">
              <div style={{ textAlign: "center", padding: "8px 0 16px" }}>
                <div className="sw-eyebrow">Open session · clock-in</div>
                <div style={{
                  fontFamily: "var(--font-display)", fontSize: 56, lineHeight: 1, marginTop: 8,
                  fontVariantNumeric: "tabular-nums lining-nums", letterSpacing: "-0.02em"
                }}>07:32</div>
                <div style={{ fontSize: 11, color: "var(--color-muted)", fontFamily: "var(--font-mono)", marginTop: 4 }}>2026-05-24 · UTC</div>
              </div>
              <div style={{ marginBottom: 12 }}>
                <SWC.SessionTypeSelector value="ON_SITE" lg/>
              </div>
              <div className="sw-stack-3">
                <button className="sw-touch destructive">
                  <span><I.X size={18}/> Clock out</span>
                  <span className="meta">SPACE</span>
                </button>
                <button className="sw-touch">
                  <span>Switch project</span>
                  <I.Chevron size={16}/>
                </button>
                <button className="sw-touch">
                  <span>Add note · gets recorded</span>
                  <I.Receipt size={16}/>
                </button>
              </div>
              <div className="sw-note" style={{ marginTop: 16, fontSize: 10 }}>
                <strong>Gloves on.</strong> Targets are ≥56px. Status flips in one tap. No fragile dropdowns.
              </div>
            </div>
            <div className="tabbar">
              <div className="item active"><I.Clock className="ico"/>Now</div>
              <div className="item"><I.Layers className="ico"/>Project</div>
              <div className="item"><I.Receipt className="ico"/>History</div>
            </div>
          </PhoneFrame>
        </div>
      </DCArtboard>

      <DCArtboard id="back-office-shell" label="Back-office shell · desktop" width={1180} height={760}>
        <div className="sw-art flush">
          <div className="sw-page">
            {/* sticky topnav · matches Tooling DS finance index */}
            <nav className="topnav" aria-label="Primary" style={{ position: "relative" }}>
              <a className="brand" role="button" tabIndex={0}>
                <span style={{
                  width: 22, height: 22, borderRadius: 5,
                  background: "var(--color-fg)", color: "var(--color-bg)",
                  display: "grid", placeItems: "center",
                  fontSize: 11, fontFamily: "var(--font-mono)", fontWeight: 600
                }}>SW</span>
                <span>Schakelwerk</span>
              </a>
              <button className="navitem desktop-only">Overview</button>
              <button className="navitem desktop-only">Sessions</button>
              <button className="navitem desktop-only" aria-current="page">
                Proposals
                <span className="sw-pill warn" style={{ marginLeft: 4, padding: "0 5px", fontSize: 9 }}>3</span>
              </button>
              <button className="navitem desktop-only">Audit <span className="chev"><I.Chevron size={12}/></span></button>
              <button className="navitem desktop-only">Projects <span className="chev"><I.Chevron size={12}/></span></button>
              <button className="navitem desktop-only">Bookkeeping</button>
              <div className="right">
                <button className="searchbtn" aria-label="Open command palette">
                  <I.Search size={14} className="ico"/>
                  <span className="placeholder">Search sessions, workers…</span>
                  <span className="kbd">⌘K</span>
                </button>
                <button className="iconbtn" title="Notifications"><span className="ico"><I.Bell size={16}/></span></button>
                <button className="iconbtn" title="Theme"><span className="ico"><I.CircleCheck size={16}/></span></button>
                <div className="avatar" aria-hidden="true">A7</div>
              </div>
            </nav>

            {/* scrollable centered column */}
            <div className="scroll">
              <div className="col">

                {/* Page header */}
                <div>
                  <div style={{ fontSize: 11, color: "var(--color-muted)", textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 6 }}>
                    <span style={{ color: "var(--color-muted)" }}>Operations</span>
                    <span style={{ margin: "0 6px", color: "var(--color-muted-2)" }}>/</span>
                    <span style={{ color: "var(--color-fg-2)" }}>Proposals</span>
                  </div>
                  <div style={{
                    display: "flex", alignItems: "flex-end", gap: 12, paddingBottom: 14,
                    backgroundImage: "var(--grad-divider)", backgroundRepeat: "no-repeat",
                    backgroundPosition: "bottom", backgroundSize: "100% var(--hairline)"
                  }}>
                    <div>
                      <h1 style={{ fontSize: 28, fontWeight: 600, letterSpacing: "-0.015em", margin: 0 }}>Proposals</h1>
                      <div style={{ fontSize: 13, color: "var(--color-muted)", marginTop: 4 }}>
                        3 pending · 124 approved this month · 8 rejected
                      </div>
                    </div>
                    <div style={{ marginLeft: "auto", display: "flex", gap: 6 }}>
                      <Button variant="secondary"><I.Download size={14}/> Export</Button>
                      <Button variant="secondary"><I.Refresh size={14}/></Button>
                    </div>
                  </div>
                  <div style={{ display: "flex", gap: 16, marginTop: 4,
                                backgroundImage: "var(--grad-divider)", backgroundRepeat: "no-repeat",
                                backgroundPosition: "bottom", backgroundSize: "100% var(--hairline)" }}>
                    {[
                      { label: "Pending", count: 3, active: true },
                      { label: "Approved", count: 124 },
                      { label: "Rejected", count: 8 },
                      { label: "All", count: 218 },
                    ].map((t,i) => (
                      <button key={t.label} className={`tab ${t.active ? "active" : ""}`} style={{
                        background: "transparent", border: 0,
                        padding: "10px 0", marginBottom: -1, cursor: "pointer",
                        fontSize: 13, color: t.active ? "var(--color-fg)" : "var(--color-muted)",
                        fontWeight: t.active ? 500 : 400, position: "relative",
                      }}>
                        {t.label}
                        <span style={{
                          marginLeft: 6, fontFamily: "var(--font-mono)", fontSize: 10,
                          color: "var(--color-muted)",
                        }}>{t.count}</span>
                        {t.active && <span style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 2,
                          background: "linear-gradient(90deg, transparent 0%, var(--color-fg) 15%, var(--color-fg) 85%, transparent 100%)" }}/>}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Stat strip · plain cards */}
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: 16 }}>
                  <StatTile label="Pending" value={<span style={{ fontFamily: "var(--font-display)", fontSize: 28, fontWeight: 400 }}>3</span>} sub="1 today"/>
                  <StatTile label="Avg confidence" value={<span style={{ fontFamily: "var(--font-display)", fontSize: 28, fontWeight: 400 }}>78%</span>} sub="across pending"/>
                  <StatTile label="Cost delta if all approved" cents={9650} sub="+12m billable median"/>
                  <StatTile label="Oldest pending" value={<span style={{ fontFamily: "var(--font-mono)", fontSize: 20, color: "var(--color-warn)" }}>9h 24m</span>} sub="prop-1404"/>
                </div>

                {/* Filter bar */}
                <div style={{
                  display: "flex", gap: 6, alignItems: "center", padding: "10px 12px",
                  background: "var(--color-card)",
                  border: "var(--hairline) solid var(--color-border)",
                  borderRadius: 8,
                  boxShadow: "var(--hairline-highlight)"
                }}>
                  <div className="sw-input" style={{ height: 30, width: 240, border: 0, boxShadow: "none", background: "var(--color-card-2)" }}>
                    <I.Search size={13}/><span style={{ fontSize: 12, color: "var(--color-muted-2)" }}>Filter by worker, session, type…</span>
                  </div>
                  <Button variant="ghost" size="sm"><I.Filter size={12}/> Type</Button>
                  <Button variant="ghost" size="sm"><I.Calendar size={12}/> Period · last 7d</Button>
                  <Button variant="ghost" size="sm"><I.Coins size={12}/> Cost delta</Button>
                  <div style={{ marginLeft: "auto", display: "flex", gap: 8, alignItems: "center", fontSize: 11, color: "var(--color-muted)" }}>
                    <span className="sw-pill"><I.CircleDot size={10}/> saved view · "Daily review"</span>
                  </div>
                </div>

                {/* Proposals table · plain card */}
                <div className="sw-card flush">
                  <div className="head">
                    <h3>Pending proposals</h3>
                    <div className="sub">3 awaiting decision</div>
                    <div className="actions">
                      <Button variant="ghost" size="sm"><I.MoreH size={14}/></Button>
                    </div>
                  </div>
                  <div className="body flush">
                    <table className="sw-table">
                      <thead>
                        <tr>
                          <th style={{ width: 36 }}></th>
                          <th>Proposal</th>
                          <th>Type</th>
                          <th>Target</th>
                          <th>Confidence</th>
                          <th className="num">Cost Δ</th>
                          <th>Created · UTC</th>
                          <th>Status</th>
                          <th></th>
                        </tr>
                      </thead>
                      <tbody>
                        {[
                          { id: "prop-1408", type: "clock_out_correction", target: "ses-3098", worker: "w-42", conf: 82, delta: 3450, when: "2026-05-24T16:12Z" },
                          { id: "prop-1407", type: "session_split",        target: "ses-3094", worker: "w-115", conf: 71, delta: -1200, when: "2026-05-24T13:48Z" },
                          { id: "prop-1404", type: "missed_clock_out",     target: "ses-3091", worker: "w-007", conf: 64, delta: 7800, when: "2026-05-24T08:09Z" },
                        ].map((r) => (
                          <tr key={r.id}>
                            <td><Radio/></td>
                            <td><span className="sw-mono">{r.id}</span></td>
                            <td><span style={{ fontFamily: "var(--font-mono)", fontSize: 11.5 }}>{r.type}</span></td>
                            <td>
                              <div className="sw-row" style={{ gap: 6 }}>
                                <Identicon id={r.worker} size="sm"/>
                                <span style={{ fontFamily: "var(--font-mono)", fontSize: 11.5 }}>{r.target}</span>
                              </div>
                            </td>
                            <td>
                              <div className="sw-conf">
                                <span className="bar"><i style={{ width: `${r.conf}%` }}/></span>
                                <span>{r.conf}%</span>
                              </div>
                            </td>
                            <td className="num">
                              <span style={{ color: r.delta >= 0 ? "var(--color-pos)" : "var(--color-neg)" }}>
                                {r.delta >= 0 ? "+" : "−"}<MoneyDisplay cents={Math.abs(r.delta)}/>
                              </span>
                            </td>
                            <td><span style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--color-muted)" }}>{r.when}</span></td>
                            <td><StatusBadge namespace="proposal" value="PENDING" showNs={false}/></td>
                            <td className="row-actions">
                              <Button variant="ghost" size="sm"><I.ChevronRight size={14}/></Button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                <div className="sw-note" style={{ marginTop: 4 }}>
                  <strong>Layout convention.</strong> Sticky topnav, centered <code>max-width: 1100px</code> column, plain hairline cards. The <code>.card</code> with the diagonal accent halo is reserved for <strong>hero cards</strong> — the CalculationSnapshotCard at the top of a session view, the active ProposalCard in review, the cost summary on a project dashboard. Everywhere else, use <code>.sw-card</code>.
                </div>
              </div>
            </div>
          </div>
        </div>
      </DCArtboard>

      <DCArtboard id="toolbar-pageheader" label="PageHeader · Toolbar · Breadcrumbs" width={760} height={300}>
        <div className="sw-art">
          <div style={{ fontSize: 11, color: "var(--color-muted)", textTransform: "uppercase", letterSpacing: "0.06em" }}>
            <a style={{ color: "var(--color-muted)", textDecoration: "none" }}>Customers</a>
            <span style={{ margin: "0 6px", color: "var(--color-muted-2)" }}>/</span>
            <a style={{ color: "var(--color-muted)", textDecoration: "none" }}>Bouwbedrijf Van Dijk</a>
            <span style={{ margin: "0 6px", color: "var(--color-muted-2)" }}>/</span>
            <span style={{ color: "var(--color-fg-2)" }}>Renovatie Stationsplein</span>
          </div>
          <div style={{ display: "flex", alignItems: "flex-end", gap: 12, padding: "10px 0 14px",
                        backgroundImage: "var(--grad-divider)", backgroundRepeat: "no-repeat",
                        backgroundPosition: "bottom", backgroundSize: "100% var(--hairline)" }}>
            <div>
              <h1 style={{ fontSize: 24, fontWeight: 600, letterSpacing: "-0.015em" }}>Renovatie Stationsplein</h1>
              <div style={{ fontSize: 12, color: "var(--color-muted)", marginTop: 2 }}>
                prj-114 · rule v3 · 47 sessions · 12 workers
              </div>
            </div>
            <div style={{ marginLeft: "auto" }} className="sw-row">
              <StatusBadge namespace="project" value="ACTIVE" showNs={false}/>
              <Button variant="secondary"><I.Download size={14}/> Export</Button>
              <Button variant="primary"><I.Plus size={14}/> New session</Button>
            </div>
          </div>
          <div className="sw-row" style={{ marginTop: 12 }}>
            <div className="sw-input" style={{ height: 30, width: 220 }}>
              <I.Search size={13}/><span style={{ fontSize: 12, color: "var(--color-muted-2)" }}>Filter sessions</span>
            </div>
            <Button variant="secondary"><I.Filter size={13}/> Status</Button>
            <Button variant="secondary"><I.Calendar size={13}/> Period · last 7d</Button>
            <Button variant="secondary"><I.Refresh size={13}/></Button>
            <div style={{ marginLeft: "auto" }}>
              <span className="sw-pill"><I.CircleDot size={10}/> 4 filters · saved view</span>
            </div>
          </div>
        </div>
      </DCArtboard>
    </DCSection>
  );
};

/* ═══════════════════════════════════════════════════════════════
   09 · DOMAIN COMPOSITES
   ═══════════════════════════════════════════════════════════════ */

SEC.Composites = function CompositesSection() {
  return (
    <DCSection id="composites" title="09 · Domain composites" subtitle="The trust story — where the system stops being generic and starts being Schakelwerk.">
      <DCArtboard id="customer-picker" label="CustomerPicker · open" width={460} height={300}>
        <div className="sw-art">
          <SWC.CustomerPicker open value="Bouwbedrijf Van Dijk"/>
        </div>
      </DCArtboard>

      <DCArtboard id="project-picker" label="ProjectPicker · rule-aware" width={520} height={320}>
        <div className="sw-art">
          <SWC.ProjectPicker open value="Renovatie Stationsplein"/>
          <div className="sw-note">A project without a <strong>published rule</strong> shows a <code>no rule</code> pill. Sessions on such projects are blocked from clock-in (engine guardrail).</div>
        </div>
      </DCArtboard>

      <DCArtboard id="worker-id" label="WorkerIdField · opaque + recent" width={460} height={260}>
        <div className="sw-art">
          <SWC.WorkerIdField value="w-42"/>
          <div className="sw-note">Free string field. No directory lookup. Recent values come from <strong>local device memory</strong> only — not server state.</div>
        </div>
      </DCArtboard>

      <DCArtboard id="session-type-comp" label="SessionTypeSelector · field-primary" width={460} height={220}>
        <div className="sw-art">
          <div className="sw-eyebrow">Top-level control · field mode</div>
          <div style={{ marginTop: 10 }}>
            <SWC.SessionTypeSelector value="ON_SITE" lg/>
          </div>
          <div className="sw-note">Travel and on-site billing rules are different. Buried in a dropdown this becomes the #1 source of wrong invoices — keep it loud.</div>
        </div>
      </DCArtboard>

      <DCArtboard id="rule-params" label="RuleParamsForm · publishes v4" width={460} height={620}>
        <div className="sw-art">
          <SWC.RuleParamsForm/>
        </div>
      </DCArtboard>

      <DCArtboard id="reason-prompt" label="ReasonPrompt · permanent, audit-relevant" width={420} height={260}>
        <div className="sw-art">
          <SWC.ReasonPrompt value="Worker confirmed late clock-out via gate-scan after standup."/>
          <div className="sw-note">Empty submit is a 400, not a UI prevention — the engine is the single source of truth.</div>
        </div>
      </DCArtboard>

      <DCArtboard id="calc-snapshot" label="CalculationSnapshotCard · deterministic" width={560} height={620}>
        <div className="sw-art">
          <SWC.CalculationSnapshotCard/>
        </div>
      </DCArtboard>

      <DCArtboard id="audit-row-collapsed" label="AuditEntryRow · collapsed" width={620} height={120}>
        <div className="sw-art flush">
          <SWC.AuditEntryRow/>
        </div>
      </DCArtboard>

      <DCArtboard id="audit-row-expanded" label="AuditEntryRow · expanded" width={620} height={520}>
        <div className="sw-art flush">
          <SWC.AuditEntryRow expanded/>
        </div>
      </DCArtboard>

      <DCArtboard id="proposal-card" label="ProposalCard · AI/automation boundary" width={560} height={760}>
        <div className="sw-art">
          <SWC.ProposalCard/>
        </div>
      </DCArtboard>

      <DCArtboard id="cost-summary" label="CostSummaryPanel · no_rate_configured" width={760} height={400}>
        <div className="sw-art">
          <SWC.CostSummaryPanel/>
        </div>
      </DCArtboard>
    </DCSection>
  );
};

/* ═══════════════════════════════════════════════════════════════
   10 · BUILD FIRST — utilities & contracts
   ═══════════════════════════════════════════════════════════════ */

SEC.BuildFirst = function BuildFirstSection() {
  return (
    <DCSection id="build-first" title="10 · Build first" subtitle="Three utilities every other component depends on. Land them before any UI screen.">
      <DCArtboard id="status-registry" label="statusRegistry · (namespace, value) → meta" width={620} height={520}>
        <div className="sw-art">
          <div className="sw-h">Contract</div>
          <pre style={{
            fontFamily: "var(--font-mono)", fontSize: 11.5,
            background: "var(--color-card-2)", border: "var(--hairline) solid var(--color-border)",
            borderRadius: 6, padding: 12, margin: 0, lineHeight: 1.6, overflow: "auto"
          }}>{`type Namespace =
  | "work_session" | "proposal" | "bookkeeping"
  | "capture"      | "project";

statusRegistry(ns: Namespace, value: string): {
  label: string;
  tone:  "open" | "closed" | "proposed" | "approved"
       | "rejected" | "pending" | "ready" | "exported"
       | "failed" | "received" | "processed" | "skipped"
       | "draft" | "active" | "paused" | "completed" | "archived";
  icon:  IconName;
}`}</pre>
          <div className="sw-h" style={{ marginTop: 14 }}>Test matrix · same label across namespaces</div>
          <table className="desk-table" style={{ width: "100%" }}>
            <thead><tr><th>label</th><th>work_session</th><th>proposal</th><th>bookkeeping</th><th>capture</th></tr></thead>
            <tbody>
              <tr>
                <td><span className="sw-mono">APPROVED</span></td>
                <td><StatusBadge namespace="work_session" value="APPROVED" showNs={false}/></td>
                <td><StatusBadge namespace="proposal" value="APPROVED" showNs={false}/></td>
                <td><span style={{ color: "var(--color-muted-2)" }}>—</span></td>
                <td><span style={{ color: "var(--color-muted-2)" }}>—</span></td>
              </tr>
              <tr>
                <td><span className="sw-mono">FAILED</span></td>
                <td><span style={{ color: "var(--color-muted-2)" }}>—</span></td>
                <td><span style={{ color: "var(--color-muted-2)" }}>—</span></td>
                <td><StatusBadge namespace="bookkeeping" value="FAILED" showNs={false}/></td>
                <td><StatusBadge namespace="capture" value="FAILED" showNs={false}/></td>
              </tr>
              <tr>
                <td><span className="sw-mono">DRAFT</span></td>
                <td><span style={{ color: "var(--color-muted-2)" }}>—</span></td>
                <td><span style={{ color: "var(--color-muted-2)" }}>—</span></td>
                <td><StatusBadge namespace="bookkeeping" value="DRAFT" showNs={false}/></td>
                <td><span style={{ color: "var(--color-muted-2)" }}>—</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </DCArtboard>

      <DCArtboard id="money-util" label="money · cents ↔ Dutch euro" width={620} height={480}>
        <div className="sw-art">
          <div className="sw-h">Contract</div>
          <pre style={{
            fontFamily: "var(--font-mono)", fontSize: 11.5,
            background: "var(--color-card-2)", border: "var(--hairline) solid var(--color-border)",
            borderRadius: 6, padding: 12, margin: 0, lineHeight: 1.6, overflow: "auto"
          }}>{`fmtMoneyCents(cents: number, opts?): string
parseEuroString(str: string): number /* cents */

// All UI props are typed \`cents: number | null\`.
// null  →  no_rate_configured
// 0     →  literal € 0,00 (rare; usually means clean-state)`}</pre>
          <div className="sw-h" style={{ marginTop: 14 }}>Fixtures</div>
          <table className="desk-table" style={{ width: "100%" }}>
            <thead><tr><th>cents</th><th>fmtMoneyCents</th><th>UI</th></tr></thead>
            <tbody>
              <tr><td>450000</td><td><span className="sw-mono">"€ 4.500,00"</span></td><td><MoneyDisplay cents={450000}/></td></tr>
              <tr><td>31500</td><td><span className="sw-mono">"€ 315,00"</span></td><td><MoneyDisplay cents={31500}/></td></tr>
              <tr><td>42</td><td><span className="sw-mono">"€ 0,42"</span></td><td><MoneyDisplay cents={42}/></td></tr>
              <tr><td>0</td><td><span className="sw-mono">"€ 0,00"</span></td><td><MoneyDisplay cents={0}/></td></tr>
              <tr><td>−1200</td><td><span className="sw-mono">"−€ 12,00"</span></td><td><MoneyDisplay cents={-1200}/></td></tr>
              <tr><td><span style={{ color: "var(--color-muted)" }}>null</span></td><td><span className="sw-mono">"no_rate_configured"</span></td><td><MoneyDisplay noRate/></td></tr>
            </tbody>
          </table>
          <div className="sw-note"><strong>Never</strong> use <code>parseFloat</code> on money. Engine inputs are integer cents; display is the only place we format.</div>
        </div>
      </DCArtboard>

      <DCArtboard id="duration-util" label="duration · minutes ↔ Hh Mm" width={620} height={460}>
        <div className="sw-art">
          <div className="sw-h">Contract</div>
          <pre style={{
            fontFamily: "var(--font-mono)", fontSize: 11.5,
            background: "var(--color-card-2)", border: "var(--hairline) solid var(--color-border)",
            borderRadius: 6, padding: 12, margin: 0, lineHeight: 1.6, overflow: "auto"
          }}>{`fmtDuration(minutes: number, opts?): string
parseDuration(str: "7h 30m" | "7:30"): number /* minutes */

// Components always carry both:
//   billable_minutes:    number
//   nonbillable_minutes: number
// "Total" duration is a derived view, not the underlying field.`}</pre>
          <div className="sw-h" style={{ marginTop: 14 }}>Fixtures</div>
          <table className="desk-table" style={{ width: "100%" }}>
            <thead><tr><th>minutes</th><th>fmtDuration</th><th>UI</th></tr></thead>
            <tbody>
              <tr><td>450</td><td><span className="sw-mono">"7h 30m"</span></td><td><DurationDisplay minutes={450}/></td></tr>
              <tr><td>30</td><td><span className="sw-mono">"30m"</span></td><td><DurationDisplay minutes={30}/></td></tr>
              <tr><td>60</td><td><span className="sw-mono">"1h"</span></td><td><DurationDisplay minutes={60}/></td></tr>
              <tr><td>0</td><td><span className="sw-mono">"0m"</span></td><td><DurationDisplay minutes={0}/></td></tr>
              <tr><td><span className="sw-mono">{`{billable:405, nonBill:30}`}</span></td><td><span className="sw-mono">"6h 45m · +30m non-bill"</span></td><td><DurationDisplay billable={405} nonBillable={30}/></td></tr>
            </tbody>
          </table>
        </div>
      </DCArtboard>

      <DCArtboard id="contracts" label="What this canvas does NOT design" width={620} height={360}>
        <div className="sw-art">
          <div className="sw-h">Out of scope · stated explicitly</div>
          <ul style={{ paddingLeft: 18, fontSize: 12.5, color: "var(--color-fg-2)", lineHeight: 1.7 }}>
            <li>Login / auth. Backend auth does not exist yet.</li>
            <li>Full app pages or user flows — these are atoms, not screens.</li>
            <li>Delete as a domain action — Schakelwerk does not delete sessions, projects, or audit rows.</li>
            <li>Profile photos for workers or admins.</li>
            <li>Floating-point money anywhere in the UI layer.</li>
            <li>Local browser time as canonical — UTC is.</li>
          </ul>
          <div className="sw-h" style={{ marginTop: 12 }}>Marked <span className="sw-needs-api">needs API</span></div>
          <ul style={{ paddingLeft: 18, fontSize: 12.5, color: "var(--color-fg-2)", lineHeight: 1.7 }}>
            <li><code>bookkeeping</code> READY → EXPORTED transition is sketched but not wired.</li>
            <li>Capture pipeline retry-from-FAILED is shown but has no endpoint.</li>
          </ul>
        </div>
      </DCArtboard>
    </DCSection>
  );
};

window.SEC = SEC;
