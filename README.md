# BBPortal

The Biobricks portal is made up of two servers:

| service | type | description |
|---:|---|
| bbportal | server | user registration and billing management |
| dvcportal | server | dvc request logging |
| biobricks-r | R client | install and pull biobricks to a library |

## How to run

1. Create new virtual environment `python3 -m venv env`
2. Activate it `source env/bin/activate`
3. Install dependencies `pip install -r requirements.txt`
4. Run the application `python src/main.py bbportal`
5. Go to `localhost:5000` in your browser to see the demo

### Docker compose

```
docker compose up
```

# TODO

## x create an account

1. x adds customer to stripe
2. x adds customer to local sqlite db
3. x links local and stripe customer ids
4. x verification link
5. x forgot password
6. x delete account (run User.delete_user(`<email>`))

## x create subscription w/ stripe customer portal

1. x create stripe subscription
2. x link subscription id to local user
3. x create an api-token
4. x delete subscription

## O aws integration

BB dvc repos should use http remote see https://dvc.org/doc/command-reference/remote/modify

1. o redirect dvc pull requests to s3
2. o record bandwidth usage of dvc pull requests
   1. o record requested object
   2. o get object size from aws at time of request
   3. o associate size with requesting token
3. o update biobricks-r to require tokens
4. o update biobricks-py to require tokens

## O Customer Billing Reports

generate customer facing usage and billing reports


# ssl

1. managed with certbot at /var/www /members.biobricks.ai and /dvc.biobricks.ai
