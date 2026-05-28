// Lucide icon subset, drawn as React components.
// Stroke 1.5 · inherit currentColor. Sized by parent (width/height props or CSS).
// Sourced from lucide.dev — keep paths byte-identical when adding more.

const Ico = (props) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width={props.size || 16}
    height={props.size || 16}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={props.strokeWidth || 1.5}
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
    {...props.svgProps}
    className={props.className}
    style={props.style}
  >
    {props.children}
  </svg>
);

const I = {
  Home: (p) => (<Ico {...p}><path d="M3 11 12 4l9 7"/><path d="M5 10v10h6v-6h2v6h6V10"/></Ico>),
  Search: (p) => (<Ico {...p}><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></Ico>),
  TrendingUp: (p) => (<Ico {...p}><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></Ico>),
  Wallet: (p) => (<Ico {...p}><rect x="3" y="6" width="18" height="14" rx="2"/><path d="M3 10h18"/><path d="M16 14h2"/></Ico>),
  Clock: (p) => (<Ico {...p}><circle cx="12" cy="12" r="9"/><path d="M12 8v4l3 2"/></Ico>),
  Bell: (p) => (<Ico {...p}><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10 21a2 2 0 0 0 4 0"/></Ico>),
  Settings: (p) => (<Ico {...p}><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/></Ico>),
  Download: (p) => (<Ico {...p}><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></Ico>),
  Plus: (p) => (<Ico {...p}><path d="M12 5v14M5 12h14"/></Ico>),
  Minus: (p) => (<Ico {...p}><path d="M5 12h14"/></Ico>),
  X: (p) => (<Ico {...p}><path d="M18 6 6 18M6 6l12 12"/></Ico>),
  Check: (p) => (<Ico {...p}><polyline points="20 6 9 17 4 12"/></Ico>),
  Chevron: (p) => (<Ico {...p}><polyline points="6 9 12 15 18 9"/></Ico>),
  ChevronRight: (p) => (<Ico {...p}><polyline points="9 18 15 12 9 6"/></Ico>),
  ArrowUp: (p) => (<Ico {...p}><path d="M12 19V5M5 12l7-7 7 7"/></Ico>),
  ArrowDown: (p) => (<Ico {...p}><path d="M12 5v14M19 12l-7 7-7-7"/></Ico>),
  ArrowRight: (p) => (<Ico {...p}><path d="M5 12h14M12 5l7 7-7 7"/></Ico>),
  ArrowLeftRight: (p) => (<Ico {...p}><path d="M8 3 4 7l4 4"/><path d="M4 7h16"/><path d="m16 21 4-4-4-4"/><path d="M20 17H4"/></Ico>),
  Filter: (p) => (<Ico {...p}><polygon points="22 3 2 3 10 12.5 10 19 14 21 14 12.5 22 3"/></Ico>),
  MoreH: (p) => (<Ico {...p}><circle cx="12" cy="12" r="1"/><circle cx="5" cy="12" r="1"/><circle cx="19" cy="12" r="1"/></Ico>),
  Eye: (p) => (<Ico {...p}><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></Ico>),
  EyeOff: (p) => (<Ico {...p}><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-10-7-10-7a18 18 0 0 1 4-5"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 10 7 10 7a17.7 17.7 0 0 1-2.16 3"/><path d="M1 1l22 22"/></Ico>),
  Info: (p) => (<Ico {...p}><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></Ico>),
  Alert: (p) => (<Ico {...p}><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/></Ico>),
  CircleCheck: (p) => (<Ico {...p}><circle cx="12" cy="12" r="10"/><polyline points="16 10 11 15 8 12"/></Ico>),
  CircleDot: (p) => (<Ico {...p}><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="2" fill="currentColor"/></Ico>),
  LineChart: (p) => (<Ico {...p}><path d="M3 3v18h18"/><path d="m7 14 4-4 3 3 6-6"/></Ico>),
  Layers: (p) => (<Ico {...p}><path d="m12 2 9 5-9 5-9-5 9-5z"/><path d="m3 12 9 5 9-5"/><path d="m3 17 9 5 9-5"/></Ico>),
  Building: (p) => (<Ico {...p}><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01M16 6h.01M8 10h.01M16 10h.01M8 14h.01M16 14h.01"/></Ico>),
  Coins: (p) => (<Ico {...p}><circle cx="8" cy="8" r="6"/><path d="M18.09 10.37A6 6 0 1 1 10.34 18M7 6h1v4M16.71 13.88l.7.71-2.82 2.82"/></Ico>),
  Receipt: (p) => (<Ico {...p}><path d="M4 2v20l3-2 3 2 3-2 3 2 3-2 1 2V2l-1 2-3-2-3 2-3-2-3 2-3-2z"/><path d="M16 8H8M16 12H8M13 16H8"/></Ico>),
  Refresh: (p) => (<Ico {...p}><path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/><path d="M3 21v-5h5"/></Ico>),
  Calendar: (p) => (<Ico {...p}><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></Ico>),
  Star: (p) => (<Ico {...p}><polygon points="12 2 15 8.5 22 9.3 17 14 18.2 21 12 17.8 5.8 21 7 14 2 9.3 9 8.5 12 2"/></Ico>),
  Logo: (p) => (
    <Ico {...p} svgProps={{ fill: "currentColor", stroke: "none" }} strokeWidth={0}>
      <rect x="2" y="2" width="20" height="20" rx="5"/>
      <path d="M7 7.5h10v2.4H7zM7 11h6v2.4H7zM7 14.5h10v2.4H7z" fill="var(--color-bg-elev, #fff)"/>
    </Ico>
  ),
};

window.I = I;
