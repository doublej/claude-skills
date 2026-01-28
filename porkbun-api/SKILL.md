---
name: porkbun-api
description: Manage Porkbun domains and DNS via API. Use for domain management, DNS records (A, CNAME, MX, TXT), nameservers, SSL certs, pricing, or URL forwarding on Porkbun. Triggers on "Porkbun", "add DNS record", "point domain to", "update nameservers".
---

# Porkbun API

Manage domains and DNS through the Porkbun API.

## Setup

Set environment variables:
```bash
export PORKBUN_API_KEY="pk1_..."
export PORKBUN_SECRET_KEY="sk1_..."
```

Get API keys from: https://porkbun.com/account/api

## Quick Reference

Base URL: `https://api.porkbun.com/api/json/v3`

All requests: HTTP POST with JSON body containing `apikey` and `secretapikey`.

## CLI Script

Use `scripts/porkbun.py` for common operations:

```bash
# Test authentication
uv run python scripts/porkbun.py ping

# List all domains
uv run python scripts/porkbun.py domains

# Check domain availability
uv run python scripts/porkbun.py check example.com

# DNS operations
uv run python scripts/porkbun.py dns list example.com
uv run python scripts/porkbun.py dns add example.com A 192.168.1.1 --name=api --ttl=600
uv run python scripts/porkbun.py dns delete example.com 123456

# Nameservers
uv run python scripts/porkbun.py ns get example.com
uv run python scripts/porkbun.py ns set example.com ns1.provider.com ns2.provider.com

# URL Forwarding
uv run python scripts/porkbun.py forward list example.com
uv run python scripts/porkbun.py forward add example.com https://target.com temporary
uv run python scripts/porkbun.py forward add example.com https://target.com permanent --subdomain=www --includepath
uv run python scripts/porkbun.py forward delete example.com 123456

# SSL certificate
uv run python scripts/porkbun.py ssl example.com

# Pricing (no auth needed)
uv run python scripts/porkbun.py pricing
```

## Common Tasks

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

## Error Handling

- `status: "SUCCESS"` = OK
- `status: "ERROR"` + `message` = failure reason
- HTTP 403 = enable API access in Porkbun account settings

## Full API Reference

See [references/api_reference.md](references/api_reference.md) for complete endpoint documentation.
