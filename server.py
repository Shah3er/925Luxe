import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


app = Flask(__name__)
CORS(app)

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.json

    # Logging the incoming request data for debugging
    print('Received request data:', data)

    # Handle multiple line items or fallback to single price_id
    line_items = data.get('line_items')
    print('Line items:', line_items)  # Log the parsed line items

    if not line_items:
        price_id = data.get('price_id')
        print('Single price_id fallback:', price_id)  # Log single price_id fallback
        if not price_id:
            return jsonify(error="No price_id or line_items provided"), 400
        line_items = [{'price': price_id, 'quantity': 1}]

    try:
        checkout_session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=line_items,
    mode='payment',
    customer_email=data.get('email'),  # Optional: passed from client
    shipping_address_collection={
        'allowed_countries': ['CA', 'US']
    },
            shipping_options=[{
                'shipping_rate_data': {
                    'type': 'fixed_amount',
                    'fixed_amount': {
                        'amount': 2000,
                        'currency': 'cad',
                    },
                    'display_name': 'Standard Shipping (2-3 Weeks)',
                    'delivery_estimate': {
                        'minimum': {'unit': 'week', 'value': 2},
                        'maximum': {'unit': 'week', 'value': 3},
                    },
                },
            }],
            success_url='https://925luxe.ca/success.html',
            cancel_url='https://925luxe.ca/cancel.html',
        )
        return jsonify({'url': checkout_session.url})
    except Exception as e:
        print('Stripe API Error:', str(e))  # Log any Stripe errors
        return jsonify(error=str(e)), 403

if __name__ == '__main__':
    app.run(port=4242)
