// Navigation chrome — TopNav, BottomNav, CommandPalette

// ----- TopNav -----
function TopNav({ route, onRoute, onOpenCmdK, dark, onToggleDark, privacy, onTogglePrivacy }) {
  const items = [
    { id: "overview", label: "Overview" },
    { id: "accounts", label: "Accounts", dropdown: [
      { id: "accounts",     label: "All accounts",   icon: <I.Wallet size={14}/> },
      { id: "accounts/fid", label: "Brokerage · Fidelity",   icon: <I.Building size={14}/> },
      { id: "accounts/vng", label: "Roth IRA · Vanguard",    icon: <I.Building size={14}/> },
      { id: "accounts/ally",label: "Savings · Ally",         icon: <I.Building size={14}/> },
      { id: "accounts/cb",  label: "Crypto · Coinbase",      icon: <I.Coins size={14}/> },
    ]},
    { id: "transactions", label: "Transactions" },
    { id: "holdings",     label: "Holdings", dropdown: [
      { id: "holdings",  label: "All holdings",   icon: <I.Layers size={14}/> },
      { id: "watchlist", label: "Watchlist",       icon: <I.Star size={14}/> },
    ]},
    { id: "reports",      label: "Reports" },
  ];

  const [openDropdown, setOpenDropdown] = useState(null);
  const navRef = useRef(null);
  useEffect(() => {
    const onClick = (e) => { if (!navRef.current?.contains(e.target)) setOpenDropdown(null); };
    document.addEventListener("mousedown", onClick);
    return () => document.removeEventListener("mousedown", onClick);
  }, []);

  return (
    <nav className="topnav" aria-label="Primary" ref={navRef}>
      <a className="brand" onClick={() => onRoute("overview")} role="button" tabIndex={0}>
        <I.Logo size={22} className="mark"/>
        <span>Tooling</span>
      </a>

      {items.map((it) => {
        const active = route === it.id || (it.dropdown && route.startsWith(it.id));
        return (
          <div key={it.id} style={{ position: "relative" }} className={it.id === "reports" ? "" : ""}>
            <button
              className="navitem desktop-only"
              aria-current={active ? "page" : undefined}
              onClick={() => {
                if (it.dropdown) setOpenDropdown(openDropdown === it.id ? null : it.id);
                else { onRoute(it.id); setOpenDropdown(null); }
              }}
            >
              {it.label}
              {it.dropdown && <span className="chev"><I.Chevron size={12}/></span>}
            </button>
            {it.dropdown && openDropdown === it.id && (
              <div className="popover" style={{ top: "calc(100% + 6px)", left: 0 }}>
                {it.dropdown.map((d) => (
                  <div key={d.id} className="item" onClick={() => { onRoute(d.id); setOpenDropdown(null); }}>
                    <span className="ico">{d.icon}</span>
                    {d.label}
                  </div>
                ))}
              </div>
            )}
          </div>
        );
      })}

      <div className="right">
        <button className="searchbtn" onClick={onOpenCmdK} aria-label="Open command palette">
          <I.Search size={14} className="ico"/>
          <span className="placeholder">Search or jump to…</span>
          <span className="kbd">⌘K</span>
        </button>
        <button className="iconbtn" aria-label="Toggle privacy" onClick={onTogglePrivacy} title="Privacy (⌘⇧P)">
          <span className="ico">{privacy ? <I.EyeOff size={16}/> : <I.Eye size={16}/>}</span>
        </button>
        <button className="iconbtn" aria-label="Notifications" title="Alerts">
          <span className="ico"><I.Bell size={16}/></span>
        </button>
        <button className="iconbtn" aria-label="Toggle theme" onClick={onToggleDark} title="Theme">
          <span className="ico">{dark ? <I.CircleDot size={16}/> : <I.CircleCheck size={16}/>}</span>
        </button>
        <div className="avatar" aria-hidden="true">{DATA.user.initial}</div>
      </div>
    </nav>
  );
}

// ----- BottomNav (mobile) -----
function BottomNav({ route, onRoute }) {
  const items = [
    { id: "overview",     label: "Home",     icon: <I.Home size={18}/> },
    { id: "holdings",     label: "Holdings", icon: <I.LineChart size={18}/> },
    { id: "transactions", label: "Activity", icon: <I.Receipt size={18}/> },
    { id: "accounts",     label: "Accounts", icon: <I.Wallet size={18}/> },
    { id: "more",         label: "More",     icon: <I.MoreH size={18}/> },
  ];
  return (
    <nav className="bottomnav" aria-label="Mobile">
      {items.map((it) => (
        <button
          key={it.id}
          className="item"
          aria-current={route === it.id || (it.id !== "more" && route.startsWith(it.id)) ? "page" : undefined}
          onClick={() => onRoute(it.id === "more" ? "overview" : it.id)}
        >
          <span className="ico">{it.icon}</span>
          {it.label}
        </button>
      ))}
    </nav>
  );
}

// ----- CommandPalette -----
function CommandPalette({ open, onClose, onRoute, onAction }) {
  const [query, setQuery] = useState("");
  const [idx, setIdx] = useState(0);
  const inputRef = useRef(null);

  const allItems = [
    { group: "Actions", id: "new-transfer", label: "New transfer",        icon: <I.ArrowLeftRight size={14}/>, kbd: "⌘T", run: () => onAction?.("transfer") },
    { group: "Actions", id: "export",        label: "Export transactions", icon: <I.Download size={14}/>,       kbd: "⌘E", run: () => onAction?.("export") },
    { group: "Actions", id: "connect",       label: "Connect account",     icon: <I.Plus size={14}/>,            run: () => onAction?.("connect") },
    { group: "Actions", id: "privacy",       label: "Toggle privacy mode", icon: <I.EyeOff size={14}/>,         kbd: "⌘⇧P", run: () => onAction?.("privacy") },
    { group: "Navigate", id: "overview",     label: "Overview",            icon: <I.Home size={14}/>,           kbd: "G O", run: () => onRoute("overview") },
    { group: "Navigate", id: "accounts",     label: "Accounts",            icon: <I.Wallet size={14}/>,         kbd: "G A", run: () => onRoute("accounts") },
    { group: "Navigate", id: "transactions", label: "Transactions",        icon: <I.Receipt size={14}/>,        kbd: "G T", run: () => onRoute("transactions") },
    { group: "Navigate", id: "holdings",     label: "Holdings",            icon: <I.LineChart size={14}/>,      kbd: "G H", run: () => onRoute("holdings") },
  ];

  const filtered = useMemo(() => {
    if (!query) return allItems;
    const q = query.toLowerCase();
    return allItems.filter(i => i.label.toLowerCase().includes(q));
  }, [query]);

  const groups = useMemo(() => {
    const m = new Map();
    filtered.forEach((it) => { if (!m.has(it.group)) m.set(it.group, []); m.get(it.group).push(it); });
    return [...m.entries()];
  }, [filtered]);

  useEffect(() => { if (open) { setQuery(""); setIdx(0); setTimeout(() => inputRef.current?.focus(), 10); } }, [open]);

  useEffect(() => {
    if (!open) return;
    const onKey = (e) => {
      if (e.key === "Escape") { e.preventDefault(); onClose(); }
      else if (e.key === "ArrowDown") { e.preventDefault(); setIdx((i) => Math.min(filtered.length - 1, i + 1)); }
      else if (e.key === "ArrowUp")   { e.preventDefault(); setIdx((i) => Math.max(0, i - 1)); }
      else if (e.key === "Enter")     { e.preventDefault(); const it = filtered[idx]; if (it) { it.run(); onClose(); } }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, filtered, idx]);

  if (!open) return null;
  let runningIdx = -1;
  return (
    <div className="cmdk-backdrop" onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="cmdk" role="dialog" aria-label="Command palette">
        <div className="cmdk-search">
          <I.Search size={16}/>
          <input
            ref={inputRef}
            value={query}
            onChange={(e) => { setQuery(e.target.value); setIdx(0); }}
            placeholder="Search or jump to…"
          />
          <span className="kbd">esc</span>
        </div>
        {groups.length === 0 && (
          <div style={{ padding: "20px 14px", color: "var(--color-muted)", fontSize: 13 }}>No matches</div>
        )}
        {groups.map(([group, items]) => (
          <div className="cmdk-group" key={group}>
            <div className="cmdk-label">{group}</div>
            {items.map((it) => {
              runningIdx++;
              const active = runningIdx === idx;
              const myIdx = runningIdx;
              return (
                <div
                  key={it.id}
                  className={`cmdk-item ${active ? "active" : ""}`}
                  onMouseEnter={() => setIdx(myIdx)}
                  onClick={() => { it.run(); onClose(); }}
                >
                  <span className="ico">{it.icon}</span>
                  {it.label}
                  {it.kbd && <span className="meta">{it.kbd}</span>}
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}

Object.assign(window, { TopNav, BottomNav, CommandPalette });
