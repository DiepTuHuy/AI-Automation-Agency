import os
import stripe
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_mock")

def create_checkout_session(customer_email: str):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=customer_email,
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Gói AI SaaS Premium (Tháng)',
                        'description': 'Sử dụng không giới hạn các AI Agents thông minh.',
                    },
                    'unit_amount': 2900, # $29.00 USD (đơn vị cent)
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://example.com/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://example.com/cancel',
        )
        return session.url
    except Exception as e:
        print(f"Lỗi tạo phiên thanh toán: {e}")
        return None

if __name__ == "__main__":
    url = create_checkout_session("customer@example.com")
    if url:
        print(f"Đường link thanh toán Stripe Checkout: {url}")