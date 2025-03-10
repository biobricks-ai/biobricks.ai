#!/bin/bash

# configure the biobricks.ai profile, ask an admin for the start-url and sso-region
# aws configure sso --profile biobricks.ai
# export AWS_PROFILE=biobricks.ai
aws sso login --profile biobricks.ai
export AWS_PROFILE=biobricks.ai

# Get the secret and set as environment variables
SECRET=$(aws secretsmanager get-secret-value \
    --secret-id "github.com/biobricks/biobricks.ai" \
    --region "us-east-1" \
    --query 'SecretString' \
    --output text)

# Export each key-value pair as an environment variable
eval "$(echo $SECRET | jq -r 'to_entries | .[] | "export \(.key)=\(.value)"')"

# Verify the variables were set
echo "Environment variables set. Testing a few:"
echo "BBPORTAL_FLASK_SERVER_NAME: $BBPORTAL_FLASK_SERVER_NAME"
echo "SQLITE_PATH: $SQLITE_PATH"