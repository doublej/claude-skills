# Commercial Bookkeeping Platforms

16 SaaS and commercial platforms used by Dutch ZZP, BV, accounting firms. Summary of APIs, AI integration claims, and recommendation for first integration.

---

## Best-First Integration

### Moneybird

- **Official site:** https://www.moneybird.com
- **API surface:** Official REST API with webhooks, idempotency keys, official MCP launch
- **Entities exposed:** Contacts, invoices, accounts, products, projects, time entries, subscriptions, financial reports
- **Tax-specific:** VAT tax rates, ledger IDs, VAT codes in API flows
- **AI integration:** Official "AI-koppeling" page lists Claude, ChatGPT, Cursor, Mistral as supported
- **Read/Write:** Read-only recommended for production start; write available (excludes delete)
- **NL focus:** Very high. Dominant Dutch SMB bookkeeping platform.
- **ZZP recommendation:** Yes. Best choice for MVP and scaling.
- **BV recommendation:** Yes. Works for BV as well.
- **Caveat:** Does not natively optimize for tax planning; requires agent prompting for smart categorization.
- **Maturity:** Production. Widely adopted.

---

## Second-Tier Integration

### e-Boekhouden

- **Official site:** https://www.e-boekhouden.nl
- **API surface:** REST API wrapper with strong public patterns
- **Entities exposed:** Invoices, ledgers, mutations, relations, cost centers, VAT codes
- **AI integration:** Community-driven; no official AI partnerships documented
- **Read/Write:** Full via REST API
- **NL focus:** Very high. Major Dutch online bookkeeping platform.
- **ZZP recommendation:** Yes. Widely used by Dutch ZZP.
- **BV recommendation:** Limited. Better for micro/solo businesses.
- **Caveat:** No official MCP yet; integration requires custom REST client.
- **Maturity:** Production.

### Exact Online

- **Official site:** https://www.exact.com/nl
- **API surface:** REST API (official) + CData JDBC/MCP (read-only wrapper)
- **Entities exposed:** GL accounts, journals, invoices, contacts, payments, tax lines
- **AI integration:** No official AI partnerships; read-only MCP available via CData
- **Read/Write:** REST API supports read+write; CData MCP is read-only
- **NL focus:** High. Enterprise ERP used by Dutch mid-market accounting firms.
- **ZZP recommendation:** Not ideal. Aimed at larger structures.
- **BV recommendation:** Yes. Enterprise-grade for larger BVs.
- **Caveat:** Enterprise pricing; more complexity than Moneybird.
- **Maturity:** Production. Mature platform.

---

## Single-Agent Automation Platforms (Rule-First)

### Jortt

- **Official site:** https://www.jortt.nl/boekhouding-zzp/
- **API surface:** REST API for bookkeeping operations
- **Capabilities:** Bank mutation categorization, invoice/payment matching, VAT placement, automatic controls, annual accounts, IB reporting, KIA reporting, year-close checklists
- **AI integration:** "Boekhoudbot" (rule-based assistant); positions AI as **explanation/advice**, not decision-maker
- **Philosophy:** "Bookkeeping should follow fixed hard rules; AI is helpful for advice/explanation"
- **Integrations:** 60+
- **Built on:** Belastingdienst rules
- **Users:** Real ZZP'ers and small BVs
- **ZZP recommendation:** Yes. Best-in-class rule-driven pattern.
- **BV recommendation:** Yes, for small BVs.
- **Caveat:** Less customizable than Moneybird for LLM integration.
- **Maturity:** Production. Reference for deterministic architecture.

---

## Mid-Market Platforms

### AFAS Software

- **Official site:** https://www.afas.nl
- **API surface:** REST and SOAP APIs
- **NL focus:** High. Dutch ERP vendor.
- **AI integration:** No official AI partnerships documented
- **ZZP recommendation:** No. Aimed at larger businesses.
- **BV recommendation:** Yes, for mid-market BVs.
- **Maturity:** Production.

### Yuki

- **Official site:** https://www.yukiapp.nl
- **API surface:** (Not fully documented in sources; assume REST/GraphQL)
- **NL focus:** High. Modern Dutch accounting platform.
- **AI integration:** "Yuki Robotic Assistant" claims AI-driven document recognition (IDR); **maturity unclear (medium confidence)**
- **ZZP recommendation:** Possibly. Growing platform.
- **BV recommendation:** Yes.
- **Maturity:** Production; AI features claim stale 2025 values.

### SnelStart

- **Official site:** https://www.snelstart.nl
- **API surface:** Official developer surface / REST API
- **NL focus:** High. Dutch SMB platform.
- **AI integration:** No official AI partnerships documented
- **ZZP recommendation:** Yes. Common for Dutch ZZP.
- **BV recommendation:** Yes.
- **Maturity:** Production.

### Twinfield (Wolters Kluwer)

- **Official site:** https://www.twinfield.com
- **API surface:** SOAP-heavy (enterprise style)
- **NL focus:** High. Enterprise accounting platform.
- **AI integration:** No official AI partnerships
- **ZZP recommendation:** No. Enterprise-focused.
- **BV recommendation:** Yes, for larger BVs / accounting firms.
- **Maturity:** Production.

### Rompslomp

- **Official site:** (Dutch bookkeeping platform)
- **API surface:** Public API support pages
- **NL focus:** High.
- **AI integration:** Not documented
- **ZZP recommendation:** Possibly. Niche platform.
- **BV recommendation:** Limited.
- **Maturity:** Production.

---

## AI-First Platforms & Tools

### Boekie AI

- **Official site:** (Dutch AI bookkeeping platform)
- **Claims:** Exact Online and e-Boekhouden integrations, bank transaction processing, purchase/sales invoice OCR, automatic VAT calculation, ledger mapping, learning from corrections, confidence scoring
- **Maturity:** **Medium confidence.** Claims stale or not independently verified.
- **ZZP recommendation:** Possibly. Competitive with Jortt.
- **BV recommendation:** Limited information.

### Paperdork

- **Official site:** (Dutch bookkeeping dashboard)
- **Claims:** KIA threshold dashboard, urencriterium tracking, zelfstandigenaftrek, startersaftrek tax-benefit insights
- **Maturity:** **Medium confidence.** Tax-specific features; claims not verified.
- **ZZP recommendation:** Yes. Tax-focused.
- **BV recommendation:** Limited.

### BTW Vriend

- **Official site:** (Dutch ZZP/VOF bookkeeping)
- **Claims:** VAT tracking, invoices, receipts, KIA benefit calculation, zelfstandigenaftrek, startersaftrek, MKB-winstvrijstelling
- **Maturity:** **Medium confidence.** Claims not verified.
- **ZZP recommendation:** Yes.
- **BV recommendation:** No.

### Fiscaal Agent / Virtual Outcomes

- **Official site:** (Dutch tax scenario planning)
- **Claims:** VAT calculators, urencriterium tracking, belastingdruk calculators, scenario planning, ZZP-vs-BV considerations
- **Maturity:** **Medium confidence.** Planning tool, not real-time bookkeeping.
- **ZZP recommendation:** Yes. For planning/advice.
- **BV recommendation:** Yes. For planning/advice.

### GekkoBot

- **Official site:** (Dutch AI tax chatbot)
- **Claims:** First Dutch AI tax advisor chatbot (launched 2023); built on ChatGPT; integrated with Gekko bookkeeping platform; now likely superseded
- **Maturity:** Low. **Stale 2023 reference.** Likely outdated.
- **ZZP recommendation:** Historical interest only.

### ZZP Pulse Expense Classifier

- **Official site:** (Free Dutch ZZP tool)
- **What:** Simple free AI tool that classifies expenses for BTW and income tax from uploaded bank statements
- **Maturity:** Early. Prototype-grade.
- **ZZP recommendation:** Yes. Free learning tool.

### BTWmate

- **Official site:** (Dutch VAT management)
- **Claims:** Cloud VAT management, automated tracking, pre-filled returns, receipt capture, deadline reminders
- **Maturity:** **Medium confidence.** Claims not independently verified.
- **ZZP recommendation:** Yes. VAT-focused.

---

## Maturity Summary

| Platform | ZZP | BV | API | AI | Recommended |
|----------|-----|----|----|----|----|
| Moneybird | ✓ | ✓ | MCP | Official | **YES** |
| e-Boekhouden | ✓ | ✓ | REST | Custom | Yes |
| Exact Online | ✗ | ✓ | REST/MCP | No | Enterprise |
| Jortt | ✓ | ✓ | REST | Rules | Reference |
| AFAS | ✗ | ✓ | SOAP/REST | No | Large BV |
| Yuki | ✓ | ✓ | ? | Claimed | Emerging |
| SnelStart | ✓ | ✓ | REST | No | Yes |
| Twinfield | ✗ | ✓ | SOAP | No | Enterprise |
| Rompslomp | ✓ | ✓ | REST | No | Niche |
| Boekie AI | ✓ | ✓ | Embedded | Yes | Beta |
| Paperdork | ✓ | ✗ | ? | Dashboard | Research |
| BTW Vriend | ✓ | ✗ | ? | No | Niche |
| Fiscaal Agent | ✓ | ✓ | ? | Planning | Advisory |
| GekkoBot | ✓ | ✗ | ? | ChatGPT | Outdated |
| ZZP Pulse | ✓ | ✗ | ? | Free | Learning |
| BTWmate | ✓ | ✗ | ? | Tracking | Niche |

---

**Sources:** note1, note2, note3, deep-report
