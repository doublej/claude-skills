// App entry — wires nav, screens, command palette, toasts, keyboard shortcuts.

function App() {
  const [route, setRoute] = useState("overview");
  const [cmdkOpen, setCmdkOpen] = useState(false);
  const [toast, setToast] = useState(null);
  const [dark, setDark] = useTheme();
  const [privacy, setPrivacy] = usePrivacy();

  // ⌘K — open palette
  useEffect(() => {
    const onKey = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setCmdkOpen(true);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  const handleRoute = useCallback((r) => {
    setRoute(r);
    window.scrollTo({ top: 0, behavior: "auto" });
  }, []);

  const handleAction = useCallback((kind) => {
    if (kind === "privacy") setPrivacy((v) => !v);
    else if (kind === "transfer") setToast("Transfer started · funds in 1 business day");
    else if (kind === "export")   setToast("Export ready · downloading transactions.csv");
    else if (kind === "connect")  setToast("Connect account · opening Plaid…");
  }, []);

  let screen = null;
  if (route === "overview") screen = <OverviewScreen onRoute={handleRoute} onAction={handleAction}/>;
  else if (route.startsWith("accounts")) screen = <AccountsScreen onRoute={handleRoute} onAction={handleAction}/>;
  else if (route === "transactions")     screen = <TransactionsScreen onAction={handleAction}/>;
  else if (route === "holdings" || route === "watchlist") screen = <HoldingsScreen onAction={handleAction}/>;
  else if (route === "reports")          screen = <ReportsScreen/>;
  else screen = <OverviewScreen onRoute={handleRoute} onAction={handleAction}/>;

  return (
    <div className="app-shell">
      <TopNav
        route={route}
        onRoute={handleRoute}
        onOpenCmdK={() => setCmdkOpen(true)}
        dark={dark}
        onToggleDark={() => setDark((v) => !v)}
        privacy={privacy}
        onTogglePrivacy={() => setPrivacy((v) => !v)}
      />
      <main id="main" className="app-main">
        {screen}
      </main>
      <BottomNav route={route} onRoute={handleRoute}/>
      <CommandPalette
        open={cmdkOpen}
        onClose={() => setCmdkOpen(false)}
        onRoute={handleRoute}
        onAction={handleAction}
      />
      <Toast msg={toast} onDismiss={() => setToast(null)}/>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App/>);
