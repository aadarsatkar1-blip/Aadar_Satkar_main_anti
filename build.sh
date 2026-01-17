#!/usr/bin/env bash
set -o errexit

echo "Starting Railway build..."

pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build completed successfully!"
