# Smoke Check

Run the base smoke test after `docker compose up -d --build`:

```bash
./verify/scripts/smoke.sh
```

What it checks:

- static landing page
- path-based app routing
- path-based API routing
- host-based virtual host routing
- basic auth
- cache miss then hit behavior

If one step fails, inspect:

```bash
docker compose ps
docker compose logs nginx app-a app-b api
```
