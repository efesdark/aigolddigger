# myapp/urls.py
from django.urls import path
from .views import home
from .views import bitcoin_chart_view

urlpatterns = [
    path('', home, name='home'),
    path('bitcoin-chart-view/', bitcoin_chart_view, name='bitcoin_chart_view'),
    path('charts/bitcoin-chart/', bitcoin_chart_view, name='bitcoin_chart'),
]
