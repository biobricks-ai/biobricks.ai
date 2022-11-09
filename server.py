#! /usr/bin/env python3.6

import stripe
import json
import os

from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv, find_dotenv

# Setup Stripe python client library
load_dotenv(find_dotenv())

# For sample support and debugging, not required for production:
stripe.set_app_info('stripe-samples/subscription-use-cases/usage-based-subscriptions',
    version='0.0.1',
    url='https://github.com/stripe-samples/subscription-use-cases/usage-based-subscriptions')

stripe.api_version = '2020-08-27'
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

static_dir = str(os.path.abspath(os.path.join(__file__, "..", os.getenv("STATIC_DIR"))))
app = Flask(__name__, static_folder=static_dir, static_url_path="", template_folder=static_dir)


@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html')




if __name__ == '__main__':
    app.run(port=4242)
