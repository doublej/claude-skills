---
name: porkbun-api
description: "Domain and DNS management: records, nameservers, SSL, URL forwarding"
---

# Porkbun API

Manage domains and DNS through the Porkbun API.

<setup>
Credentials come from onenv (1Password) — never `export`, never a `.env` file.
The `porkbun` namespace holds `PORKBUN_API_KEY` and `PORKBUN_SECRET_KEY`.

Prefix every command that talks to the API:
```bash
onenv export porkbun -- python3 ~/.claude/skills/porkbun-api/scripts/porkbun.py ping
```

`onenv export` works from any directory. `onenv run` does not — it needs a
project-level `.onenv.json` and fails with `NO_PROJECT_CONFIG` without one.

Keys are managed at https://porkbun.com/account/api and stored with
`onenv set porkbun PORKBUN_API_KEY`.
</setup>

<reference>
## Quick Reference

Base URL: `https://api.porkbun.com/api/json/v3`

All requests: HTTP POST with JSON body containing `apikey` and `secretapikey`.
</reference>

<cli>
## CLI Script

Use `scripts/porkbun.py` for common operations. The script is stdlib-only — no
`uv run`, no venv. Always call it by absolute path so it works from whatever
project you happen to be in; a relative `scripts/porkbun.py` only resolves when
cwd is the skill directory. Each line below is a complete command:

```bash
PB=~/.claude/skills/porkbun-api/scripts/porkbun.py   # or the repo path

# Test authentication
onenv export porkbun -- python3 $PB ping

# List all domains
onenv export porkbun -- python3 $PB domains

# Check domain availability
onenv export porkbun -- python3 $PB check example.com

# DNS operations
onenv export porkbun -- python3 $PB dns list example.com
onenv export porkbun -- python3 $PB dns add example.com A 192.168.1.1 --name=api --ttl=600
onenv export porkbun -- python3 $PB dns delete example.com 123456

# Nameservers
onenv export porkbun -- python3 $PB ns get example.com
onenv export porkbun -- python3 $PB ns set example.com ns1.provider.com ns2.provider.com

# URL Forwarding
onenv export porkbun -- python3 $PB forward list example.com
onenv export porkbun -- python3 $PB forward add example.com https://target.com temporary
onenv export porkbun -- python3 $PB forward add example.com https://target.com permanent --subdomain=www --includepath
onenv export porkbun -- python3 $PB forward delete example.com 123456

# SSL certificate
onenv export porkbun -- python3 $PB ssl example.com

# Pricing (no auth needed)
python3 $PB pricing
```

`$PB` is set in the same shell invocation as the command that uses it — shell
state does not survive between separate tool calls, so set it inline (`PB=...;
onenv export porkbun -- python3 $PB ping`) or just paste the full path.

</cli>

<common_tasks>
### Add A Record
```python
import urllib.request, json, os

data = {
    "apikey": os.environ["PORKBUN_API_KEY"],
    "secretapikey": os.environ["PORKBUN_SECRET_KEY"],
    "type": "A",
    "content": "192.168.1.1",
    "name": "api",  # subdomain, empty for root
    "ttl": "600"
}
req = urllib.request.Request(
    "https://api.porkbun.com/api/json/v3/dns/create/example.com",
    data=json.dumps(data).encode(),
    headers={"Content-Type": "application/json"}
)
resp = urllib.request.urlopen(req)
print(json.loads(resp.read()))
```

### Add CNAME Record
```python
data = {
    "apikey": os.environ["PORKBUN_API_KEY"],
    "secretapikey": os.environ["PORKBUN_SECRET_KEY"],
    "type": "CNAME",
    "content": "target.example.com",
    "name": "www"
}
# POST to /dns/create/{domain}
```

### Add MX Record
```python
data = {
    "apikey": os.environ["PORKBUN_API_KEY"],
    "secretapikey": os.environ["PORKBUN_SECRET_KEY"],
    "type": "MX",
    "content": "mail.example.com",
    "prio": "10"
}
```

### Add TXT Record (SPF/DKIM/DMARC)
```python
data = {
    "apikey": os.environ["PORKBUN_API_KEY"],
    "secretapikey": os.environ["PORKBUN_SECRET_KEY"],
    "type": "TXT",
    "content": "v=spf1 include:_spf.google.com ~all"
}
```

### Update Nameservers to Cloudflare
```python
data = {
    "apikey": os.environ["PORKBUN_API_KEY"],
    "secretapikey": os.environ["PORKBUN_SECRET_KEY"],
    "ns": ["ns1.cloudflare.com", "ns2.cloudflare.com"]
}
# POST to /domain/updateNs/{domain}
```
</common_tasks>

<dns_types>
## DNS Record Types

| Type | Purpose | Content Example |
|------|---------|-----------------|
| A | IPv4 address | `192.168.1.1` |
| AAAA | IPv6 address | `2001:db8::1` |
| CNAME | Alias | `target.example.com` |
| MX | Mail server | `mail.example.com` (+ prio) |
| TXT | Text/verification | `v=spf1 ...` |
| NS | Nameserver | `ns1.example.com` |
| SRV | Service | `0 5 5060 sipserver.example.com` |
| CAA | Certificate auth | `0 issue "letsencrypt.org"` |
</dns_types>

<error_handling>
- `status: "SUCCESS"` = OK
- `status: "ERROR"` + `message` = failure reason
- HTTP 403 = enable API access in Porkbun account settings
</error_handling>

## Full API Reference

See [references/api_reference.md](references/api_reference.md) for complete endpoint documentation.
