#!/usr/bin/env python3
"""
Porkbun API CLI - Domain and DNS management

Usage:
  uv run python porkbun.py ping
  uv run python porkbun.py domains
  uv run python porkbun.py check <domain>
  uv run python porkbun.py dns list <domain>
  uv run python porkbun.py dns add <domain> <type> <content> [--name=<subdomain>] [--ttl=<ttl>]
  uv run python porkbun.py dns delete <domain> <id>
  uv run python porkbun.py ns get <domain>
  uv run python porkbun.py ns set <domain> <ns1> <ns2> [<ns3>] [<ns4>]
  uv run python porkbun.py forward list <domain>
  uv run python porkbun.py forward add <domain> <location> <type> [--subdomain=<sub>] [--includepath] [--wildcard]
  uv run python porkbun.py forward delete <domain> <id>
  uv run python porkbun.py ssl <domain>
  uv run python porkbun.py pricing

Requires PORKBUN_API_KEY and PORKBUN_SECRET_KEY environment variables.
"""
import os
import sys
import json
import urllib.request
import urllib.error

BASE_URL = "https://api.porkbun.com/api/json/v3"

def get_credentials():
    api_key = os.environ.get("PORKBUN_API_KEY")
    secret_key = os.environ.get("PORKBUN_SECRET_KEY")
    if not api_key or not secret_key:
        print("Error: Set PORKBUN_API_KEY and PORKBUN_SECRET_KEY environment variables")
        sys.exit(1)
    return api_key, secret_key

def api_request(endpoint, data=None, auth=True):
    url = f"{BASE_URL}{endpoint}"
    payload = data or {}
    if auth:
        api_key, secret_key = get_credentials()
        payload["apikey"] = api_key
        payload["secretapikey"] = secret_key

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        try:
            return json.loads(error_body)
        except:
            return {"status": "ERROR", "message": error_body}

def cmd_ping():
    result = api_request("/ping")
    if result.get("status") == "SUCCESS":
        print(f"OK - Your IP: {result.get('yourIp', 'unknown')}")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")

def cmd_domains():
    result = api_request("/domain/listAll")
    if result.get("status") == "SUCCESS":
        domains = result.get("domains", [])
        if not domains:
            print("No domains found")
            return
        for d in domains:
            exp = d.get("expireDate", "?")[:10]
            print(f"{d.get('domain'):<30} expires: {exp}")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")

def cmd_check(domain):
    result = api_request(f"/domain/checkDomain/{domain}")
    if result.get("status") == "SUCCESS":
        if result.get("avail") == "yes":
            print(f"{domain} is AVAILABLE")
            if result.get("pricing"):
                reg = result["pricing"].get("registration", "?")
                print(f"  Registration: ${reg}")
        else:
            print(f"{domain} is NOT available")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")

def cmd_dns_list(domain):
    result = api_request(f"/dns/retrieve/{domain}")
    if result.get("status") == "SUCCESS":
        records = result.get("records", [])
        if not records:
            print("No DNS records found")
            return
        for r in records:
            name = r.get("name", "@")
            rtype = r.get("type", "?")
            content = r.get("content", "")[:50]
            rid = r.get("id", "")
            ttl = r.get("ttl", "")
            print(f"[{rid}] {name:<30} {rtype:<6} {content:<50} TTL:{ttl}")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")

def cmd_dns_add(domain, rtype, content, name=None, ttl=None):
    data = {"type": rtype.upper(), "content": content}
    if name:
        data["name"] = name
    if ttl:
        data["ttl"] = ttl
    result = api_request(f"/dns/create/{domain}", data)
    if result.get("status") == "SUCCESS":
        print(f"Created record ID: {result.get('id', '?')}")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")

def cmd_dns_delete(domain, record_id):
    result = api_request(f"/dns/delete/{domain}/{record_id}")
    if result.get("status") == "SUCCESS":
        print("Record deleted")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")

def cmd_ns_get(domain):
    result = api_request(f"/domain/getNs/{domain}")
    if result.get("status") == "SUCCESS":
        ns = result.get("ns", [])
        for n in ns:
            print(n)
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")

def cmd_ns_set(domain, nameservers):
    result = api_request(f"/domain/updateNs/{domain}", {"ns": nameservers})
    if result.get("status") == "SUCCESS":
        print("Nameservers updated")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")

def cmd_ssl(domain):
    result = api_request(f"/ssl/retrieve/{domain}")
    if result.get("status") == "SUCCESS":
        print("=== Certificate Chain ===")
        print(result.get("certificatechain", ""))
        print("\n=== Private Key ===")
        print(result.get("privatekey", ""))
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")

def cmd_pricing():
    result = api_request("/pricing/get", auth=False)
    if result.get("status") == "SUCCESS":
        pricing = result.get("pricing", {})
        sorted_tlds = sorted(pricing.keys())
        for tld in sorted_tlds[:30]:
            p = pricing[tld]
            reg = p.get("registration", "?")
            renew = p.get("renewal", "?")
            print(f".{tld:<10} reg: ${reg:<8} renew: ${renew}")
        if len(sorted_tlds) > 30:
            print(f"... and {len(sorted_tlds) - 30} more TLDs")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")

def cmd_forward_list(domain):
    result = api_request(f"/domain/getUrlForwarding/{domain}")
    if result.get("status") == "SUCCESS":
        forwards = result.get("forwards", [])
        if not forwards:
            print("No URL forwards found")
            return
        for f in forwards:
            fid = f.get("id", "")
            subdomain = f.get("subdomain", "@") or "@"
            location = f.get("location", "")
            ftype = f.get("type", "")
            print(f"[{fid}] {subdomain:<20} -> {location} ({ftype})")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")

def cmd_forward_add(domain, location, ftype, subdomain=None, includepath=False, wildcard=False):
    data = {
        "location": location,
        "type": ftype,
        "includePath": "yes" if includepath else "no",
        "wildcard": "yes" if wildcard else "no"
    }
    if subdomain:
        data["subdomain"] = subdomain
    result = api_request(f"/domain/addUrlForward/{domain}", data)
    if result.get("status") == "SUCCESS":
        print("URL forward created")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")

def cmd_forward_delete(domain, forward_id):
    result = api_request(f"/domain/deleteUrlForward/{domain}/{forward_id}")
    if result.get("status") == "SUCCESS":
        print("URL forward deleted")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    cmd = args[0]

    if cmd == "ping":
        cmd_ping()
    elif cmd == "domains":
        cmd_domains()
    elif cmd == "check" and len(args) >= 2:
        cmd_check(args[1])
    elif cmd == "dns" and len(args) >= 2:
        subcmd = args[1]
        if subcmd == "list" and len(args) >= 3:
            cmd_dns_list(args[2])
        elif subcmd == "add" and len(args) >= 5:
            name = None
            ttl = None
            for a in args[5:]:
                if a.startswith("--name="):
                    name = a.split("=", 1)[1]
                elif a.startswith("--ttl="):
                    ttl = a.split("=", 1)[1]
            cmd_dns_add(args[2], args[3], args[4], name, ttl)
        elif subcmd == "delete" and len(args) >= 4:
            cmd_dns_delete(args[2], args[3])
        else:
            print("Usage: dns list|add|delete ...")
    elif cmd == "ns" and len(args) >= 2:
        subcmd = args[1]
        if subcmd == "get" and len(args) >= 3:
            cmd_ns_get(args[2])
        elif subcmd == "set" and len(args) >= 5:
            cmd_ns_set(args[2], args[3:])
        else:
            print("Usage: ns get|set ...")
    elif cmd == "forward" and len(args) >= 2:
        subcmd = args[1]
        if subcmd == "list" and len(args) >= 3:
            cmd_forward_list(args[2])
        elif subcmd == "add" and len(args) >= 5:
            subdomain = None
            includepath = False
            wildcard = False
            for a in args[5:]:
                if a.startswith("--subdomain="):
                    subdomain = a.split("=", 1)[1]
                elif a == "--includepath":
                    includepath = True
                elif a == "--wildcard":
                    wildcard = True
            cmd_forward_add(args[2], args[3], args[4], subdomain, includepath, wildcard)
        elif subcmd == "delete" and len(args) >= 4:
            cmd_forward_delete(args[2], args[3])
        else:
            print("Usage: forward list|add|delete ...")
    elif cmd == "ssl" and len(args) >= 2:
        cmd_ssl(args[1])
    elif cmd == "pricing":
        cmd_pricing()
    else:
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
