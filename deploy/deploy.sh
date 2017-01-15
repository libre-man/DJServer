#!/usr/bin/env bash

source deploy.cnf

sdaas_dir="$(dirname $(pwd))/sdaas"

# Set environment variables needed by Django
export STATIC_ROOT="$sdaas_dir/static/"
export DATABASE_CNF="$(pwd)/db.cnf"

# Apply database migrations
./$sdaas_dir/manage.py migrate --settings=sdaas.settings.production

rm -rf "$deploy_dir"
mkdir "$deploy_dir"

# Copy to production directory
cp -r "$sdaas_dir" "$deploy_dir"

cd "$deploy_dir"

# Setup virtual environment
virtualenv sdaasenv
source ./env/bin/activate
pip install -r ../requirements.txt
deactivate
