# Nginx Docker Lab

This repository is a hands-on lab for learning what Nginx is, how it works in real platform and DevOps environments, and how to experiment with the most important features locally on a Mac with Docker Desktop.

The lab uses open source Nginx as the runnable target. It also includes a short comparison to Nginx Plus so you can see where the paid product extends the open source feature set.

## What Nginx Is

Nginx is a high-performance, event-driven server that is usually deployed in front of applications. It can act as:

- a static web server
- a reverse proxy
- an HTTP load balancer
- a TLS termination point
- a lightweight API gateway
- a TCP or UDP proxy through the `stream` subsystem

In most real systems, Nginx is the traffic control layer between clients and upstream services.

## How Nginx Works

At a high level, Nginx uses a master and worker model:

1. The master process reads config, opens sockets, and manages workers.
2. Worker processes accept requests and process them using an event loop instead of one thread per connection.
3. A request is matched against `server` blocks and then `location` blocks.
4. Nginx either serves a local file or proxies the request to an upstream application.
5. On the way through, Nginx can add headers, enforce limits, cache responses, terminate TLS, and log request metadata.

That is the core mental model you should keep in mind while using this lab: Nginx receives traffic, decides where it goes, and shapes the request and response path.

## How Nginx Is Used In Industry

The most common production use cases are:

- fronting web apps and APIs behind a single entry point
- balancing traffic across multiple app instances
- terminating HTTPS so applications do not need to manage certificates themselves
- serving static assets more efficiently than the application layer
- protecting upstreams with buffering, timeouts, auth, and rate limits
- providing a simple edge or gateway tier for containerized services

Nginx still appears in virtual machines, bare metal systems, and traditional monoliths, but it is also common in container platforms, Kubernetes ingress setups, and internal platform stacks.

## What This Lab Covers

This lab is built to let you observe and test these core behaviors locally:

- static file serving
- path-based routing
- host-based virtual hosts
- reverse proxying and forwarded headers
- upstream load balancing and passive failover
- local TLS and HTTP to HTTPS redirects
- rate limiting and connection limiting
- basic authentication
- proxy caching
- WebSocket proxying
- Nginx status and exporter-based observability

It does not try to cover every Nginx module or every production integration. It focuses on the behaviors that matter most when you are learning the product.

## Repository Layout

```text
.
├── README.md
├── compose.yaml
├── compose.tls.yaml
├── compose.observability.yaml
├── docs/
├── nginx/
│   ├── nginx.conf
│   ├── conf.d/
│   ├── snippets/
│   ├── html/
│   ├── tls.conf
│   └── certs/
├── services/
│   ├── backend/
│   └── ws/
└── verify/
```

## Prerequisites

- Docker Desktop on macOS
- `docker compose` available in your shell
- `curl` on the host, or the optional toolbox container

You do not need a local Python runtime for the lab itself. The demo services run inside containers.

## Quick Start

Optional: copy the example environment file if you want to change ports.

```bash
cp .env.example .env
```

The base stack reads `NGINX_HTTP_PORT` and `NGINX_EXPORTER_PORT` directly through Compose. The TLS overlay also uses `NGINX_HTTPS_PORT` for the published HTTPS port, but if you change that value you should update the redirect in `nginx/tls/http-redirect.conf` so HTTP redirects land on the same host port.

Start the base lab:

```bash
docker compose up -d --build
```

Open the landing page:

```bash
open http://localhost:8080
```

Watch Nginx logs:

```bash
docker compose logs -f nginx
```

Run a quick smoke check:

```bash
./verify/scripts/smoke.sh
```

## Base Stack Topology

- `nginx` is the edge proxy and static server.
- `app-a` and `app-b` are identical HTTP backends used for balancing and failover.
- `api` is a richer backend used for headers, delays, cache demonstrations, and auth-protected routes.
- `ws` is an optional WebSocket echo backend enabled through the `ws` profile.

Only Nginx publishes ports to your host. The upstream services stay on the internal Compose network.

## Base Endpoints

Once the lab is running on `http://localhost:8080`, try these endpoints:

- `/` serves the static landing page directly from Nginx.
- `/app/` proxies to the `app_pool` upstream and load balances between `app-a` and `app-b`.
- `/api/headers` shows the forwarded headers Nginx sent to the upstream.
- `/secure/headers` requires basic auth using `student` and `labpass`.
- `/cache/demo` demonstrates proxy caching and returns `X-Cache-Status`.
- `/limited/delay/1` lets you generate rate-limited traffic.
- `/ws/` proxies to the optional WebSocket backend when the `ws` profile is enabled.

## Host-Based Routing

You can test virtual hosts without editing local DNS by sending a `Host` header.

App virtual host:

```bash
curl -sS -H 'Host: app.lab.local' http://localhost:8080/
```

API virtual host:

```bash
curl -sS -H 'Host: api.lab.local' http://localhost:8080/headers
```

This is useful because it isolates the `server_name` matching behavior without requiring `/etc/hosts` changes.

## TLS Overlay

Generate a self-signed certificate:

```bash
docker compose -f compose.yaml -f compose.tls.yaml run --rm certgen
```

Start the stack with HTTPS enabled:

```bash
docker compose -f compose.yaml -f compose.tls.yaml up -d --build
```

Then open:

```bash
open https://localhost:8443
```

The TLS overlay does three things:

- adds HTTPS on host port `8443`
- mounts a certificate-backed `443` server config
- replaces the base no-op redirect snippet so port `80` redirects to HTTPS

Because the certificate is self-signed, your browser will warn until you trust it locally.

## Observability Overlay

Start the observability helpers:

```bash
docker compose -f compose.yaml -f compose.observability.yaml up -d --build
```

This overlay adds:

- `toolbox`, a general-purpose network troubleshooting container
- `nginx-exporter`, which scrapes Nginx stub status and exposes Prometheus metrics on `http://localhost:9113/metrics`

Example status checks:

```bash
docker compose exec toolbox curl -sS http://nginx/nginx_status
curl -sS http://localhost:9113/metrics | head
```

## WebSocket Profile

Enable the optional WebSocket backend:

```bash
docker compose --profile ws up -d --build
```

The `/ws/` route is always defined in Nginx, but it only becomes useful when the `ws` service is running.

## Recommended Learning Order

1. Read [docs/01-basics.md](docs/01-basics.md).
2. Work through [docs/02-routing.md](docs/02-routing.md).
3. Observe balancing behavior in [docs/03-load-balancing.md](docs/03-load-balancing.md).
4. Add HTTPS with [docs/04-tls-http2.md](docs/04-tls-http2.md).
5. Test auth and limits in [docs/05-security-rate-limits.md](docs/05-security-rate-limits.md).
6. Finish with cache, logs, WebSockets, and exporter metrics in [docs/06-cache-logs-websockets.md](docs/06-cache-logs-websockets.md).

## Useful Control Commands

Test the active Nginx config:

```bash
docker compose exec nginx nginx -t
```

Reload the config without restarting the container:

```bash
docker compose exec nginx nginx -s reload
```

Stop one backend to watch passive failover:

```bash
docker compose stop app-b
curl -sS http://localhost:8080/app/
docker compose start app-b
```

## Open Source Nginx vs Nginx Plus

This lab uses open source Nginx because it is fully runnable from public images and covers the core operating model. Nginx Plus keeps the same mental model, but adds features that matter more to runtime operations than first-time learning.

The most relevant differences are:

- active health checks for upstreams
- richer live activity and API-driven control
- additional balancing and session persistence options
- enterprise packaging and commercial support

For learning how routing, proxying, TLS termination, limits, and caching work, open source Nginx is the right place to start.

## Suggested Next Experiments

- edit the balancing method in `nginx/conf.d/10-upstreams.conf`
- change rate limits in `nginx/conf.d/00-zones.conf`
- add a new `server` block for another virtual host
- inspect how `proxy_pass` changes URI behavior when you add or remove trailing slashes
