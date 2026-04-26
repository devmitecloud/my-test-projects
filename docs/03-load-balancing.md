# 03. Load Balancing And Failover

## Goals

- watch Nginx distribute requests across multiple upstream servers
- see passive failover when one backend is unavailable
- connect upstream behavior to the `upstream` block in the config

## Files To Look At

- `nginx/conf.d/10-upstreams.conf`
- `nginx/conf.d/20-base-server.conf`

## Round Trips Through The App Pool

Repeat the same request several times:

```bash
for _ in 1 2 3 4 5; do curl -sS http://localhost:8080/app/; echo; done
```

Look for the `service` field toggling between `app-a` and `app-b`.

The upstream currently uses `least_conn`. Try changing it to plain round robin by removing that directive and reloading Nginx.

## Passive Failover

Stop one backend:

```bash
docker compose stop app-b
for _ in 1 2 3; do curl -sS http://localhost:8080/app/; echo; done
docker compose start app-b
```

What to observe:

- Nginx keeps sending traffic to the remaining healthy upstream.
- No active health check runs in the open source build.
- Failover here is passive: Nginx learns from connection or response failures.

## Industry Note

This is enough to understand the basic balancing layer that commonly fronts app replicas. More advanced runtime health control is one of the places where Nginx Plus differs.
