from django.urls import path
from . import views

urlpatterns = [
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('products/', views.list_products, name='list_products'),
]
