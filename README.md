# BBPortal

The Biobricks portal is made up of:

1. bbportal: user registration and billing management 
2. dvcportal: dvc request logging

## How to develop

1. Create new virtual environment `python3 -m venv env`
2. Activate it `source env/bin/activate`
3. Install dependencies `pip install -r requirements.txt`
4. run `./develop.sh bbportal` or `./develop.sh dvcportal`

## How to deploy

```
docker compose build 
aws ecr get-login --no-include-email --region us-east-1 --profile <your_insilica_profile> | docker login --username AWS --password-stdin 951523641836.dkr.ecr.us-east-1.amazonaws.com
docker push 951523641836.dkr.ecr.us-east-1.amazonaws.com/bbportal:latest
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