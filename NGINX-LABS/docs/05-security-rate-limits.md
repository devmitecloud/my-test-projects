# 05. Security Controls And Rate Limits

## Goals

- observe basic auth in front of an upstream
- inspect security headers added by Nginx
- trigger rate limits and connection limits

## Basic Auth

Unauthenticated:

```bash
curl -i http://localhost:8080/secure/headers
```

Authenticated:

```bash
curl -i -u student:labpass http://localhost:8080/secure/headers
```

## Security Headers

```bash
curl -I http://localhost:8080/
```

Look for:

- `X-Content-Type-Options`
- `X-Frame-Options`
- `Referrer-Policy`
- `Content-Security-Policy`

## Rate Limiting

Run a short burst:

```bash
seq 1 15 | xargs -I{} -n1 -P8 curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/limited/delay/1
```

You should see a mix of success and throttled responses once the limit is exceeded.

## Where The Controls Live

- zones are defined in `nginx/conf.d/00-zones.conf`
- route-level enforcement happens in `nginx/conf.d/20-base-server.conf`
- auth uses `nginx/.htpasswd`
