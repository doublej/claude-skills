// Screens — composed from components + charts. Each screen reads window.DATA.

// ----- Overview -----
function OverviewScreen({ onRoute, onAction }) {
  const [range, setRange] = useState("90D");
  const tone = DATA.net_worth_delta >= 0 ? "pos" : "neg";

  return (
    <>
      <PageHeader
        title="Overview"
        sub={`Updated 2m ago · ${DATA.accounts.length} accounts`}
        actions={
          <>
            <Button variant="secondary" icon={<I.Refresh size={14}/>}>Sync</Button>
            <Button variant="primary" icon={<I.ArrowLeftRight size={14}/>} onClick={() => onAction?.("transfer")}>New transfer</Button>
          </>
        }
      />

      <div className="grid grid-3">
        <Stat
          label="Net worth"
          value={fmt.money(DATA.net_worth)}
          delta={DATA.net_worth_delta}
          deltaPct={DATA.net_worth_delta_pct}
          sub="today"
          spark={DATA.net_worth_series.slice(-12)}
          sparkTone={tone}
        />
        <Stat label="YTD return" value={fmt.pct(DATA.ytd_return_pct)} sub={`${fmt.money(DATA.ytd_return_abs, { signed: true })} vs cost basis`} spark={DATA.net_worth_series.slice(-12)} />
        <Stat label="Holdings" value={String(DATA.holdings.length)} sub={`${DATA.accounts.length} accounts · 2 currencies`}/>
      </div>

      <Card
        title="Net worth"
        sub={range === "90D" ? "Last 90 days" : range}
        actions={
          <div style={{ display: "flex", gap: 2, background: "var(--color-card-2)", borderRadius: 6, padding: 2 }}>
            {["1M", "3M", "90D", "YTD", "1Y", "All"].map((r) => (
              <button
                key={r}
                onClick={() => setRange(r)}
                style={{
                  height: 24, padding: "0 10px",
                  background: range === r ? "var(--color-bg-elev)" : "transparent",
                  border: 0, borderRadius: 4,
                  fontSize: 11, fontWeight: 500,
                  color: range === r ? "var(--color-fg)" : "var(--color-muted)",
                  fontFamily: "var(--font-mono)",
                  cursor: "pointer",
                  boxShadow: range === r ? "var(--shadow-xs)" : "none",
                }}
              >{r}</button>
            ))}
          </div>
        }
      >
        <PriceChart data={DATA.net_worth_series} height={220} tone={tone}/>
      </Card>

      <div className="grid grid-2">
        <Card title="Allocation" sub="By account">
          <AllocationDonut items={DATA.accounts.map(a => ({ label: a.name, value: a.balance }))}/>
        </Card>

        <Card title="Watchlist" actions={<Button size="sm" variant="ghost" icon={<I.Plus size={12}/>}>Add</Button>} flush>
          <table className="table">
            <tbody>
              {DATA.watchlist.map((w) => (
                <tr key={w.ticker}>
                  <td className="ticker">{w.ticker}</td>
                  <td className="num"><Money value={w.price}/></td>
                  <td className="num"><Pct value={w.day_pct}/></td>
                  <td className="num" style={{ width: 90 }}>
                    <Sparkline data={[3,5,4,7,6,8,9].map(v => v + Math.random())} width={70} height={20} tone={w.day_pct >= 0 ? "pos" : "neg"}/>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      </div>

      <Card
        title="Recent activity"
        actions={<Button size="sm" variant="ghost" onClick={() => onRoute("transactions")}>View all <I.ArrowRight size={12}/></Button>}
        flush
        className=""
      >
        <DataTable
          columns={[
            { key: "date",     label: "Date",      render: (r) => r.date },
            { key: "desc",     label: "Description", render: (r) => <><span>{r.desc}</span> {r.status === "pending" && <Badge tone="warn">Pending</Badge>}</> },
            { key: "account",  label: "Account",   render: (r) => <span className="muted">{r.account}</span> },
            { key: "amount",   label: "Amount", num: true, render: (r) => <Money value={r.amount} signed tone={r.amount > 0 ? "pos" : undefined}/> },
          ]}
          rows={DATA.transactions.slice(0, 5)}
          mobileCard={(r) => (
            <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
              <div>
                <div style={{ fontSize: 13, fontWeight: 500 }}>{r.desc}</div>
                <div style={{ fontSize: 12, color: "var(--color-muted)" }}>{r.date} · {r.account}</div>
              </div>
              <Money value={r.amount} signed tone={r.amount > 0 ? "pos" : undefined}/>
            </div>
          )}
        />
      </Card>

      {DATA.alerts.length > 0 && (
        <Card title="Alerts" actions={<Button size="sm" variant="ghost">Dismiss all</Button>} flush>
          <div style={{ padding: "4px 0" }}>
            {DATA.alerts.map((a, i) => (
              <div key={i} className={i < DATA.alerts.length - 1 ? "alert-row" : ""} style={{ display: "flex", alignItems: "center", gap: 10, padding: "10px 16px" }}>
                <span style={{ color: a.kind === "warn" ? "var(--color-warn)" : "var(--color-info)" }}>
                  {a.kind === "warn" ? <I.Alert size={14}/> : <I.Info size={14}/>}
                </span>
                <span style={{ fontSize: 13 }}>{a.text}</span>
                <span style={{ marginLeft: "auto", fontSize: 12, color: "var(--color-muted)" }}>{a.time}</span>
              </div>
            ))}
          </div>
        </Card>
      )}
    </>
  );
}

// ----- Accounts -----
function AccountsScreen({ onRoute, onAction }) {
  return (
    <>
      <PageHeader
        crumb={[{ label: "Accounts" }]}
        title="Accounts"
        sub={`${DATA.accounts.length} accounts · ${fmt.money(DATA.accounts.reduce((s,a) => s + a.balance, 0))} total`}
        actions={<Button variant="primary" icon={<I.Plus size={14}/>} onClick={() => onAction?.("connect")}>Connect account</Button>}
      />

      <Card flush>
        <DataTable
          columns={[
            { key: "name", label: "Account", render: (r) => (
              <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                <span style={{ width: 28, height: 28, borderRadius: 6, background: "var(--color-card-2)", display: "inline-flex", alignItems: "center", justifyContent: "center", color: "var(--color-muted)" }}>
                  {r.type === "Crypto" ? <I.Coins size={14}/> : <I.Building size={14}/>}
                </span>
                <div>
                  <div style={{ fontWeight: 500 }}>{r.name}</div>
                  <div className="muted">{r.inst}</div>
                </div>
              </div>
            )},
            { key: "type",    label: "Type",    render: (r) => <Tag>{r.type}</Tag> },
            { key: "status",  label: "Status",  render: (r) => r.status === "active"
                ? <Badge tone="pos" dot>Active</Badge>
                : <Badge tone="warn" dot>Action needed</Badge>
            },
            { key: "synced",  label: "Synced",  render: (r) => <span className="muted">{r.synced}</span> },
            { key: "change",  label: "Today", num: true, render: (r) => <Money value={r.change} signed tone={r.change > 0 ? "pos" : r.change < 0 ? "neg" : undefined}/> },
            { key: "balance", label: "Balance", num: true, render: (r) => <Money value={r.balance}/> },
          ]}
          rows={DATA.accounts}
          getRowKey={(r) => r.id}
          mobileCard={(r) => (
            <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
              <div>
                <div style={{ fontWeight: 500 }}>{r.name}</div>
                <div style={{ fontSize: 12, color: "var(--color-muted)" }}>{r.inst} · {r.synced}</div>
              </div>
              <div style={{ textAlign: "right" }}>
                <Money value={r.balance}/>
                <div style={{ fontSize: 12 }}><Money value={r.change} signed tone={r.change > 0 ? "pos" : "neg"}/></div>
              </div>
            </div>
          )}
        />
      </Card>
    </>
  );
}

// ----- Transactions -----
function TransactionsScreen({ onAction }) {
  const [filter, setFilter] = useState("All");
  const rows = filter === "All" ? DATA.transactions : DATA.transactions.filter(t => t.category === filter);
  return (
    <>
      <PageHeader
        crumb={[{ label: "Activity" }]}
        title="Transactions"
        sub={`${DATA.transactions.length} transactions · last 30 days`}
        actions={
          <>
            <Button variant="secondary" icon={<I.Filter size={14}/>}>Filter</Button>
            <Button variant="secondary" icon={<I.Download size={14}/>} onClick={() => onAction?.("export")}>Export</Button>
          </>
        }
        tabs={["All", "Trade", "Income", "Transfer"]}
        activeTab={filter}
        onTab={setFilter}
      />

      <Card flush>
        <DataTable
          columns={[
            { key: "date",     label: "Date",        render: (r) => r.date },
            { key: "desc",     label: "Description", render: (r) => (
              <div>
                <div>{r.desc}</div>
                <div className="muted">{r.account}</div>
              </div>
            )},
            { key: "category", label: "Category",    render: (r) => <Tag>{r.category}</Tag> },
            { key: "status",   label: "Status",      render: (r) => r.status === "pending" ? <Badge tone="warn">Pending</Badge> : <Badge tone="neutral">Settled</Badge> },
            { key: "amount",   label: "Amount", num: true, render: (r) => <Money value={r.amount} signed tone={r.amount > 0 ? "pos" : undefined}/> },
          ]}
          rows={rows}
          getRowKey={(r) => r.id}
          mobileCard={(r) => (
            <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
              <div>
                <div style={{ fontSize: 13, fontWeight: 500 }}>{r.desc}</div>
                <div style={{ fontSize: 12, color: "var(--color-muted)" }}>{r.date} · {r.account}</div>
              </div>
              <Money value={r.amount} signed tone={r.amount > 0 ? "pos" : undefined}/>
            </div>
          )}
        />
        {rows.length === 0 && (
          <EmptyState
            icon={<I.Receipt size={32}/>}
            title="No transactions"
            body="Try a different filter, or connect an account to see activity here."
            action={<Button variant="primary" icon={<I.Plus size={14}/>}>Connect account</Button>}
          />
        )}
      </Card>
    </>
  );
}

// ----- Holdings -----
function HoldingsScreen({ onAction }) {
  const total = DATA.holdings.reduce((s, h) => s + h.mv, 0);
  return (
    <>
      <PageHeader
        crumb={[{ label: "Portfolio" }]}
        title="Holdings"
        sub={`${DATA.holdings.length} positions · ${fmt.money(total)} market value`}
        actions={
          <>
            <Button variant="secondary" icon={<I.Filter size={14}/>}>Filter</Button>
            <Button variant="primary" icon={<I.Plus size={14}/>}>Add position</Button>
          </>
        }
      />

      <Card flush>
        <DataTable
          columns={[
            { key: "ticker", label: "Ticker", render: (r) => (
              <div>
                <div className="ticker">{r.ticker}</div>
                <div className="muted">{r.name}</div>
              </div>
            )},
            { key: "account", label: "Account", render: (r) => <Tag>{r.account}</Tag> },
            { key: "shares",  label: "Shares",  num: true, render: (r) => <span className="num">{fmt.num(r.shares, 3)}</span> },
            { key: "price",   label: "Price",   num: true, render: (r) => <Money value={r.price}/> },
            { key: "mv",      label: "Market value", num: true, render: (r) => <Money value={r.mv}/> },
            { key: "day_pct", label: "Day",     num: true, render: (r) => <Pct value={r.day_pct}/> },
          ]}
          rows={DATA.holdings}
          getRowKey={(r) => r.ticker + r.account}
          mobileCard={(r) => (
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
                <span className="ticker" style={{ fontSize: 14 }}>{r.ticker}</span>
                <Money value={r.mv} style={{ fontSize: 14, fontWeight: 500 }}/>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", marginTop: 4 }}>
                <span className="muted" style={{ fontSize: 12 }}>{r.name} · {r.account}</span>
                <Pct value={r.day_pct}/>
              </div>
            </div>
          )}
        />
      </Card>
    </>
  );
}

// ----- More / generic fallback for less-built screens -----
function ReportsScreen() {
  return (
    <>
      <PageHeader title="Reports" sub="Generate tax-ready statements and exports"/>
      <Card>
        <EmptyState
          icon={<I.LineChart size={32}/>}
          title="Reports coming soon"
          body="Year-end summaries, realized gains, and dividend breakdowns will live here."
          action={<Button variant="secondary">Notify me</Button>}
        />
      </Card>
    </>
  );
}

Object.assign(window, { OverviewScreen, AccountsScreen, TransactionsScreen, HoldingsScreen, ReportsScreen });
