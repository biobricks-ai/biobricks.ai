# BBPortal

The Biobricks portal is made up of:

1. bbportal: user registration and billing management 
2. dvcportal: dvc request logging

## How to run

1. Create new virtual environment `python3 -m venv env`
2. Activate it `source env/bin/activate`
3. Install dependencies `pip install -r requirements.txt`
4. Add environment variables `source env_test.env`
5. Run the application `python src/main.py bbportal`
6. Go to `localhost:5000` in your browser to see the demo

### Docker compose

```
docker compose up
```
