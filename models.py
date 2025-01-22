from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Cart
import stripe
import os

# Configuração da chave secreta Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Adicionar item ao carrinho
@csrf_exempt
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        product = Product.objects.get(id=product_id)

        cart_item, created = Cart.objects.get_or_create(
            user=request.user, product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return JsonResponse({"message": "Item added to cart."})

# Processar pagamento via Stripe
@csrf_exempt
def checkout(request):
    if request.method == "POST":
        try:
            # Definir o preço total baseado no carrinho
            cart_items = Cart.objects.filter(user=request.user)
            total_amount = sum([item.product.price * item.quantity for item in cart_items])

            # Criar uma sessão de pagamento no Stripe
            checkout_session = stripe.checkout.Session.create(
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
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
            )

            return JsonResponse({"url": checkout_session.url})

        except Exception as e:
            return JsonResponse({"error": str(e)})

# Listar produtos
def list_products(request):
    products = Product.objects.all()
    return render(request, 'products/list.html', {'products': products})
