# myapp/urls.py
from django.urls import path
from .views import home, get_bitcoin_price


urlpatterns = [
    path('', home, name='home'),
    path('get_bitcoin_price/', get_bitcoin_price, name='get_bitcoin_price'),
]
