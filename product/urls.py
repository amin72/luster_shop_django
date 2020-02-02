from django.urls import path
from . import views


app_name = 'product'

urlpatterns = [
    # item list
    path('', views.ItemListView.as_view(), name='list'),

    # item detail
    path('product/<slug>/', views.ItemDetailView.as_view(), name='detail'),
]