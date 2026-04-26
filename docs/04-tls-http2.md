# 04. TLS And HTTP/2

## Goals

- terminate HTTPS at Nginx
- inspect the redirect from HTTP to HTTPS
- understand why TLS is usually handled at the edge

## Generate A Local Certificate

```bash
docker compose -f compose.yaml -f compose.tls.yaml run --rm certgen
```

## Start The TLS Stack

```bash
docker compose -f compose.yaml -f compose.tls.yaml up -d --build
```

## Verify

```bash
curl -k -I https://localhost:8443/
curl -I http://localhost:8080/
```

What to observe:

- port `80` redirects to `https://localhost:8443`
- port `8443` serves the same app through the TLS-enabled server block
- Nginx terminates TLS and then proxies clear HTTP to the upstream containers

## HTTP/2 Check

If your local curl supports it:

```bash
curl -k --http2 -I https://localhost:8443/
```

## Why Industry Uses This Pattern

Putting TLS at Nginx centralizes certificate handling, cipher policy, redirects, and security headers so upstream apps stay simpler.
