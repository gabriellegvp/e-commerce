from django.urls import path, include
from . import views

app_name = 'store'  # Namespace para evitar conflitos de URLs

urlpatterns = [
    # Página inicial
    path('', views.home, name='home'),

    # Produtos
    path('products/', views.list_products, name='list_products'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('products/<slug:slug>/reviews/', views.list_product_reviews, name='list_product_reviews'),
    path('products/<slug:slug>/add-review/', views.add_product_review, name='add_product_review'),

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

    # Descontos
    path('discounts/', views.list_discounts, name='list_discounts'),
    path('discounts/add/', views.add_discount, name='add_discount'),
    path('discounts/remove/<int:discount_id>/', views.remove_discount, name='remove_discount'),

    # Autenticação
    path('accounts/', include('django.contrib.auth.urls')),  # URLs padrão do Django para autenticação
    path('accounts/register/', views.register, name='register'),
    path('accounts/profile/', views.user_profile, name='user_profile'),

    # API Externa (Exemplo: Consulta de frete)
    path('api/shipping/', views.calculate_shipping, name='calculate_shipping'),

    # API Interna (Exemplo: Endpoints para aplicativos móveis)
    path('api/', include([
        path('products/', views.api_list_products, name='api_list_products'),
        path('products/<slug:slug>/', views.api_product_detail, name='api_product_detail'),
        path('cart/', views.api_view_cart, name='api_view_cart'),
        path('cart/add/', views.api_add_to_cart, name='api_add_to_cart'),
    ])),
]