#!/usr/bin/env bash
set -o errexit

export DJANGO_SETTINGS_MODULE=config.settings.prod

python3 -m pip install -r requirements.txt
python3 scripts/compile_admin_uk_locale.py
python3 scripts/compile_public_locales.py
python3 scripts/download_images.py
python3 manage.py collectstatic --no-input
python3 manage.py migrate --no-input
python3 manage.py seed_site
