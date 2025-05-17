import stripe
import os

class PaymentProcessor:
    def __init__(self):
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

    def create_checkout_session(self, user_email, amount, product_name):
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product_name,
                        },
                        'unit_amount': int(amount * 100),  # cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                customer_email=user_email,
                success_url="https://your-domain.com/success",
                cancel_url="https://your-domain.com/cancel",
            )
            return session.url
        except Exception as e:
            print(f"Stripe error: {e}")
            return None
