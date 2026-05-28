# Pressure Resistance

How to handle pressure to skip or reduce analysis scope.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Code works fine" | Working != maintainable. Analysis reveals hidden debt. |
| "Too time-consuming" | Cost of analysis < cost of compounding debt. |
| "Standards don't fit us" | Document YOUR standards, then analyse against those. |
| "Only critical matters" | Today's medium = tomorrow's critical. Document all. |
| "Legacy gets a pass" | Legacy needs analysis most — it sets precedent. |

## Analysis Completeness

All 4 dimensions should be covered unless the user explicitly scopes down:

| Deliverable | Required | Purpose |
|-------------|----------|---------|
| analysis-report.md | Yes | Document findings |
| tasks.md | Yes | Convert findings to actionable tasks |
| User approval | Yes | Get explicit decision on execution |

## Cancellation

If the user cancels at the approval step:

1. Ask why (briefly)
2. Save reason to `docs/refactor/{timestamp}/cancelled-reason.md`
3. Preserve partial analysis artifacts
