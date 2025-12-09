#!/bin/bash
sudo service postgresql start
# Check if user exists, if not create
sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='taskpilot'" | grep -q 1 || sudo -u postgres psql -c "CREATE USER taskpilot WITH PASSWORD 'taskpilot_password';"
# Check if db exists, if not create
sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='taskpilot'" | grep -q 1 || sudo -u postgres psql -c "CREATE DATABASE taskpilot OWNER taskpilot;"
