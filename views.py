from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import Product, Cart, Order
import stripe
import os

# Configuração da chave secreta Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Adicionar item ao carrinho
@csrf_exempt
@login_required
def add_to_cart(request):
    if request.method == "POST":
        try:
            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('quantity', 1))

            if quantity <= 0:
                raise ValidationError("Quantity must be greater than zero.")

            product = get_object_or_404(Product, id=product_id)

            cart_item, created = Cart.objects.get_or_create(
                user=request.user, product=product,
                defaults={'quantity': quantity}
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return JsonResponse({"message": "Item added to cart."})

        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# Visualizar carrinho
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum([item.product.price * item.quantity for item in cart_items])
    return render(request, 'cart/view.html', {'cart_items': cart_items, 'total_amount': total_amount})

# Remover item do carrinho
@csrf_exempt
@login_required
def remove_from_cart(request, item_id):
    if request.method == "POST":
        try:
            cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
            cart_item.delete()
            return JsonResponse({"message": "Item removed from cart."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# Processar pagamento via Stripe
@csrf_exempt
@login_required
def checkout(request):
    if request.method == "POST":
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if not cart_items:
                raise ValidationError("Your cart is empty.")

            checkout_session = create_stripe_checkout_session(cart_items, request)
            return JsonResponse({"url": checkout_session.url})

        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# Função auxiliar para criar sessão de pagamento no Stripe
def create_stripe_checkout_session(cart_items, request):
    line_items = [{
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': item.product.name,
            },
            'unit_amount': int(item.product.price * 100),  # Preço em centavos
        },
        'quantity': item.quantity,
    } for item in cart_items]

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/checkout/success/'),
        cancel_url=request.build_absolute_uri('/checkout/cancel/'),
    )
    return checkout_session

# Página de sucesso após o pagamento
@login_required
def checkout_success(request):
    # Limpar o carrinho após o pagamento bem-sucedido
    Cart.objects.filter(user=request.user).delete()
    return render(request, 'checkout/success.html')

# Página de cancelamento do pagamento
@login_required
def checkout_cancel(request):
    return render(request, 'checkout/cancel.html')

# Listar produtos
def list_products(request):
    products = Product.objects.all()
    return render(request, 'products/list.html', {'products': products})

# Histórico de pedidos
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/history.html', {'orders': orders})