#!/bin/bash
set -e
mkdir -p backend/app frontend/src scraper
[ -f .env ] || cp .env.example .env
echo 'Development environment ready.'
