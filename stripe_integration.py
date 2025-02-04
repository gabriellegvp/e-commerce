import stripe
from django.core.exceptions import ValidationError

stripe.api_key = 'your_stripe_secret_key'

def create_line_items(cart_items):
    """
    Cria os itens da linha para a sessão de checkout.
    """
    line_items = []
    for item in cart_items:
        if item.quantity <= 0:
            raise ValidationError(f"Invalid quantity for product {item.product.name}.")
        if item.product.price <= 0:
            raise ValidationError(f"Invalid price for product {item.product.name}.")

        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.product.name,
                    'description': item.product.description[:500],  # Limita a descrição a 500 caracteres
                },
                'unit_amount': int(item.product.price * 100),  # Preço em centavos
            },
            'quantity': item.quantity,
        })
    return line_items

def create_checkout_session(cart_items, success_url, cancel_url, metadata=None):
    """
    Cria uma sessão de checkout no Stripe.

    :param cart_items: Lista de itens do carrinho.
    :param success_url: URL para redirecionar após o pagamento bem-sucedido.
    :param cancel_url: URL para redirecionar após o cancelamento do pagamento.
    :param metadata: Dicionário de metadados para incluir na sessão.
    :return: Sessão de checkout ou mensagem de erro.
    """
    try:
        # Validação de entrada
        if not cart_items:
            raise ValidationError("The cart is empty.")
        
        # Cria os itens da linha
        line_items = create_line_items(cart_items)

        # Cria a sessão de checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],  # Adicione outros métodos de pagamento, se necessário
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=metadata or {},  # Inclui metadados personalizados
            shipping_address_collection={  # Coleta endereço de entrega
                'allowed_countries': ['US', 'BR', 'CA'],  # Personalize os países permitidos
            },
            automatic_tax={  # Habilita cálculo automático de impostos
                'enabled': True,
            },
        )
        return session
    except stripe.error.StripeError as e:
        # Captura erros específicos do Stripe
        return f"Stripe error: {str(e)}"
    except ValidationError as e:
        # Captura erros de validação
        return f"Validation error: {str(e)}"
    except Exception as e:
        # Captura outros erros inesperados
        return f"Unexpected error: {str(e)}"