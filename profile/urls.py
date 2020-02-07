from django.urls import path
from . import views


app_name = 'profile'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='login'),
]
