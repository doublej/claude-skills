topic: 03-architecture
title: "Merged Architecture Layer — Deterministic + LLM Split, Evidence-First, Accountant-in-Loop"

subtopics:

  - name: deterministic-engine
    description: "Python deterministic tax calc engine for verified 2026 rules"
    facts:
      - claim: "Let LLM extract facts and classify; let deterministic code calculate VAT, KIA, KOR, deductions, Box thresholds"
        sources: ["note1#L139-140", "note3#L8950-9100"]
        confidence: high
        contradictions: none
        implementation_hints: "Python service with hardcoded verified 2026 tax tables (35.75% Box 1 Bracket 1, 21% VAT, KIA tiers, MKB 12.7%)"
        risk_class: "Low if properly versioned and tested; High if rules are stale or manually edited"

      - claim: "Deterministic engine is custom-built core IP; no comprehensive open-source library for all 2026 rules"
        sources: ["note3#L9200-9400", "deep-report#L28650-28900"]
        confidence: high
        contradictions: none
        implementation_hints: "Must manually code brackets, €500k excess borrowing logic, KIA taper algorithms, WKR percentages"
        risk_class: "High — requires annual maintenance for Prinsjesdag rule changes"

      - claim: "Must be deterministic: VAT rates, VAT return calcs, KOR turnover, KIA tiers, MKB-winstvrijstelling, zelfstandigenaftrek/startersaftrek, beperkt aftrekbare kosten, Box 2, Box 3, DGA excess-borrowing"
        sources: ["note1#L242-253"]
        confidence: high
        contradictions: none
        implementation_hints: "YAML/JSON rules with source URLs, effective dates, numeric parameters, eligibility predicates"
        risk_class: "Low if versioned; High if live-edited without regression tests"

  - name: rgs-normalization
    description: "Referentie Grootboekschema mapping for chart-of-accounts standardization"
    facts:
      - claim: "RGS is universal chart of accounts taxonomy used by Belastingdienst and CBS; standard available via 1truth.nl"
        sources: ["note3#L10100-10300", "note3#L36500-36700"]
        confidence: high
        contradictions: none
        implementation_hints: "Map proprietary user accounts to RGS taxonomy upon ingestion; query RGS codes independent of naming"
        risk_class: "Medium — adds complexity but essential for accountant acceptance and filing"

      - claim: "Essential for normalized chart-of-accounts mapping and filing compatibility; RGS linked to SBR"
        sources: ["deep-report#L19", "deep-report#L549-560"]
        confidence: high
        contradictions: none
        implementation_hints: "AI agent maps user ledger to RGS; deterministic engine queries specific RGS codes"
        risk_class: "Low if taxonomy is stable; Medium if changes occur mid-year"

  - name: mcp-layer
    description: "MCP-based ingestion from Moneybird, Exact, banks via read-write connectors"
    facts:
      - claim: "Moneybird official AI docs distinguish read-only from read-write; read-write excludes delete; production should start read-only"
        sources: ["note1#L146"]
        confidence: high
        contradictions: none
        implementation_hints: "moneybird-mcp-server (Node/MIT, 35 commits, read+write); exact-online-mcp-server (read-only OSS)"
        risk_class: "Low for read-only ingestion; High for writeback without approval gates"

      - claim: "MCP surfaces should be used as developer/operator tooling, not as tax reasoning engine"
        sources: ["deep-report#L560"]
        confidence: high
        contradictions: none
        implementation_hints: "Use Moneybird MCP for data transport; keep tax rules in separate deterministic modules"
        risk_class: "High if MCP becomes single source of truth for tax logic"

      - claim: "Ingestion layer: bank feeds via API (JSON), receipt extraction via email scraping/cloud storage, MCP server to accounting platform"
        sources: ["note3#C20600-20900", "note3#C20950-21200"]
        confidence: high
        contradictions: none
        implementation_hints: "Normalized transaction stream before tax reasoning; RGS mapping in pipeline"
        risk_class: "Medium — requires idempotency, deduplication, webhook retry handling"

  - name: exception-handling
    description: "Quarantine, classified/assumed/needs-review trichotomy for ambiguous items"
    facts:
      - claim: "Create explicit queues: missing receipt, low-confidence VAT, foreign supplier, mixed private/business, home-office, vehicle, KIA near threshold, DGA/shareholder-loan, WBSO candidate, related-party, large manual entry, bank/invoice/ledger mismatch"
        sources: ["note1#L274-289"]
        confidence: high
        contradictions: none
        implementation_hints: "Exception queue compiled into accountant review pack at month-end/quarter-end"
        risk_class: "Low if queue is monitored; High if items languish unreviewed"

      - claim: "When LLM confidence drops below threshold, transaction quarantined; system does not guess. Accountant resolves ambiguity"
        sources: ["note3#C9950-10100"]
        confidence: high
        contradictions: none
        implementation_hints: "Outcome states: classified, assumed_conservative, needs_user_input, needs_accountant_review"
        risk_class: "Low if thresholds are properly calibrated; High if too many false positives overwhelm accountant"

      - claim: "Allowed outcome states: classified, assumed_conservative, needs_user_input, needs_accountant_review, blocked_out_of_scope"
        sources: ["deep-report#L268"]
        confidence: high
        contradictions: none
        implementation_hints: "Each state has clear action: auto-post, flag for review, request input, escalate"
        risk_class: "Low if contract is enforced; High if states are ignored"

  - name: evidence-logging
    description: "7-year retention, audit trail, hash anchoring for defensible records"
    facts:
      - claim: "Each tax conclusion should produce: finding_id, tax_year, entity_id, tax_concept, input_records, rule_version, official_source_url, calculation_trace, llm_extraction_trace, confidence, review_status, reviewer_notes, final_action"
        sources: ["note1#L295-309"]
        confidence: high
        contradictions: none
        implementation_hints: "Makes system accountant-reviewable and defensible; every finding cites statute and source"
        risk_class: "Low if logging is comprehensive; High if traces are missing for material items"

      - claim: "Every deterministic calculation should emit: calc_id, module, rule_ids, source_urls, input_snapshot, evidence_ids, intermediate_steps, output_values, rounding_policy, generated_at, engine_version"
        sources: ["deep-report#L236"]
        confidence: high
        contradictions: none
        implementation_hints: "Calculation trace is critical for audit defense and reproducibility"
        risk_class: "Medium — requires strict structured logging; High if logs are unstructured"

      - claim: "Belastingdienst mandates 7-year business records retention; burden of proof on entrepreneur. Create cryptographic/database link between receipt, bank transaction, and applied tax rule"
        sources: ["note3#C13250-13450", "note3#C14000-14200"]
        confidence: high
        contradictions: none
        implementation_hints: "Vision model (Claude 3.5 Sonnet) OCR extraction; linking ensures audit defensibility"
        risk_class: "Low if evidence links are maintained; High if evidence is lost or orphaned"

  - name: accountant-in-loop
    description: "Handoff packs, signoff protocols, mandatory review gates before filing"
    facts:
      - claim: "Generate four packs: 1) Quarterly VAT (totals, source invoices, reverse-charge list, missing receipts); 2) Annual IB/VPB (P&L, balance sheet, asset register, deductions); 3) Opportunity (KIA/KOR/hours/WBSO/Box/DGA warnings); 4) Questions (accountant queries with evidence links)"
        sources: ["note1#L315-320"]
        confidence: high
        contradictions: none
        implementation_hints: "Packs are pre-generated, accountant-ready, with evidence IDs and rule citations"
        risk_class: "Low if packs are complete; High if packs are incomplete or contradictory"

      - claim: "Accountant-in-the-loop is mandatory, not optional. Every AI output carries disclaimer: 'Must be reviewed by qualified professional before filing.' System produces review packs, not final filings."
        sources: ["note2#L426"]
        confidence: high
        contradictions: none
        implementation_hints: "Safe-writeback approval flows; year-end requires accountant signature before KVK deposit"
        risk_class: "Low if human oversight is enforced; High if disclaimer is ignored"

      - claim: "Mandatory review before: filing VAT/IB/VPB, applying KOR, claiming KIA for ambiguous assets, home-office/car/mixed, WBSO/innovatiebox, BV/holding/DGA salary/dividend, moving money between entities, writing back corrections above materiality"
        sources: ["note1#L324-333"]
        confidence: high
        contradictions: none
        implementation_hints: "Define materiality threshold; escalate high-risk items automatically"
        risk_class: "Low if thresholds are enforced; High if bypass is possible"

  - name: rag-knowledge
    description: "RAG over Belastingdienst docs, RVO, RGS, OpenAccountants skills"
    facts:
      - claim: "Maintains localized knowledge base with latest Belastingdienst PDFs, tax treaties, KVK regulations. LLM uses RAG instead of base training weights"
        sources: ["note3#C12500-12700", "note3#C12750-12900"]
        confidence: high
        contradictions: none
        implementation_hints: "Belastbaar MCP as single source of truth for tax rates; never hardcode rates in prompts"
        risk_class: "Low if RAG is regularly refreshed; High if stale documents are used"

      - claim: "OpenAccountants skills govern LLM behavior; define classification contract (Classified/Assumed/Needs Input), conservative defaults, refusal catalogues, output formats"
        sources: ["note2#L424"]
        confidence: high
        contradictions: none
        implementation_hints: "Load skills conditionally to prevent hallucination; ban invented thresholds"
        risk_class: "Low if skills are versioned; High if they drift from official sources"

  - name: multi-agent
    description: "Pipeline shape: ingester → categorizer → reviewer → reporter"
    facts:
      - claim: "Data Inputs/Ingestion → MCP to Moneybird/Exact → Bookkeeping Normalization (RGS mapping) → LLM Reasoning (categorization, VAT review) → Deterministic Tax Engine (calc modules) → Exception Handling → Accountant Handoff"
        sources: ["note3#C20600-23050"]
        confidence: high
        contradictions: none
        implementation_hints: "Each stage has clear input/output contract; exception queue bridges LLM and deterministic"
        risk_class: "Low if pipeline is idempotent; High if stages are coupled or out of sync"

      - claim: "Two-stage classification: Stage 1 (deterministic) — vendor keyword dictionary 14 account categories × 100+ keywords, handles 70-90%; Stage 2 (LLM) — fallback for unknown with confidence high/medium → auto-book, low → flag"
        sources: ["note2#L156-172", "note2#L86"]
        confidence: high
        contradictions: none
        implementation_hints: "Reduces LLM load; deterministic-first pattern scales without liability"
        risk_class: "Low if fallback rate is monitored; High if dictionary is not maintained"

  - name: outcome-states
    description: "classified/assumed/needs-input/needs-accountant-review state machine"
    facts:
      - claim: "OpenAccountants uses three-outcome transaction pattern: classify when clear, assume conservatively when needed, route ambiguous to review. Ideal for Dutch tax because private/business mixed, VAT reverse charge, DGA items, home-office are high-risk"
        sources: ["note1#L142-143"]
        confidence: high
        contradictions: none
        implementation_hints: "Each outcome has clear next action; conservative default is permissible"
        risk_class: "Low if assumed-conservative is never auto-posted; High if it bypasses review"

      - claim: "Allowed outcome states: classified, assumed_conservative, needs_user_input, needs_accountant_review, blocked_out_of_scope"
        sources: ["deep-report#L268"]
        confidence: high
        contradictions: none
        implementation_hints: "Map to action: classified → auto-post after batch review, assumed → flag for accountant, needs_input → request from user, review → escalate, blocked → skip"
        risk_class: "Low if states are enforced; High if mixed"

  - name: read-only-first
    description: "Connector pattern starting read-only, generating proposed entries, requiring human approval before writeback"
    facts:
      - claim: "Production should start read-only, generate proposed journal entries/corrections, then require human approval before writeback. Moneybird MCP distinguishes read-only from read-write; read-write excludes delete"
        sources: ["note1#L146"]
        confidence: high
        contradictions: none
        implementation_hints: "Safe-writeback workflow: LLM proposes, deterministic validates, accountant approves"
        risk_class: "Low if approval gates are enforced; High if read-write access is premature"

      - claim: "Safe-writeback approval flows require accountant review before material changes. Every material output traceable to evidence and deterministic rules"
        sources: ["deep-report#L7", "deep-report#L470"]
        confidence: high
        contradictions: none
        implementation_hints: "Define materiality threshold (e.g., €500); block writeback if evidence missing"
        risk_class: "Low if approval is mandatory; High if bypass is possible"

  - name: receipt-extraction
    description: "OCR / vision pipeline for document ingestion and field extraction"
    facts:
      - claim: "Speedy extracts supplier, amounts, VAT, ledger suggestions from invoices and connects to bookkeeping actions. LinkedIn VAT workflow organizes quarter folders; model extracts amounts, VAT, categories, missing items, source references"
        sources: ["note1#L149"]
        confidence: high
        contradictions: none
        implementation_hints: "Claude 3.5 Sonnet vision for OCR cleanup; structured JSON extraction"
        risk_class: "Low if OCR is validated; High if hallucinated fields are used for tax calc"

      - claim: "Automated extraction pipeline: scrape designated email inboxes, extract PDF/image attachments, process via OCR, create cryptographic/database link between receipt and applied rule"
        sources: ["note3#C13500-13950"]
        confidence: high
        contradictions: none
        implementation_hints: "Email authentication, attachment dedup, LLM feeding; requires custom orchestration (n8n, Pipedream, Python cron)"
        risk_class: "Medium — requires robust error handling, retry logic, duplicate detection"

      - claim: "Receipt Extraction Pipeline requires custom orchestration despite Claude 3.5 Sonnet OCR capability. Must handle email auth, attachment extraction, deduplication, LLM feeding automatically"
        sources: ["deep-report#L696-700"]
        confidence: high
        contradictions: none
        implementation_hints: "Moderate custom build; not trivial but well-scoped"
        risk_class: "Medium — operational complexity; Low tax risk if validations are in place"

  - name: continuous-auditing
    description: "Quarterly scanner pattern for proactive opportunity detection and risk flagging"
    facts:
      - claim: "Cron-triggered batch processing performs continuous auditing; inverts traditional retroactive accounting. End of each quarter: optimization agent scans cumulative ledger. Example: if €2,500 in KIA-qualifying investments by Nov, alert if additional €401 by Dec 31 triggers 28% deduction"
        sources: ["note3#C11450-12250"]
        confidence: high
        contradictions: none
        implementation_hints: "Automated schedulers on Oct 1, monthly until Dec 31; alert-driven workflow"
        risk_class: "Low if alerts are reviewed; High if alerts are ignored"

      - claim: "Quarterly opportunity scan runs Oct 1 and monthly thereafter until Dec 31. Checks KIA (sum assets > €450, approaching €2,901), Excess Borrowing (DGA > €450k), WKR Free Space. Generates actionable executive summary"
        sources: ["note3#C25150-26200"]
        confidence: high
        contradictions: none
        implementation_hints: "Inputs: YTD trial balance mapped to RGS, asset registry, DGA current account"
        risk_class: "Low if thresholds are accurate; High if calculations are stale"

      - claim: "System should surface opportunities: KIA threshold nearly reached, KOR may be beneficial, hours evidence insufficient, DGA loan near excess-borrowing threshold, WBSO candidate. Should NOT present aggressive positions as advice"
        sources: ["note1#L155"]
        confidence: high
        contradictions: none
        implementation_hints: "Opportunity scanner is detection + explanation, not recommendation engine"
        risk_class: "Low if tone is cautious; High if framed as tax advice"
