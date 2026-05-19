#!/bin/sh

set -eu

base_url="${1:-http://localhost:${NGINX_HTTP_PORT:-8080}}"

echo "Checking landing page"
curl -fsS "$base_url/" >/dev/null

echo "Checking path-based app routing"
curl -fsS "$base_url/app/" | grep -E '"service": "app-a"|"service": "app-b"' >/dev/null

echo "Checking path-based API routing"
curl -fsS "$base_url/api/headers" | grep '"service": "api"' >/dev/null

echo "Checking host-based app routing"
curl -fsS -H 'Host: app.lab.local' "$base_url/" | grep -E '"service": "app-a"|"service": "app-b"' >/dev/null

echo "Checking basic auth"
curl -fsS -u student:labpass "$base_url/secure/headers" | grep '"service": "api"' >/dev/null

echo "Checking cache miss then hit"
first_cache_status=$(curl -sS -D - "$base_url/cache/demo" -o /dev/null | tr -d '\r' | awk '/^X-Cache-Status:/ {print $2}')
second_cache_status=$(curl -sS -D - "$base_url/cache/demo" -o /dev/null | tr -d '\r' | awk '/^X-Cache-Status:/ {print $2}')

if [ "$first_cache_status" != "MISS" ]; then
    echo "Expected first cache status to be MISS, got: $first_cache_status"
    exit 1
fi

if [ "$second_cache_status" != "HIT" ]; then
    echo "Expected second cache status to be HIT, got: $second_cache_status"
    exit 1
fi

echo "Smoke check passed"
