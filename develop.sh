#!/bin/bash
# run with ./develop.sh bbportal or ./develop.sh dvcportal

# Set Flask to run in development environment
export FLASK_ENV=development

# Add environmental variables from env_test.env
export $(echo $(cat env_test.env | sed 's/#.*//g'| xargs) | envsubst)

# Start the Flask application
python3 src/main.py $1
