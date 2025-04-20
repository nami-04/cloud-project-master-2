#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python packages
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --no-cache-dir

# Collect static files and run migrations
python manage.py collectstatic --no-input
python manage.py migrate 