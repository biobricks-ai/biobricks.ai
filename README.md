# BBPortal

The Biobricks portal is made up of:

1. bbportal: user registration and billing management 
2. dvcportal: dvc request logging

## How to run

1. Create new virtual environment `python3 -m venv env`
2. Activate it `source env/bin/activate`
3. Install dependencies `pip install -r requirements.txt`
4. run `./develop.sh bbportal` or `./develop.sh dvcportal`

## How to deploy

```
docker compose build 
aws ecr get-login --no-include-email --region us-east-1
docker push 951523641836.dkr.ecr.us-east-1.amazonaws.com/bbportal:latest
ssh biobricks.ai
screen -r bbportal
# stop the process
docker compose down
docker compose pull
docker compose up 
```