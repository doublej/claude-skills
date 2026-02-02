# Porkbun API Reference

Base URL: `https://api.porkbun.com/api/json/v3`
Alternative IPv4: `https://api-ipv4.porkbun.com/api/json/v3`

All requests use HTTP POST with JSON payloads. Every request requires `apikey` and `secretapikey`.

## Domain Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/domain/listAll` | List all domains (optional: `start`, `includeLabels`) |
| `/domain/checkDomain/{DOMAIN}` | Check availability (rate-limited) |
| `/domain/getNs/{DOMAIN}` | Get nameservers |
| `/domain/updateNs/{DOMAIN}` | Update nameservers (`ns` array) |
| `/domain/addUrlForward/{DOMAIN}` | Add redirect (`location`, `type`, `includePath`, `wildcard`, optional `subdomain`) |
| `/domain/getUrlForwarding/{DOMAIN}` | Get URL forwards |
| `/domain/deleteUrlForward/{DOMAIN}/{ID}` | Delete forward |
| `/domain/createGlue/{DOMAIN}/{HOST}` | Create glue record (`ips` array) |
| `/domain/updateGlue/{DOMAIN}/{HOST}` | Update glue record (`ips` array) |
| `/domain/deleteGlue/{DOMAIN}/{HOST}` | Delete glue record |
| `/domain/getGlue/{DOMAIN}` | Get glue records |

## DNS Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/dns/create/{DOMAIN}` | Create record (`type`, `content`, optional: `name`, `ttl`, `prio`, `notes`) |
| `/dns/retrieve/{DOMAIN}` | Get all records |
| `/dns/retrieve/{DOMAIN}/{ID}` | Get single record |
| `/dns/retrieveByNameType/{DOMAIN}/{TYPE}/{SUBDOMAIN}` | Get by subdomain+type |
| `/dns/edit/{DOMAIN}/{ID}` | Edit by ID (`type`, `content`, optional: `name`, `ttl`, `prio`, `notes`) |
| `/dns/editByNameType/{DOMAIN}/{TYPE}/{SUBDOMAIN}` | Edit by subdomain+type (`content`) |
| `/dns/delete/{DOMAIN}/{ID}` | Delete by ID |
| `/dns/deleteByNameType/{DOMAIN}/{TYPE}/{SUBDOMAIN}` | Delete by subdomain+type |

**DNS Types:** A, AAAA, MX, CNAME, ALIAS, TXT, NS, SRV, TLSA, CAA, HTTPS, SVCB, SSHFP

## DNSSEC Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/dns/createDnssecRecord/{DOMAIN}` | Create DS record (`keyTag`, `alg`, `digestType`, `digest`) |
| `/dns/getDnssecRecords/{DOMAIN}` | Get DNSSEC records |
| `/dns/deleteDnssecRecord/{DOMAIN}/{KEYTAG}` | Delete DNSSEC record |

## SSL Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/ssl/retrieve/{DOMAIN}` | Get SSL bundle (cert chain, private key, public key) |

## Utility Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/ping` | Test auth, returns client IP |
| `/pricing/get` | Get TLD pricing (no auth needed) |

## Response Format

Success:
```json
{"status": "SUCCESS", ...data}
```

Error:
```json
{"status": "ERROR", "message": "error description"}
```

HTTP 403 = missing 2FA on account.
