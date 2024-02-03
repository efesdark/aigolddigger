from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from . import consumers



websocket_urlpatterns =[
    re_path(r'ws/digger/$', consumers.ChatConsumer.as_asgi()),
]

"""       
application = ProtocolTypeRouter({
    'websocket': URLRouter([
        re_path('ws/digger/$', ChatConsumer.as_asgi()),
    ])
})

""" 
"""
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/test/$', consumers.YourConsumer.as_asgi()),
]

"""