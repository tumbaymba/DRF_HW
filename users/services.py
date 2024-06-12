import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY

def create_stripe_product(product):
    stripe_product = stripe.Product.create(name=product)
    return stripe_product['id']

def create_stripe_price(price, product):
    stripe_price = stripe.Price.create(
        currency="rub",
        unit_amount=price*100,
        product=product,
    )
    return stripe_price['id']
def create_stripe_session(stripe_price_id):
    stripe_session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{
            "price": stripe_price_id,
            "quantity": 1}],
        mode="payment",
    )
    return stripe_session['url'], stripe_session['id']