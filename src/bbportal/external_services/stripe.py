import stripe
import os 

stripe.api_version = '2020-08-27'
stripe.api_key = os.environ['STRIPE_SECRET_KEY']
class BBStripe():

  @staticmethod
  def create_customer(email):
    return stripe.Customer.create(email=email)

  @staticmethod
  def delete_customer(stripe_customer_id):
    return stripe.Customer.delete(stripe_customer_id)

  @staticmethod
  def create_customer_portal_session(stripe_customer_id, return_url):
    return stripe.billing_portal.Session.create(
      customer=stripe_customer_id,return_url=return_url)
  
  # https://stripe.com/docs/api/checkout/sessions/create
  @staticmethod
  def create_checkout_session(stripe_customer_id, success_url, cancel_url):
    print(f"success url is {success_url}")
    session = stripe.checkout.Session.create(
      customer = stripe_customer_id,
      line_items=[
        {"price": os.environ["STRIPE_PRICE_monthly_subscription"], "quantity": 1},
        {"price": os.environ["STRIPE_PRICE_usage_subscription"],}
      ],
      mode='subscription',
      success_url= success_url, cancel_url = cancel_url
    )
    print(f"session is {session}")
    return session
  
  # https://stripe.com/docs/api/subscriptions/cancel
  @staticmethod
  def unsubscribe(stripe_customer_id):
    prices = BBStripe.prices()
    stripe.Subscription.delete(stripe_customer_id, prices.monthly_subscription)
    stripe.Subscription.delete(stripe_customer_id, prices.usage_subscription, invoice_now=True)
