#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Crear directorio staticfiles si no existe
mkdir -p staticfiles

python manage.py collectstatic --no-input
python manage.py migrate