// Sample portfolio data for the demo. Stable, deterministic.
window.DATA = {
  user: { name: "Alex Riley", initial: "AR" },
  net_worth: 128402.10,
  net_worth_delta: 1540.20,
  net_worth_delta_pct: 1.21,
  cash: 2084.55,
  ytd_return_pct: 13.7,
  ytd_return_abs: 15402.00,

  // 90-day net worth series (just a few points; chart interpolates)
  net_worth_series: [
    111200, 112050, 110800, 113400, 114200, 115100, 116250, 115980, 117400,
    118200, 119050, 118300, 120100, 121400, 120800, 122500, 123200, 124100,
    124000, 125400, 126100, 126020, 127200, 127800, 128402,
  ],

  accounts: [
    { id: "fid",  name: "Brokerage", inst: "Fidelity",      type: "Taxable",       balance: 84012.55, change: 1102.40, change_pct: 1.33, status: "active", synced: "2m ago" },
    { id: "vng",  name: "Roth IRA",  inst: "Vanguard",      type: "Tax-advantaged", balance: 32480.55, change:  402.10, change_pct: 1.25, status: "active", synced: "12m ago" },
    { id: "ally", name: "Savings",   inst: "Ally Bank",     type: "Cash",          balance:  9824.00, change:    0.00, change_pct: 0.00, status: "active", synced: "1h ago" },
    { id: "cb",   name: "Crypto",    inst: "Coinbase",      type: "Crypto",        balance:  2085.00, change:   35.70, change_pct: 1.74, status: "action", synced: "Reconnect" },
  ],

  holdings: [
    { ticker: "VTI",  name: "Vanguard Total Stock",  account: "Brokerage", shares: 120.500, price: 264.12, mv: 31826.46, day_pct:  1.20 },
    { ticker: "VXUS", name: "Vanguard Intl Stock",   account: "Brokerage", shares:  85.000, price:  62.40, mv:  5304.00, day_pct:  0.42 },
    { ticker: "BND",  name: "Vanguard Total Bond",   account: "Roth IRA",  shares: 200.000, price:  72.80, mv: 14560.00, day_pct: -0.12 },
    { ticker: "VTSAX",name: "Vanguard Total Stock A",account: "Roth IRA",  shares: 102.430, price: 142.05, mv: 14550.20, day_pct:  1.18 },
    { ticker: "AAPL", name: "Apple Inc.",            account: "Brokerage", shares:  42.000, price: 208.55, mv:  8759.10, day_pct:  2.41 },
    { ticker: "MSFT", name: "Microsoft Corp.",       account: "Brokerage", shares:  28.000, price: 432.10, mv: 12098.80, day_pct:  0.84 },
    { ticker: "NVDA", name: "NVIDIA Corp.",          account: "Brokerage", shares:  18.000, price: 124.55, mv:  2241.90, day_pct:  3.12 },
    { ticker: "TSLA", name: "Tesla Inc.",            account: "Brokerage", shares:  14.000, price: 178.40, mv:  2497.60, day_pct: -1.42 },
    { ticker: "BTC",  name: "Bitcoin",               account: "Crypto",    shares:   0.024, price: 68420.00, mv: 1642.08, day_pct:  2.10 },
    { ticker: "ETH",  name: "Ethereum",              account: "Crypto",    shares:   0.140, price:  3164.00, mv:  442.96, day_pct:  1.55 },
  ],

  transactions: [
    { id: "t1",  date: "May 22", account: "Brokerage", desc: "Buy · VTI",        category: "Trade",    amount:  -1320.60, status: "settled" },
    { id: "t2",  date: "May 22", account: "Brokerage", desc: "Dividend · VTI",    category: "Income",   amount:    84.20, status: "settled" },
    { id: "t3",  date: "May 21", account: "Roth IRA",  desc: "Buy · VTSAX",       category: "Trade",    amount:  -1500.00, status: "settled" },
    { id: "t4",  date: "May 20", account: "Savings",   desc: "Transfer to Brokerage", category: "Transfer", amount: -2000.00, status: "settled" },
    { id: "t5",  date: "May 19", account: "Brokerage", desc: "Sell · TSLA",       category: "Trade",    amount:    892.40, status: "settled" },
    { id: "t6",  date: "May 18", account: "Coinbase",  desc: "Buy · BTC",         category: "Trade",    amount:   -250.00, status: "pending" },
    { id: "t7",  date: "May 16", account: "Brokerage", desc: "Dividend · MSFT",   category: "Income",   amount:    21.00, status: "settled" },
    { id: "t8",  date: "May 15", account: "Savings",   desc: "Interest",          category: "Income",   amount:    12.80, status: "settled" },
  ],

  watchlist: [
    { ticker: "SPY",  price: 540.20, day_pct: 0.62 },
    { ticker: "QQQ",  price: 472.10, day_pct: 1.24 },
    { ticker: "GLD",  price: 215.40, day_pct: -0.18 },
    { ticker: "TLT",  price:  92.30, day_pct: -0.42 },
  ],

  alerts: [
    { kind: "warn", text: "Coinbase needs reconnect", time: "3h ago" },
    { kind: "info", text: "Dividend posted · VTI",     time: "1d ago" },
  ],
};

// ----- Formatters -----
window.fmt = {
  money: (n, opts = {}) => {
    const sign = n < 0 ? "−" : (opts.signed ? "+" : "");
    const abs = Math.abs(n);
    const fixed = opts.decimals === 0 ? 0 : 2;
    return sign + "$" + abs.toLocaleString("en-US", { minimumFractionDigits: fixed, maximumFractionDigits: fixed });
  },
  pct: (n, opts = {}) => {
    const sign = n < 0 ? "−" : (opts.signed === false ? "" : "+");
    return sign + Math.abs(n).toFixed(opts.decimals ?? 1) + "%";
  },
  num: (n, decimals = 3) => n.toLocaleString("en-US", { minimumFractionDigits: decimals, maximumFractionDigits: decimals }),
};
