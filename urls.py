from django.urls import path, include
from . import views

app_name = 'store'  # Namespace para evitar conflitos de URLs

urlpatterns = [
    # Página inicial
    path('', views.home, name='home'),

    # Produtos
    path('products/', views.list_products, name='list_products'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),

    # Carrinho
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/<str:session_id>/', views.checkout_success, name='checkout_success'),
    path('checkout/cancel/', views.checkout_cancel, name='checkout_cancel'),

    # Pedidos
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),

    # Autenticação
    path('accounts/', include('django.contrib.auth.urls')),  # URLs padrão do Django para autenticação
    path('accounts/register/', views.register, name='register'),
    path('accounts/profile/', views.user_profile, name='user_profile'),
]