#!/usr/bin/env bash
# build.sh

echo "Building the project..."

# Install dependencies
pip install -r requirements.txt

# Install whitenoise for static files
pip install whitenoise

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate