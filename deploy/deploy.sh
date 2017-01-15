#!/usr/bin/env bash

source deploy.cnf

main_dir="$(dirname $(pwd))"
sdaas_dir="$main_dir/sdaas"

# Set environment variables needed by Django
export STATIC_ROOT="$sdaas_dir/static/"
export DATABASE_CNF="$(pwd)/db.cnf"

echo "Resetting deploy directory"
rm -rf "$deploy_dir"
mkdir "$deploy_dir"
echo "Done"

echo "Copying to deploy directory"
# Copy to production directory
cp -r "$sdaas_dir" "$deploy_dir"
cp db.cnf "$deploy_dir/db.cnf"
echo "Done"

cd "$deploy_dir"

mkdir log
touch log/error.log
touch log/access.log

echo "Setting up virtual environment"
# Setup virtual environment
virtualenv -p python3 sdaasenv
source ./sdaasenv/bin/activate
pip install -r "$main_dir/requirements.txt"
echo "Done"

# Apply database migrations
echo "Applying database migrations"
cd sdaas
./manage.py migrate --settings=sdaas.settings.production
echo "Done"

deactivate

