# myapp/urls.py
from django.urls import path
from .views import home, get_bitcoin_price, chart, charts,test,candles,update_chart,your_view_name,test_message,ajax,ajax_message


urlpatterns = [
    path('', home, name='home'),
    path('get_bitcoin_price/', get_bitcoin_price, name='get_bitcoin_price'),
    path('ajax/', ajax, name='ajax'),
    path('chart/', chart, name='chart'),
    path('charts/', charts, name='charts'),
    path('test/', test, name='test'),
    path('candles/', candles, name='candles'),
    path('update_chart/', update_chart, name='update_chart'),
    path('your_view_name/', your_view_name, name='your_view_name'),
    path("ajax-message/", ajax_message, name="ajax_message"),
    path("test-message/", test_message, name="test_message"),
]

