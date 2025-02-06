import stripe
import logging
from django.core.exceptions import ValidationError

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

stripe.api_key = 'your_stripe_secret_key'  # Substitua pela sua chave secreta do Stripe

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
        if not item.product.is_active:
            raise ValidationError(f"Product {item.product.name} is not active.")
        if item.quantity > item.product.stock:
            raise ValidationError(f"Not enough stock for product {item.product.name}.")

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

def create_checkout_session(cart_items, success_url, cancel_url, metadata=None, customer_email=None):
    """
    Cria uma sessão de checkout no Stripe.

    :param cart_items: Lista de itens do carrinho.
    :param success_url: URL para redirecionar após o pagamento bem-sucedido.
    :param cancel_url: URL para redirecionar após o cancelamento do pagamento.
    :param metadata: Dicionário de metadados para incluir na sessão.
    :param customer_email: E-mail do cliente para pré-preenchimento no Stripe.
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
            payment_method_types=['card', 'ideal', 'alipay'],  # Adicione outros métodos de pagamento, se necessário
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
            customer_email=customer_email,  # Pré-preenche o e-mail do cliente
        )
        logger.info(f"Checkout session created: {session.id}")
        return session
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {str(e)}")
        return f"Stripe error: {str(e)}"
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        return f"Validation error: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return f"Unexpected error: {str(e)}"

def apply_discount_to_line_items(line_items, discount_code):
    """
    Aplica um desconto aos itens da linha, se o código de desconto for válido.
    """
    # Aqui você pode adicionar a lógica para validar e aplicar descontos
    # Exemplo: Verificar o código de desconto no banco de dados e aplicar o desconto
    pass

def update_stock_after_payment(cart_items):
    """
    Atualiza o estoque dos produtos após o pagamento bem-sucedido.
    """
    for item in cart_items:
        item.product.update_stock(item.quantity)
        logger.info(f"Stock updated for product {item.product.name}: {item.product.stock} remaining")