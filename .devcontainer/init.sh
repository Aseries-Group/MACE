#!/bin/bash
set -euo pipefail

mkdir -p backend/app frontend/src scraper/src

if [ ! -f .env ]; then
  cp .env.example .env
fi

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

npm ci

python3 -m playwright install chromium
python3 -m playwright install-deps chromium

echo "Development environment ready."