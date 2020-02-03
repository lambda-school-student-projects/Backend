from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import battleroyale.routing


application = ProtocolTypeRouter({
    # includes index by default
    'websocket': AuthMiddlewareStack(
        URLRouter(
            battleroyale.routing.websocket_urlpatterns
        )
    )
})