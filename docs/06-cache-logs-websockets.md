# 06. Cache, Logs, WebSockets, And Observability

## Goals

- see proxy cache hit and miss behavior
- inspect structured logs from Nginx
- enable the optional WebSocket backend
- scrape Nginx status with the exporter overlay

## Cache Demo

First request:

```bash
curl -sS -D - http://localhost:8080/cache/demo -o /dev/null
```

Second request:

```bash
curl -sS -D - http://localhost:8080/cache/demo -o /dev/null
```

Look at the `X-Cache-Status` header. The first request should be a miss and the second should usually be a hit.

## Logs

```bash
docker compose logs -f nginx
```

Look for:

- `request_time`
- `upstream_addr`
- `upstream_status`
- `upstream_response_time`
- `cache_status`

These fields matter because they tell you what the edge saw, what upstream handled the request, and whether cache or upstream latency affected the response.

## WebSockets

Start the stack with the WebSocket profile:

```bash
docker compose --profile ws up -d --build
```

The lab includes an echo WebSocket backend behind `/ws/`. Use a browser client, a local tool such as `wscat`, or a helper container if you install one in the toolbox.

## Observability Overlay

```bash
docker compose -f compose.yaml -f compose.observability.yaml up -d --build
docker compose exec toolbox curl -sS http://nginx/nginx_status
curl -sS http://localhost:9113/metrics | head
```

This shows the difference between:

- the native Nginx stub status endpoint
- a metrics exporter that converts that data into a Prometheus-friendly format
