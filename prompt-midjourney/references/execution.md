# Getting prompts into Midjourney

This skill's default output is text: a prompt the user pastes. Read this only when the user wants
generation driven from the session, or asks about APIs and MCP servers.

<no_official_api>

As of 2026-07-27 there is **no official public Midjourney API**. No REST endpoint, no SDK, no
self-service API key, and **no consumer OAuth**. API access exists only through a restricted
Enterprise programme you apply for. Everything else on the market is unofficial.

That means there is no MCP server that authenticates as the user via Midjourney's own OAuth,
because Midjourney publishes no OAuth flow to authenticate against.

</no_official_api>

<paths>

| Path | Auth | Verdict |
|---|---|---|
| **Manual paste** | the user's own logged-in session | Default. Zero risk, zero setup |
| **Drive the user's own browser** (claude-in-chrome / Playwright) | the session already in their browser | Closest thing to "consumer auth". No third party, no tokens handled. Selectors on midjourney.com rot; treat as best-effort |
| **Session-token MCP** (e.g. `Lala-0x3f/mj-mcp`, GPL-3.0) | `TOKEN_R` / `TOKEN_I` cookies lifted from the logged-in browser | Not OAuth — replayed session cookies. Ships defaulting to `--v 6.1`. Tokens expire, and handing them to a process is a real credential exposure |
| **Third-party paid relay** (RunAPI, EvoLink, apiframe, useapi) | the relay's own API key; the relay holds a Midjourney account | Works and is stable, but the user pays twice and the relay sees every prompt |
| **Unofficial Discord clients** (`erictik/midjourney-api`, 1.8k⭐) | a Discord user token | Automating a user token is the most account-risky option |

</paths>

<caution>

Midjourney's terms restrict automated access. Browser automation of the user's own session sits in a
grey area; replayed session tokens and Discord user-token automation sit further out and have
historically drawn account action. Say this plainly once when the user asks for automation, then
respect their decision — it is their account.

Never write Midjourney session tokens into a repo, a config file under version control, or a shell
history. If the user wants token-based automation, route the secrets through `onenv`.

</caution>

<browser_path>

When driving the user's own browser:

1. Confirm they are logged in at midjourney.com and ask before the first submission.
2. Submit the prompt into the imagine bar; do not click anything that spends GPU minutes beyond what was agreed (Upscale, HD rerun, Vary) without saying so first.
3. Wait for all four images, then read them back into the session to score against `references/diagnostics.md`.
4. HD costs roughly 1.6x SD per job — explore in SD or Draft, and only rerun keepers as HD.

Cost discipline matters here: every iteration is real money from the user's plan. Batch changes
where the diagnostics allow it, and stop when the score plateaus rather than chasing the last 0.05.

</browser_path>
