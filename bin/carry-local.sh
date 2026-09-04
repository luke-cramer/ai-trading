#!/bin/bash
# Laptop backup writer: ingest once, commit, push. Safe alongside the GitHub Actions job (rows dedupe on timestamp).
set -euo pipefail
cd "$(dirname "$0")/.."
[ -f .env ] && set -a && . ./.env && set +a
exec >> reports/carry-local.log 2>&1
echo "== $(date -u +%Y-%m-%dT%H:%M:%SZ)"
.venv/bin/python -m strategies.carry ingest
.venv/bin/python -m strategies.carry check-stale || true
git add data/
if ! git diff --cached --quiet; then
  git commit -q -m "data(carry): ingest $(date -u +%Y-%m-%dT%H:%MZ) (laptop)"
  for i in 1 2 3; do
    git pull --rebase --autostash -q origin main && git push -q origin HEAD:main && exit 0
    sleep $((i * 5))
  done
  exit 1
fi
