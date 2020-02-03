from django.urls import path
from . import views


app_name = 'product'

urlpatterns = [
    # item list
    path('', views.ItemListView.as_view(), name='list'),

    # item detail
    path('product/<slug>/', views.ItemDetailView.as_view(), name='detail'),

    # add item to cart
    path('add-to-cart/<slug>/', views.add_to_cart, name='add_to_cart'),
]