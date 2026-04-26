# 02. Routing

## Goals

- compare path-based routing with host-based routing
- understand how `proxy_pass` and URI rewriting interact
- inspect forwarded headers seen by the upstream

## Path-Based Routing

Base routes:

- `/app/` goes to the app pool
- `/api/` goes to the API backend
- `/secure/` goes to the API backend with basic auth
- `/cache/` goes to the cache demo path on the API backend

Run these requests:

```bash
curl -sS http://localhost:8080/app/
curl -sS http://localhost:8080/api/headers
curl -sS -u student:labpass http://localhost:8080/secure/headers
```

Look for these response fields from the backend:

- `host`
- `x_forwarded_for`
- `x_forwarded_host`
- `x_forwarded_proto`
- `x_forwarded_port`

## Host-Based Routing

Test Nginx `server_name` behavior without touching local DNS.

```bash
curl -sS -H 'Host: app.lab.local' http://localhost:8080/
curl -sS -H 'Host: api.lab.local' http://localhost:8080/headers
```

Why this matters:

- path routing is common when one edge serves several apps behind one hostname
- host routing is common at the outer edge of a platform or multi-tenant service

## Trailing Slash Exercise

In `nginx/conf.d/20-base-server.conf`, change one `proxy_pass` line to remove the trailing slash, then reload Nginx and repeat the request.

This shows one of the most common Nginx learning traps: the presence or absence of a trailing slash changes how the request URI is forwarded upstream.
