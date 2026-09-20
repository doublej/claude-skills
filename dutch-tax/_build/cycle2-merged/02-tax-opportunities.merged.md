topic: 02-tax-opportunities

subtopics:
  kia:
    - claim: "KIA 2026: investment range €2,901–€71,683 → 28% deduction; if >€71,684 apply fixed €20,072 tapering"
      sources:
        - "note1#L175, L161"
        - "note3#C13150-13550"
      confidence: high
      contradictions: none

    - claim: "KIA applies to ZZP, VOF, BV entities with business investments"
      sources:
        - "note3#C9100-9200"
      confidence: high
      contradictions: none

    - claim: "KIA detection: summation of qualifying asset purchases with individual value >€450 within fiscal year"
      sources:
        - "note3#C9350-9500, C23100-23350"
      confidence: high
      contradictions: none

    - claim: "KIA classification risk: must exclude goodwill and passenger cars; low calculation risk"
      sources:
        - "note3#C13650-13800"
      confidence: high
      contradictions: none

    - claim: "KIA 'declining table' with deterministic deduction amounts; high automation fit for opportunity detection"
      sources:
        - "note2#L26, L298"
        - "deep-report#L87"
      confidence: high
      contradictions: none

  mkb-winstvrijstelling:
    - claim: "MKB-winstvrijstelling 2026: automatic 12.7% deduction of remaining profit (after ondernemersaftrek)"
      sources:
        - "note1#L180"
        - "note3#C14300-14450"
      confidence: high
      contradictions: none

    - claim: "Applies to ZZP, VOF, Eenmanszaak; zero calculation risk, purely mathematical execution"
      sources:
        - "note2#L297"
        - "note3#C14000-14150, C14500-14600"
      confidence: high
      contradictions: none

  zelfstandigenaftrek:
    - claim: "Zelfstandigenaftrek 2026: €1,200 annual allowance under listed conditions"
      sources:
        - "note1#L178, L161"
        - "note3#C14800-15000"
      confidence: high
      contradictions: "note2 states €2,470 for 2025 (L26); 2026 amount €1,200 confirmed in note1 and note3 — represents step-down toward 2027 abolition"

    - claim: "Eligibility: urencriterium met (≥1,225 hours/year), AOW status check, profit ≥ deduction amount; carryforward of unrealized amount"
      sources:
        - "note1#L178"
        - "note2#L295, L295-296"
        - "note3#C14800-15200"
      confidence: high
      contradictions: none

    - claim: "System should detect: eligibility, 2026 amount, AOW adjustment, unused carry-forward if low profit"
      sources:
        - "note1#L178"
      confidence: high
      contradictions: none

  startersaftrek:
    - claim: "Startersaftrek 2026: €2,123 when conditions met; additional deduction on top of zelfstandigenaftrek"
      sources:
        - "note1#L179"
        - "note3#C15050-15200"
      confidence: high
      contradictions: "note2 cites €2,123 for 2025 (L26); 2026 confirmed unchanged"

    - claim: "Eligibility: starter status, urencriterium met, hasn't used 3 times, max 3 uses; requires history tracking over prior 5 years"
      sources:
        - "note2#L208-209"
        - "note3#C15050-15200"
        - "deep-report#L92"
      confidence: high
      contradictions: none

    - claim: "Requires time-tracking logs and KVK registration date evidence; moderate risk for audit defense"
      sources:
        - "note3#C14700-14800, C15250-15450"
      confidence: medium
      contradictions: none

  urencriterium:
    - claim: "Urencriterium threshold: minimum 1,225 hours/year required; evidence required; pregnancy/disability rules apply"
      sources:
        - "note1#L177, L161"
        - "note2#L295, L569"
        - "note3#C14800-15000"
        - "deep-report#L90, L227"
      confidence: high
      contradictions: none

    - claim: "Detection logic: approved time entries, calendar, work categories; includes startup work, admin hours, interruptions"
      sources:
        - "note2#L295"
        - "deep-report#L90, L360"
      confidence: high
      contradictions: none

    - claim: "System should detect: whether logged hours plausibly meet 1,225; missing evidence; employee-time comparison"
      sources:
        - "note1#L177"
      confidence: high
      contradictions: none

  wbso-innovatiebox:
    - claim: "WBSO applies to ZZP, BV with R&D projects; identifies software development/engineering expenses linked to approved R&D"
      sources:
        - "note1#L184, L161"
        - "note2#L321"
        - "note3#C15550-15950"
      confidence: high
      contradictions: none

    - claim: "WBSO: year-versioned with percentage, bracket, optional forfait benefit; qualification requires S&O wages/hours, starter status, approved project"
      sources:
        - "note2#L321"
        - "deep-report#L101"
      confidence: high
      contradictions: none

    - claim: "Innovatiebox: 9% effective corporate tax rate on qualifying innovation profits; applies to BV/VPB companies with IP/R&D"
      sources:
        - "note1#L185"
        - "note2#L278"
        - "note3#C15550-15950"
      confidence: high
      contradictions: none

    - claim: "Innovatiebox: requires S&O statement and admin; high judgment content; year-versioned with thresholds and small/large taxpayer distinctions"
      sources:
        - "note1#L185"
        - "deep-report#L102"
      confidence: high
      contradictions: none

    - claim: "High risk of misclassification; strict accountant review mandatory; medium automation fit for candidate detection, low for final eligibility"
      sources:
        - "note3#C16350-16500"
        - "deep-report#L101-102"
      confidence: medium
      contradictions: none

    - claim: "System should detect: candidate R&D projects, future-only applications, required project admin; rule type Heuristic + RVO/accountant review"
      sources:
        - "note1#L184"
      confidence: high
      contradictions: none

  excessief-lenen:
    - claim: "Excess borrowing (Box 2): shareholder loans exceeding €500,000 (excluding mortgages on primary residence) trigger Box 2 deemed dividend"
      sources:
        - "note1#L188, L161"
        - "note3#C17050-17300"
        - "deep-report#L105"
      confidence: high
      contradictions: "note2 states €700,000 threshold (L320), this is the 2023 value; 2026 confirmed as €500,000 in note1, note3 and deep-report"

    - claim: "Applies to DGA (Director/Shareholder); detection via continuous monitoring of total DGA debt and connected persons to BV"
      sources:
        - "note3#C16650-16800, C16900-17050"
      confidence: high
      contradictions: none

    - claim: "System should detect: debt near/over threshold; connected persons; home-loan exceptions; generate urgent alert if balance nears €500,000 before year-end"
      sources:
        - "note1#L188"
        - "note3#C17350-17550"
      confidence: high
      contradictions: none

    - claim: "Low calculation risk; rule type is Deterministic + legal/accountant review; Risk is Very high"
      sources:
        - "note1#L188"
      confidence: high
      contradictions: none

  representatiekosten:
    - claim: "Representatiekosten (business gifts/meals) 2026: €5,700 non-deductible threshold OR deduct 80% (income tax) / 73.5% (VPB), select most favorable"
      sources:
        - "note1#L181"
        - "note3#C17800-18050"
      confidence: high
      contradictions: "note2 states 80% up to €4,600 (L484), older threshold; 2026 confirmed as €5,700"

    - claim: "Relatiegeschenken (business gifts) max €227 per recipient"
      sources:
        - "note2#L483"
      confidence: high
      contradictions: none

    - claim: "Applies to all entities; aggregate mixed-use promotional and relational expenses; rule type Deterministic + classification"
      sources:
        - "note1#L181"
        - "note3#C17650-17800"
      confidence: high
      contradictions: none

    - claim: "Moderate risk: AI must accurately distinguish between pure private expenses and valid representation costs"
      sources:
        - "note3#C18100-18300"
      confidence: medium
      contradictions: none

    - claim: "Belastingdienst rule: BTW on food/drink consumed on-premises NOT deductible as input tax; classify under representatiekosten"
      sources:
        - "note3#C24650-24850"
      confidence: high
      contradictions: none

  wkr:
    - claim: "WKR (Werkkostenregeling) applies to employers and DGA holdings"
      sources:
        - "note3#C18400-18550"
      confidence: high
      contradictions: none

    - claim: "WKR free space 2026: 2.00% on first €400,000 of wage sum; 1.18% above that; exceeding space triggers 80% final levy (eindheffing)"
      sources:
        - "note3#C18750-18950, C19000-19200"
      confidence: high
      contradictions: none

    - claim: "System must halt non-essential allowances if approaching limit; data required: fiscal wage sum, general ledger for employee benefits and untaxed allowances"
      sources:
        - "note3#C18550-18750"
      confidence: high
      contradictions: none

  btw-mixed-use:
    - claim: "VAT mixed-use applies to all entities using assets for both business and private purposes; VAT cannot be deducted for private use"
      sources:
        - "note1#L182"
        - "note3#C19300-19450"
      confidence: high
      contradictions: none

    - claim: "If VAT deducted initially for private-use portion, private-use VAT must be repaid; high automation fit"
      sources:
        - "note1#L182"
        - "deep-report#L95"
      confidence: high
      contradictions: none

    - claim: "Applies to phone, car, travel, home office, subscriptions, devices with private use; rule type Heuristic + accountant review"
      sources:
        - "note1#L182"
      confidence: high
      contradictions: none

    - claim: "Requires asset registry, mileage logs, private-use declarations; must calculate mandatory VAT correction for private use in final VAT return"
      sources:
        - "note3#C19450-19600, C19700-19900"
      confidence: high
      contradictions: none

    - claim: "Company car VAT correction: Belastingdienst gives 2.7% or 1.5% forfait where no private-use km administration exists; medium-high automation fit"
      sources:
        - "note1#L183"
        - "note3#C19950-20150"
        - "deep-report#L96"
      confidence: high
      contradictions: none

    - claim: "High risk; requires accurate mileage logs or application of standard Belastingdienst percentage correction"
      sources:
        - "note3#C19950-20150"
      confidence: medium
      contradictions: none

  dga-salary:
    - claim: "DGA salary (gebruikelijk loon): accountant-only decision; compare salary against reference norm; flag if too low or inefficient"
      sources:
        - "note2#L317"
      confidence: high
      contradictions: none

    - claim: "DGA salary norms: reference norm €56,000 (2025); monitored monthly; includes loans, payroll floor, dividend patterns"
      sources:
        - "note2#L681"
        - "deep-report#L5, L467"
      confidence: high
      contradictions: "2026 value not explicitly confirmed in any source — treat 2025 €56,000 as baseline; verify against Belastingdienst for 2026"

    - claim: "Detection: DGA/holding/excess-loan/gebruikelijk-loon patterns detected by BV/DGA edge-case detector"
      sources:
        - "deep-report#L388, L473-474"
      confidence: high
      contradictions: none

  other:
    - claim: "KOR (Kleineondernemersregeling): applies at ≤€20,000 turnover; participants do not charge VAT, file no VAT return, cannot deduct input VAT"
      sources:
        - "note1#L174"
        - "note2#L293"
        - "deep-report#L85"
      confidence: high
      contradictions: none

    - claim: "KOR detection: turnover near/under €20,000; whether VAT exemption helps or hurts because input VAT cannot be reclaimed"
      sources:
        - "note1#L174"
        - "note2#L293"
      confidence: high
      contradictions: none

    - claim: "Box 2 2026: rates 24.5% up to €68,843 and 31% above; system should detect dividend amount split across brackets, partner allocation"
      sources:
        - "note1#L186"
      confidence: high
      contradictions: none

    - claim: "Box 3 2026: provisional percentages 1.28% bank, 6% investments/other assets, 2.70% debts; tax-free allowance €59,357 single, €118,714 with partner"
      sources:
        - "note1#L187"
      confidence: high
      contradictions: none

    - claim: "Reverse-charge foreign VAT (btw verlegd): foreign entrepreneur transactions can trigger reverse-charge treatment; rule type Deterministic + review; Risk High"
      sources:
        - "note1#L173"
      confidence: high
      contradictions: none

    - claim: "VAT rates and compliance: 21%, 9%, 0%, exempt categories with different VAT deduction consequences; system should detect all variants"
      sources:
        - "note1#L170"
      confidence: high
      contradictions: none

    - claim: "VAT invoice compliance: legal name/address, VAT ID, KVK, date, unique invoice number, supply date, amount ex VAT, VAT rate/amount"
      sources:
        - "note1#L171"
      confidence: high
      contradictions: none

    - claim: "VAT corrections over €1,000 require suppletie form; smaller corrections can be processed in next VAT return"
      sources:
        - "note1#L172"
      confidence: high
      contradictions: none

    - claim: "BV/holding/DGA optimization: detect opportunities for fiscale eenheid, dividend planning; accountant-only decision"
      sources:
        - "note2#L318"
      confidence: high
      contradictions: none

    - claim: "30% ruling interaction with ZZP: detect if 30% ruling affects benefit calculations; heuristic detection; accountant verification essential"
      sources:
        - "note2#L310, L49"
      confidence: high
      contradictions: none

    - claim: "International transactions / ICP: flag intra-EU supplies; verify ICP reporting; deterministic rules with complex implications"
      sources:
        - "note2#L323"
      confidence: high
      contradictions: none

    - claim: "FOR (Fiscale Oudedagsreserve) abolition transition: existing FOR holders check pre-2023 balance, compute release rules"
      sources:
        - "note2#L299"
      confidence: high
      contradictions: none
