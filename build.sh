#!/usr/bin/env bash
# exit on error
set -o errexit

python -m pip install --upgrade pip
pip install -r requirements.txt

python candangoEcommerce/manage.py collectstatic --no-input
python candangoEcommerce/manage.py migrate
