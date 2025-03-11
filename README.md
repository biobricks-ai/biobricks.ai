# BBPortal

The Biobricks portal is made up of:

1. bbportal: user registration and billing management 
2. dvcportal: dvc request logging

## How to develop

1. Create new virtual environment `python3 -m venv env`
2. Activate it `source env/bin/activate`
3. Install dependencies `pip install -r requirements.txt`
4. Set up environment variables `source set-env.sh`
5. run `./develop.sh bbportal` or `./develop.sh dvcportal`

## How to deploy

```
docker compose build 
aws ecr get-login-password --region us-east-1 --profile iam_tom | docker login --username AWS --password -stdin 951523641836.dkr.ecr.us-east-1.amazonaws.com
COMMIT=$(git rev-parse HEAD)
# update the image tag in docker-compose.yml
sed -i "s/bbportal:<commit>/bbportal:$COMMIT/g" docker-compose.yml
docker compose build
docker push 951523641836.dkr.ecr.us-east-1.amazonaws.com/bbportal:$COMMIT

# change the image tag back to latest reference
sed -i "s/bbportal:$COMMIT/bbportal:latest/g" docker-compose.yml
docker compose build
docker push 951523641836.dkr.ecr.us-east-1.amazonaws.com/bbportal:latest

# login and start the new process
ssh biobricks.ai
screen -r bbportal
# stop the process
docker compose down
docker compose pull
docker compose up 
```

You also need to set up nginx:
1. add the nginx/biobricks.ai.conf file to the nginx config directory.
2. rename the server_name as necessary
3. install certbot, the certbot nginx plugin, and run `certbot install --cert-name <server_name>`