/* Sections 04-10 — forms, data, feedback, overlays, layout, composites, utilities */

/* ═══════════════════════════════════════════════════════════════
   04 · FORM CONTROLS
   ═══════════════════════════════════════════════════════════════ */

SEC.Forms = function FormsSection() {
  return (
    <DCSection id="forms" title="04 · Form controls" subtitle="Cents-aware money, UTC-aware time, minute-typed durations.">
      <DCArtboard id="text-inputs" label="Text · Number · Select · Combobox" width={460} height={520}>
        <div className="sw-art sw-stack-4">
          <Field label="Customer name (TextInput)" hint="Free-form, 1–120 chars.">
            <TextInput value="Bouwbedrijf Van Dijk"/>
          </Field>
          <Field label="Default budget (NumberInput · raw integer)">
            <div className="sw-input">
              <span className="val">1248</span>
              <span className="suffix">units</span>
            </div>
          </Field>
          <Field label="Select · static options">
            <div className="sw-input">
              <span className="val left" style={{ fontFamily: "var(--font-sans)", textAlign: "left" }}>Round to 5 min</span>
              <I.Chevron size={14}/>
            </div>
          </Field>
          <Field label="Combobox · async with prefix match" hint="Used for ProjectPicker etc.">
            <div className="sw-input is-focus">
              <I.Search size={14}/>
              <span className="val left" style={{ fontFamily: "var(--font-sans)", textAlign: "left" }}>Renovatie<span style={{ color: "var(--color-muted-2)" }}>|</span></span>
            </div>
            <div style={{
              marginTop: 4, background: "var(--color-bg-elev)",
              border: "var(--hairline) solid var(--color-border-strong)", borderRadius: 6,
              boxShadow: "var(--shadow-sm)", overflow: "hidden", fontSize: 12,
            }}>
              {["Renovatie Stationsplein", "Renovatie Markt 14", "Renovatie Kade Noord"].map((s,i) => (
                <div key={s} style={{
                  padding: "8px 10px", background: i === 0 ? "var(--color-card-2)" : "transparent",
                  display: "flex", justifyContent: "space-between"
                }}>
                  <span><b>Renovatie</b> {s.slice(10)}</span>
                  {i === 0 && <span style={{ fontSize: 10, color: "var(--color-muted)", fontFamily: "var(--font-mono)" }}>↵</span>}
                </div>
              ))}
            </div>
          </Field>
          <Field label="MultiSelect · enum">
            <div className="sw-input" style={{ minHeight: 36, height: "auto", padding: 4, flexWrap: "wrap", gap: 4 }}>
              <span className="sw-pill"><I.X size={10}/> APPROVED</span>
              <span className="sw-pill"><I.X size={10}/> CORRECTION_PROPOSED</span>
              <span style={{ color: "var(--color-muted-2)", fontSize: 12 }}>Add…</span>
            </div>
          </Field>
        </div>
      </DCArtboard>

      <DCArtboard id="money-input" label="CurrencyInput · Dutch euros · cents" width={460} height={420}>
        <div className="sw-art sw-stack-4">
          <Field label="Budget"
            hint="Displays € 4.500,00 (NL). Stores 450000 (integer cents). No float in the UI layer.">
            <CurrencyInput cents={450000}/>
          </Field>
          <Field label="Travel rate per minute">
            <CurrencyInput cents={42}/>
          </Field>
          <Field label="Empty"><CurrencyInput cents={null}/></Field>
          <Field label="Focus state"><CurrencyInput cents={75} focus/></Field>
          <Field label="Validation error" error="Negative rates aren't supported by the engine.">
            <CurrencyInput cents={-1200} error/>
          </Field>
          <div className="sw-note">
            Component prop is <code>cents: number</code>. Onchange returns <code>cents: number</code>. The display string never round-trips through the value.
          </div>
        </div>
      </DCArtboard>

      <DCArtboard id="datetime" label="DateTimePicker · UTC-aware" width={460} height={400}>
        <div className="sw-art sw-stack-4">
          <Field label="Clock-in"
            hint="Stored as ISO 8601 UTC. The viewing timezone is a presentation choice — never canonical.">
            <DateTimePicker iso="2026-05-24T07:32:00Z"/>
          </Field>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
            <Field label="Open · with TZ pill">
              <DateTimePicker iso="2026-05-24T15:48:00Z" focus/>
            </Field>
            <Field label="Local-time preview">
              <div className="sw-input" style={{ background: "var(--color-card-2)" }}>
                <I.Eye size={14}/>
                <span className="val left" style={{ fontFamily: "var(--font-mono)", textAlign: "left" }}>17:48 · Europe/Amsterdam</span>
              </div>
            </Field>
          </div>
          <div className="sw-note">
            The picker shows UTC and the chosen viewing TZ side-by-side. The Europe/Amsterdam row is <strong>presentation only</strong> and is never persisted on its own.
          </div>
        </div>
      </DCArtboard>

      <DCArtboard id="duration" label="DurationInput · integer minutes" width={460} height={380}>
        <div className="sw-art sw-stack-4">
          <Field label="Lunch deduction" hint="Stored as integer minutes. Renders Hh Mm.">
            <DurationInput minutes={30}/>
          </Field>
          <Field label="Long session">
            <DurationInput minutes={450}/>
          </Field>
          <Field label="Negative · disallowed by engine" error="Engine rejects negative durations.">
            <div className="sw-input is-error" style={{ width: 160 }}>
              <I.Clock size={14}/>
              <span className="val" style={{ color: "var(--color-neg)" }}>−15m</span>
              <span className="suffix">min</span>
            </div>
          </Field>
          <Field label="Billable / non-billable split">
            <div className="sw-input" style={{ width: 240 }}>
              <I.Clock size={14}/>
              <span className="val left" style={{ textAlign: "left" }}>
                <DurationDisplay billable={405} nonBillable={30}/>
              </span>
            </div>
          </Field>
        </div>
      </DCArtboard>

      <DCArtboard id="session-type" label="SessionTypeSelector · prominent" width={460} height={300}>
        <div className="sw-art sw-stack-4">
          <Field label="Field mode · large, full-width, primary selector">
            <SWC.SessionTypeSelector value="ON_SITE" lg/>
          </Field>
          <Field label="Back-office mode · inline default">
            <Segmented value="TRAVEL" options={[
              { value: "TRAVEL",  label: "Travel",  icon: <I.ArrowLeftRight size={12}/> },
              { value: "ON_SITE", label: "On site", icon: <I.Building size={12}/> },
            ]}/>
          </Field>
          <div className="sw-note">
            This selector is <strong>never</strong> a dropdown — workers in gloves can't tap precise targets. The control is large enough to misfire-tolerant by ~16px on every side.
          </div>
        </div>
      </DCArtboard>

      <DCArtboard id="toggle-radio-textarea" label="Toggle · Radio · Textarea (audit reason)" width={460} height={420}>
        <div className="sw-art sw-stack-4">
          <Field label="Toggle">
            <div className="sw-row">
              <Toggle on={false}/><span style={{ fontSize: 12 }}>Auto-close session at end of day</span>
            </div>
            <div className="sw-row" style={{ marginTop: 6 }}>
              <Toggle on/><span style={{ fontSize: 12 }}>Notify ops manager on FAILED capture</span>
            </div>
          </Field>
          <Field label="Radio · static enum">
            <div className="sw-stack-2">
              <label className="sw-row" style={{ gap: 8, fontSize: 12 }}><Radio on/> Round to 5 min</label>
              <label className="sw-row" style={{ gap: 8, fontSize: 12 }}><Radio/> Round to 15 min</label>
              <label className="sw-row" style={{ gap: 8, fontSize: 12 }}><Radio/> No rounding</label>
            </div>
          </Field>
          <Field label="Textarea · audit reason" audit hint="This text becomes a permanent audit_entry payload.">
            <textarea defaultValue="Worker confirmed late clock-out via gate-scan."
              style={{
                width: "100%", padding: "8px 10px",
                background: "var(--color-bg-elev)",
                border: "var(--hairline) solid var(--color-border-strong)",
                borderRadius: 6, fontSize: 13, fontFamily: "var(--font-sans)",
                minHeight: 60, resize: "vertical"
              }}/>
          </Field>
        </div>
      </DCArtboard>

      <DCArtboard id="form-shell" label="Form shell · dirty / saving / error" width={460} height={420}>
        <div className="sw-art sw-stack-3">
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            <div>
              <h3 style={{ fontSize: 14 }}>Edit work session</h3>
              <div style={{ fontSize: 11, color: "var(--color-muted)" }}>ses-3098 · w-42</div>
            </div>
            <span className="sw-pill warn"><I.CircleDot size={10}/> dirty · 3 fields</span>
          </div>
          <hr className="sw-divider"/>
          <Field label="Clock-in (UTC)"><DateTimePicker iso="2026-05-24T07:32:00Z"/></Field>
          <Field label="Clock-out (UTC)"><DateTimePicker iso="2026-05-24T15:48:00Z" focus/></Field>
          <Field label="Type"><Segmented value="ON_SITE" options={[
            { value: "TRAVEL", label: "Travel" },
            { value: "ON_SITE", label: "On site" },
          ]}/></Field>
          <SWC.ReasonPrompt value="Gate-scan correction confirmed by ops."/>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: 8 }}>
            <div style={{ fontSize: 11, color: "var(--color-warn)", display: "flex", gap: 4, alignItems: "center" }}>
              <I.Alert size={12}/> Saving will append an audit_entry and trigger a new calculation revision.
            </div>
            <div className="sw-row" style={{ gap: 6 }}>
              <Button variant="ghost">Cancel</Button>
              <Button variant="primary"><span className="sw-spin"/> Saving…</Button>
            </div>
          </div>
        </div>
      </DCArtboard>
    </DCSection>
  );
};

/* ═══════════════════════════════════════════════════════════════
   05 · DATA DISPLAY
   ═══════════════════════════════════════════════════════════════ */

SEC.Data = function DataSection() {
  return (
    <DCSection id="data" title="05 · Data display" subtitle="Tables, calculation snapshots, diffs, timelines. The audit story lives here.">
      <DCArtboard id="table" label="Table · dense / hover / stale / selected" width={760} height={420}>
        <div className="sw-art flush">
          <table className="desk-table" style={{ width: "100%" }}>
            <thead>
              <tr>
                <th style={{ width: 36 }}></th>
                <th>Session</th>
                <th>Worker</th>
                <th>Type</th>
                <th>Status</th>
                <th>Duration</th>
                <th className="num">Cost</th>
                <th>Updated · UTC</th>
              </tr>
            </thead>
            <tbody>
              <tr style={{ background: "var(--color-accent-soft)" }}>
                <td><Radio on/></td>
                <td><span className="sw-mono">ses-3098</span></td>
                <td><div className="sw-row" style={{ gap: 6 }}><Identicon id="w-42" size="sm"/><span>w-42</span></div></td>
                <td>ON_SITE</td>
                <td><StatusBadge namespace="work_session" value="CORRECTION_PROPOSED" showNs={false}/></td>
                <td><DurationDisplay minutes={450}/></td>
                <td className="num"><MoneyDisplay cents={31500}/></td>
                <td><span style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--color-muted)" }}>2026-05-24T16:12Z</span></td>
              </tr>
              <tr>
                <td><Radio/></td>
                <td><span className="sw-mono">ses-3097</span></td>
                <td><div className="sw-row" style={{ gap: 6 }}><Identicon id="w-115" size="sm"/><span>w-115</span></div></td>
                <td>TRAVEL</td>
                <td><StatusBadge namespace="work_session" value="APPROVED" showNs={false}/></td>
                <td><DurationDisplay minutes={90}/></td>
                <td className="num"><MoneyDisplay noRate/></td>
                <td><span style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--color-muted)" }}>2026-05-24T11:02Z</span></td>
              </tr>
              <tr style={{ opacity: 0.55 }}>
                <td><Radio/></td>
                <td><span className="sw-mono">ses-3091</span></td>
                <td><div className="sw-row" style={{ gap: 6 }}><Identicon id="w-007" size="sm"/><span>w-007</span></div></td>
                <td>ON_SITE</td>
                <td><StatusBadge namespace="work_session" value="CLOSED" showNs={false}/></td>
                <td><DurationDisplay minutes={420}/></td>
                <td className="num"><MoneyDisplay cents={31500}/></td>
                <td><span style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--color-muted)" }}>stale · rule v2</span></td>
              </tr>
              <tr>
                <td><Radio/></td>
                <td><span className="sw-mono">ses-3088</span></td>
                <td><div className="sw-row" style={{ gap: 6 }}><Identicon id="w-86" size="sm"/><span>w-86</span></div></td>
                <td>ON_SITE</td>
                <td><StatusBadge namespace="work_session" value="REJECTED" showNs={false}/></td>
                <td><DurationDisplay minutes={0}/></td>
                <td className="num" style={{ color: "var(--color-muted)" }}>—</td>
                <td><span style={{ fontFamily: "var(--font-mono)", fontSize: 11, color: "var(--color-muted)" }}>2026-05-23T18:33Z</span></td>
              </tr>
              <tr>
                <td><Radio/></td>
                <td colSpan={7}>
                  <EmptyState
                    icon={<I.Receipt size={28}/>}
                    title="No more sessions this period"
                    body="Connect a capture device to keep the table fresh."
                    action={<Button variant="secondary"><I.Plus size={14}/> Add capture source</Button>}
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </DCArtboard>

      <DCArtboard id="kv-list" label="DescriptionList · List · Card" width={460} height={380}>
        <div className="sw-art sw-stack-4">
          <div>
            <div className="sw-eyebrow">Description list · key/value</div>
            <dl className="sw-kv" style={{ marginTop: 6 }}>
              <dt>session_id</dt><dd>ses-3098</dd>
              <dt>worker_id</dt><dd>w-42</dd>
              <dt>project_id</dt><dd>prj-114</dd>
              <dt>rule_version</dt><dd>rule:prj-114:v3</dd>
              <dt>engine_revision</dt><dd>calc-engine 2.4.1</dd>
            </dl>
          </div>
          <hr className="sw-divider"/>
          <div>
            <div className="sw-eyebrow">List item · stacked</div>
            {[
              { who: "w-42",  what: "Clock-in",  when: "07:32Z" },
              { who: "w-42",  what: "Clock-out", when: "15:02Z" },
              { who: "admin-7", what: "Edit", when: "17:04Z" },
            ].map((r,i) => (
              <div key={i} className="sw-row" style={{
                padding: "8px 0", gap: 10,
                backgroundImage: "var(--grad-divider)", backgroundRepeat: "no-repeat",
                backgroundPosition: "bottom", backgroundSize: "100% var(--hairline)"
              }}>
                <Identicon id={r.who} size="sm"/>
                <div style={{ fontSize: 12 }}>
                  <div><b>{r.who}</b> <span style={{ color: "var(--color-muted)" }}>· {r.what}</span></div>
                  <div style={{ fontFamily: "var(--font-mono)", fontSize: 10, color: "var(--color-muted)" }}>{r.when}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </DCArtboard>

      <DCArtboard id="stat-tile" label="StatTile · no_rate_configured as first-class" width={760} height={220}>
        <div className="sw-art" style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: 12 }}>
          <StatTile label="Budget"  cents={450000} sub="locked at project start"/>
          <StatTile label="Spent (rate v3)" cents={297500} sub="61% of budget"/>
          <StatTile label="Spent · this worker" noRate sub="no_rate_configured · w-115"/>
          <StatTile label="Open sessions" value={<span style={{ fontFamily: "var(--font-mono)", fontSize: 24 }}>14</span>} sub="3 awaiting approval"/>
        </div>
      </DCArtboard>

      <DCArtboard id="money-duration-display" label="MoneyDisplay · DurationDisplay · DateTime" width={520} height={300}>
        <div className="sw-art sw-stack-3">
          <div className="sw-eyebrow">MoneyDisplay · cents → € NL</div>
          <div className="sw-row" style={{ gap: 18 }}>
            <MoneyDisplay cents={450000} large/>
            <MoneyDisplay cents={31500}/>
            <MoneyDisplay cents={-450}/>
            <MoneyDisplay noRate/>
          </div>
          <div className="sw-eyebrow">DurationDisplay · minutes</div>
          <div className="sw-row" style={{ gap: 18 }}>
            <DurationDisplay minutes={450}/>
            <DurationDisplay billable={405} nonBillable={30}/>
            <DurationDisplay minutes={0}/>
          </div>
          <div className="sw-eyebrow">DateTimeDisplay · UTC + viewing TZ</div>
          <div className="sw-stack-2">
            <DateTimeDisplay iso="2026-05-24T07:32:00Z" tz="UTC" rel="9h ago"/>
            <DateTimeDisplay iso="2026-05-24T07:32:00Z" tz="Europe/Amsterdam"/>
          </div>
        </div>
      </DCArtboard>

      <DCArtboard id="json-viewer" label="JSONViewer · calculation_snapshot" width={620} height={520}>
        <div className="sw-art">
          <div className="sw-h">calculation_snapshot</div>
          <JsonViewer
            value={{
              engine_version: "calc-engine 2.4.1",
              rule_version: "rule:prj-114:v3",
              rule_params: { rate_minute_on_site_cents: 75, lunch_min: 30, round_min: 5 },
              input: { clock_in_utc: "2026-05-24T07:32:00Z", clock_out_utc: "2026-05-24T15:02:00Z", session_type: "ON_SITE" },
              steps: [
                { op: "duration_minutes", out: 450 },
                { op: "subtract_lunch",   out: 420 },
                { op: "round_to_5min",    out: 420 },
                { op: "apply_rate",       out_cents: 31500 },
              ],
              output: { billable_minutes: 420, nonbillable_minutes: 30, total_cents: 31500 },
            }}
            highlights={{ engine_version: true, rule_version: true, rule_params: true, input: true, steps: true, output: true }}
            annotations={{
              engine_version: "pinned at session-close — never updated",
              rule_version:   "snapshotted reference, not a live join",
              steps:          "ordered, immutable",
              output:         "deterministic from inputs above",
            }}/>
        </div>
      </DCArtboard>

      <DCArtboard id="diff-viewer" label="DiffViewer · canonical vs proposed" width={620} height={420}>
        <div className="sw-art">
          <div className="sw-h">DiffViewer · arbitrary JSON shapes</div>
          <DiffViewer
            title="canonical → proposed"
            subtitle="work_sessions/ses-3098"
            rows={[
              { kind: " ", text: '"session_id": "ses-3098",', indent: 1 },
              { kind: " ", text: '"worker_id": "w-42",', indent: 1 },
              { kind: "-", text: '"clock_out_utc": "2026-05-24T15:02:00Z",', indent: 1 },
              { kind: "+", text: '"clock_out_utc": "2026-05-24T15:48:00Z",', indent: 1 },
              { kind: " ", text: '"session_type": "ON_SITE",', indent: 1 },
              { kind: "-", text: '"billable_minutes": 420,', indent: 1 },
              { kind: "+", text: '"billable_minutes": 466,', indent: 1 },
              { kind: "-", text: '"total_cents": 31500', indent: 1 },
              { kind: "+", text: '"total_cents": 34950', indent: 1 },
            ]}/>
          <div className="sw-note">Same component is used for proposal review <em>and</em> audit-entry inspection. Both feed it `{`{ before, after }`}` JSON of any shape.</div>
        </div>
      </DCArtboard>

      <DCArtboard id="timeline" label="Timeline · append-only · immutable" width={460} height={520}>
        <div className="sw-art">
          <div className="sw-h">Session timeline · ses-3098</div>
          <div style={{ marginTop: 8 }}>
            <Timeline items={[
              { kind: "create",  who: "w-42",     verb: "clocked in",  iso: "2026-05-24T07:32:00Z", rel: "9h 32m ago", badge: <StatusBadge namespace="work_session" value="OPEN" showNs={false}/> },
              { kind: "edit",    who: "w-42",     verb: "clocked out", iso: "2026-05-24T15:02:00Z", rel: "2h ago",     badge: <StatusBadge namespace="work_session" value="CLOSED" showNs={false}/> },
              { kind: "edit",    who: "automation-01", verb: "created correction proposal", iso: "2026-05-24T16:12:11Z", rel: "55m ago", badge: <span className="sw-pill warn">prop-1408</span>, detail: "+46m · derived from gate-scan capture · confidence 82%" },
              { kind: "approve", who: "admin-7",  verb: "approved proposal",  iso: "2026-05-24T17:04:22Z", rel: "14m ago", badge: <StatusBadge namespace="proposal" value="APPROVED" showNs={false}/>, detail: "Reason: gate-scan correction confirmed." },
            ]}/>
          </div>
          <div className="sw-note">No edit / reorder affordances. Entries are appended forward only; corrections are new entries, not mutations of old ones.</div>
        </div>
      </DCArtboard>

      <DCArtboard id="trail" label="ProgressTrail · bookkeeping fork" width={760} height={300}>
        <div className="sw-art sw-stack-4">
          <div className="sw-eyebrow">Linear · default</div>
          <ProgressTrail steps={[
            { ns: "bookkeeping", value: "DRAFT",   state: "done" },
            { ns: "bookkeeping", value: "READY",   state: "current" },
            { ns: "bookkeeping", value: "EXPORTED" },
          ]}/>
          <div className="sw-eyebrow">Forked · stale READY/EXPORTED + new DRAFT</div>
          <div className="sw-trail">
            <div className="step done">
              <StatusBadge namespace="bookkeeping" value="DRAFT" showNs={false}/>
            </div>
            <span className="arr">→</span>
            <div className="step done" style={{ opacity: 0.55 }}>
              <StatusBadge namespace="bookkeeping" value="READY" showNs={false}/>
              <span style={{ fontSize: 10, color: "var(--color-muted)" }}>· stale (rule v2)</span>
            </div>
            <span className="arr">→</span>
            <div className="step done" style={{ opacity: 0.55 }}>
              <StatusBadge namespace="bookkeeping" value="EXPORTED" showNs={false}/>
              <span style={{ fontSize: 10, color: "var(--color-muted)" }}>· stale</span>
            </div>
            <span className="arr" style={{ color: "var(--color-warn)" }}>↘</span>
            <div className="step fork">
              <StatusBadge namespace="bookkeeping" value="DRAFT" showNs={false}/>
              <span style={{ fontSize: 10 }}>· new fork (rule v3)</span>
            </div>
          </div>
          <div className="sw-note">A new DRAFT does not replace the prior EXPORTED row — both rows coexist. The new DRAFT carries the upgraded rule_version.</div>
        </div>
      </DCArtboard>

      <DCArtboard id="empty-pagination" label="EmptyState · Pagination · CodeBlock" width={620} height={300}>
        <div className="sw-art sw-stack-4">
          <div className="card" style={{ padding: 0 }}>
            <EmptyState
              icon={<I.Receipt size={28}/>}
              title="No proposals to review"
              body="Automation has nothing pending for this project."
              action={<Button variant="secondary">Configure capture source</Button>}
            />
          </div>
          <div className="sw-row" style={{ justifyContent: "space-between" }}>
            <div style={{ fontSize: 12, color: "var(--color-muted)" }}>14 of 218 sessions</div>
            <div className="sw-row" style={{ gap: 4 }}>
              <Button variant="secondary" size="sm" disabled>Prev</Button>
              <span className="sw-pill">1</span>
              <span style={{ fontSize: 11, color: "var(--color-muted)", padding: "0 4px" }}>2 3 …</span>
              <Button variant="secondary" size="sm">Load more</Button>
            </div>
          </div>
          <div>
            <div className="sw-eyebrow" style={{ marginBottom: 6 }}>CodeBlock</div>
            <pre style={{
              fontFamily: "var(--font-mono)", fontSize: 11,
              background: "var(--color-card-2)",
              border: "var(--hairline) solid var(--color-border)",
              borderRadius: 6, padding: 10, margin: 0, overflow: "auto",
            }}>{`POST /work_sessions/ses-3098/proposals
  prop-1408 · clock_out_correction · confidence=82 · status=PENDING`}</pre>
          </div>
        </div>
      </DCArtboard>
    </DCSection>
  );
};

/* ═══════════════════════════════════════════════════════════════
   06 · FEEDBACK & STATE
   ═══════════════════════════════════════════════════════════════ */

SEC.Feedback = function FeedbackSection() {
  return (
    <DCSection id="feedback" title="06 · Feedback & state" subtitle="API-error-shape aware. Confirmations frame audit consequences.">
      <DCArtboard id="alerts" label="InlineAlert · Banner" width={520} height={420}>
        <div className="sw-art sw-stack-3">
          <InlineAlert tone="info"  title="Proposal is read-only" body="Canonical state is unchanged until you Approve."/>
          <InlineAlert tone="warn"  title="Rule v3 published 5m ago" body="Sessions closed before publish still reference rule v2 — they will not recompute."/>
          <InlineAlert tone="error" title="Validation guardrail (400)" body="clock_out_utc must be > clock_in_utc. Engine rejected the proposed correction." action={<Button variant="ghost" size="sm">View payload</Button>}/>
          <InlineAlert tone="ok"    title="Bookkeeping draft created" body="bk-DRAFT-0044 ready for review."/>
        </div>
      </DCArtboard>

      <DCArtboard id="error-state" label="ErrorState · {detail} shape" width={520} height={320}>
        <div className="sw-art">
          <div className="card" style={{ padding: 20 }}>
            <div className="sw-row" style={{ gap: 8 }}>
              <span style={{
                width: 28, height: 28, borderRadius: 8,
                background: "var(--color-neg-soft)", color: "var(--color-neg)",
                display: "grid", placeItems: "center"
              }}><I.Alert size={16}/></span>
              <div>
                <div style={{ fontWeight: 600, fontSize: 14 }}>Couldn't approve proposal</div>
                <div style={{ fontSize: 12, color: "var(--color-muted)", fontFamily: "var(--font-mono)" }}>HTTP 400 · validation_error</div>
              </div>
            </div>
            <hr className="sw-divider" style={{ margin: "12px 0" }}/>
            <div style={{ fontFamily: "var(--font-mono)", fontSize: 12 }}>
              <span className="sw-pill">detail</span>
              <p style={{ marginTop: 6, color: "var(--color-fg-2)" }}>
                "Session ses-3098 is closed under rule v2. Proposed clock_out (15:48Z) crosses into a new billing day and is rejected by the period guardrail."
              </p>
            </div>
            <div className="sw-row" style={{ marginTop: 14, justifyContent: "flex-end", gap: 6 }}>
              <Button variant="ghost">Open audit context</Button>
              <Button variant="secondary">Retry</Button>
            </div>
          </div>
          <div className="sw-note">400-class errors are user-fixable domain guardrails. They are not "crash" surfaces — they show the offending field and an action to fix it.</div>
        </div>
      </DCArtboard>

      <DCArtboard id="confirm" label="ConfirmDialog · audit framing" width={520} height={360}>
        <div className="sw-art">
          <div className="card" style={{ padding: 20 }}>
            <div className="sw-row" style={{ gap: 8 }}>
              <span style={{
                width: 28, height: 28, borderRadius: 8,
                background: "var(--color-warn-soft)", color: "var(--color-warn)",
                display: "grid", placeItems: "center"
              }}><I.Alert size={16}/></span>
              <h3 style={{ fontSize: 16 }}>Approve proposal · this writes an audit row</h3>
            </div>
            <p style={{ fontSize: 13, color: "var(--color-fg-2)", marginTop: 10 }}>
              You're about to mutate <code style={{ fontFamily: "var(--font-mono)" }}>work_sessions/ses-3098</code> and append a permanent audit_entry attributed to <code style={{ fontFamily: "var(--font-mono)" }}>admin-7</code>. A new calculation revision will be triggered.
            </p>
            <SWC.ReasonPrompt value=""/>
            <div className="sw-row" style={{ marginTop: 14, justifyContent: "flex-end", gap: 6 }}>
              <Button variant="ghost">Cancel</Button>
              <Button variant="primary"><I.Check size={14}/> Approve · writes audit</Button>
            </div>
          </div>
          <div className="sw-note">Copy frames <em>what changes permanently</em>, not generic "Are you sure?". Reason is required, not optional.</div>
        </div>
      </DCArtboard>

      <DCArtboard id="toast-overlay" label="Toast · LoadingOverlay · Badge-with-count" width={520} height={360}>
        <div className="sw-art sw-stack-4">
          <div className="sw-eyebrow">Toast · single line, past tense</div>
          <div style={{ position: "relative", height: 60 }}>
            <div className="toast" style={{ position: "absolute", left: 0, top: 0 }}>
              <span className="ico"><I.CircleCheck size={14}/></span>
              Audit entry appended (aud-90211).
            </div>
          </div>
          <div className="sw-eyebrow">Loading overlay · in-card</div>
          <div className="card" style={{ position: "relative", padding: 24, minHeight: 80 }}>
            <div style={{ fontSize: 12, color: "var(--color-muted)" }}>Loading session…</div>
            <div style={{
              position: "absolute", inset: 0,
              background: "color-mix(in oklab, var(--color-card) 70%, transparent)",
              backdropFilter: "blur(2px)", borderRadius: 12,
              display: "grid", placeItems: "center"
            }}>
              <span className="sw-spin" style={{ width: 18, height: 18 }}/>
            </div>
          </div>
          <div className="sw-eyebrow">Badge-with-count</div>
          <div className="sw-row" style={{ gap: 18 }}>
            <span style={{ position: "relative", display: "inline-flex" }}>
              <Button variant="secondary"><I.Bell size={14}/> Proposals</Button>
              <span style={{
                position: "absolute", top: -4, right: -6,
                background: "var(--color-warn)", color: "#fff",
                fontFamily: "var(--font-mono)", fontSize: 10, fontWeight: 600,
                padding: "1px 5px", borderRadius: 999, lineHeight: 1.3,
                border: "1.5px solid var(--color-bg)",
              }}>3</span>
            </span>
            <span style={{ position: "relative", display: "inline-flex" }}>
              <Button variant="ghost"><I.Bell size={14}/></Button>
              <span style={{
                position: "absolute", top: 2, right: 2,
                width: 7, height: 7, borderRadius: 999,
                background: "var(--color-warn)",
                border: "1.5px solid var(--color-bg)",
              }}/>
            </span>
          </div>
        </div>
      </DCArtboard>
    </DCSection>
  );
};

window.SEC = SEC;
