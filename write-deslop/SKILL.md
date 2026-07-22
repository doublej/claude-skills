---
name: write-deslop
description: Scan text for AI copywriting tells and rewrite them out — the delve-cluster vocabulary, negative parallelism ("it's not X, it's Y"), rule-of-three saturation, em-dash density, hedging, confident vagueness, and channel-specific slop (email, LinkedIn, sales copy). Use when the user asks to "deslop", "remove AI tells", "humanize this", "make this not sound like AI", "does this sound AI-written?", or wants copy audited/cleaned before publishing. Complements writer's clean.py (which only strips mechanical Unicode watermarks).
---

# write-deslop

Scan → fix → verify loop for de-AI-ing copy. The scanner is deterministic; the fix is a rewrite pass you perform guided by the catalog.

<workflow>
1. **Scan.** Text in a file: run directly. Inline text: write it to the scratchpad first.
   ```bash
   python3 ~/.claude/skills/write-deslop/scripts/scan.py <file>          # human-readable
   python3 ~/.claude/skills/write-deslop/scripts/scan.py <file> --json   # machine-readable
   ```
   Output: verdict (`clean` / `mild` / `heavy` / `saturated` / `smoking-gun`), density score per 1k words, and findings with line numbers and severity.

2. **Read the catalog.** Load `references/tells.md` — at minimum the sections matching flagged categories, plus ALWAYS `<substance>` and `<copy_specific>`: the scanner cannot detect missing specificity, both-sidesism, or the swap test. Those need a reading pass and are the highest-value fixes.

3. **Fix.** Rewrite following `<fix_principles>` below and the per-category "Fix:" lines in the catalog. Edit the user's file in place (or return rewritten text if it came inline).

4. **Verify.** Re-run scan.py. Target: verdict `clean` or `mild`, zero critical, and the reading-pass tells addressed. Report before/after scores.

5. **Mechanical layer (optional).** For email/paste destinations, `~/.claude/skills/writer/scripts/clean.py` strips Unicode watermarks, zero-width chars, and em-dashes mechanically — run it after the rewrite, not instead of it.
</workflow>

<fix_principles>
- **Preserve meaning, claims, and facts.** Deslop the prose, not the content. Never invent specifics — if the copy is vague because the source material has no numbers/names/dates, ask the user for them.
- **Density rule.** One em-dash or one "leverage" in clean surroundings is fine — humans use these too. Fix clusters, not singletons. Over-scrubbed text is its own tell ("syntax salad").
- **Fix substance before surface.** Swapping "delve" for "explore" changes nothing. The order of leverage: (1) add specifics / take a position, (2) break structural templates, (3) vary rhythm, (4) swap vocabulary.
- **Keep the user's voice.** Match their register, formality, and existing quirks; don't impose a house style.
- **One rhetorical device max.** Negative parallelism, tricolon, staccato — each is legitimate exactly once per piece, deliberately.
- **Rhythm = variance.** Add a 3-word sentence. Let one run long. Uneven paragraph mass reads human.
- **Channel matters.** Grade 5–7 readability for sales copy; short lines + one ask for email; 1–2 emoji for social. See `<channel_specific>` in the catalog.
</fix_principles>

<scanner_notes>
- scan.py masks fenced code blocks; it scans prose only.
- `smoking-gun` verdict = chat/placeholder leakage present ("as an AI", "[insert brand name]", "Let me know if you need modifications", `utm_source=chatgpt.com`) — fix those first, they are publication-blockers.
- Word findings are era-stamped (2024–26 lists) and the weakest signal tier; a `mild` verdict from word hits alone with good structure metrics is usually fine. Structure findings (low burstiness, em-dash saturation, bold-lead-in bullets) and phrase findings are stronger.
- The scanner produces false positives by design (e.g. "robust" in an engineering doc is fine). Judge each finding in context; report ignored findings as "kept: reason".
</scanner_notes>
