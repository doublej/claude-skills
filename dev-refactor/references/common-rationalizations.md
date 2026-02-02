# Pressure Resistance & Rationalizations

Handling pressure to skip or reduce analysis scope.

## Pressure Resistance

Codebase analysis is MANDATORY when requested. Responses to pressure:

| Pressure Type | Request | Agent Response |
|---------------|---------|----------------|
| **Works Fine** | "Code works, skip analysis" | "Working != maintainable. Analysis reveals hidden technical debt." |
| **Time** | "No time for full analysis" | "Partial analysis = partial picture. Technical debt compounds daily." |
| **Legacy** | "Standards don't apply to legacy" | "Legacy code needs analysis MOST. Document gaps for improvement." |
| **Critical Only** | "Only fix critical issues" | "Medium issues become critical. Document all, prioritize later." |

**Non-negotiable:** If user requests refactoring analysis, complete ALL 4 dimensions (Architecture, Code, Testing, DevOps).

## Common Rationalizations - REJECTED

| Excuse | Reality |
|--------|---------|
| "Code works fine" | Working != maintainable. Analysis finds hidden debt. |
| "Too time-consuming" | Cost of analysis < cost of compounding debt. |
| "Standards don't fit us" | Then document YOUR standards. Analysis still reveals gaps. |
| "Only critical matters" | Today's medium = tomorrow's critical. Document all. |
| "Legacy gets a pass" | Legacy sets precedent. Analysis shows what to improve. |
| "Team has their own way" | Document "their way" as standards. Analyze against it. |
| "ROI of refactoring is low" | ROI calculation requires analysis. You can't calculate without data. |
| "Partial analysis is enough" | Partial analysis = partial picture. Hidden debt in skipped areas. |
| "3 years without bugs = stable" | No bugs != no debt. Time doesn't validate architecture. |
| "Analysis is overkill" | Analysis is the MINIMUM. Refactoring without analysis is guessing. |
| "Code smells != problems" | Code smells ARE problems. They slow development and cause bugs. |
| "No specific problem motivating" | Technical debt IS the problem. Analysis quantifies it. |
| "Analysis complete, user can decide" | Analysis without action guidance is incomplete. Provide tasks.md. |
| "Findings documented, my job done" | Findings -> Tasks -> Execution. Documentation alone changes nothing. |

## Red Flags - STOP

If you catch yourself thinking ANY of these, STOP immediately:

- "Code works, no need to analyze"
- "This is too time-consuming"
- "Standards don't apply here"
- "Only critical issues matter"
- "Legacy code is exempt"
- "That's just how we do it here"
- "ROI doesn't justify full analysis"
- "Partial analysis is sufficient"
- "3+ years stable = no debt"
- "Analysis is overkill"
- "Code smells aren't real problems"
- "No specific problem to solve"
- "Analysis is done, user decides next"
- "Documented findings, job complete"

**All of these indicate analysis violation. Complete full 4-dimension analysis.**

## Analysis-to-Action Pipeline - MANDATORY

Analysis without action guidance is incomplete:

| Deliverable | Required? | Purpose |
|-------------|----------|---------|
| analysis-report.md | YES | Document findings |
| tasks.md | YES | Convert findings to actionable tasks |
| User approval prompt | YES | Get explicit decision on execution |

**Completion checklist:**
- [ ] All 4 dimensions analyzed
- [ ] Findings categorized by severity
- [ ] Findings converted to REFACTOR-XXX tasks
- [ ] tasks.md generated in PM Team format
- [ ] User presented with approval options

**"Analysis complete" means tasks.md exists and user has been asked to approve.**

## Cancellation Documentation

If user cancels analysis at approval step:

1. **ASK:** "Why is analysis being cancelled?"
2. **DOCUMENT:** Save reason to `docs/refactor/{timestamp}/cancelled-reason.md`
3. **PRESERVE:** Keep partial analysis artifacts
4. **NOTE:** "Analysis cancelled by user: [reason]. Partial findings preserved."

**Cancellation without documentation is NOT allowed.**
