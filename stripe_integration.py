import stripe

stripe.api_key = 'your_stripe_secret_key'

def create_checkout_session(cart_items):
    try:
        # Calcular o total
        total_amount = sum([item.product.price * item.quantity for item in cart_items])
        
        # Criar a sessão de checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                    'unit_amount': int(item.product.price * 100),  # Preço em centavos
                },
                'quantity': item.quantity,
            } for item in cart_items],
            mode='payment',
            success_url="your_success_url",
            cancel_url="your_cancel_url",
        )
        return session
    except Exception as e:
        return str(e)
