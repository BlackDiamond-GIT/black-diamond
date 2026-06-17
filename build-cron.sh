#!/usr/bin/env bash
# Cron jobs only need dependencies — no collectstatic/migrate/seed at build time.
set -o errexit

python3 -m pip install -r requirements.txt
