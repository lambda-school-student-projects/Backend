from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import livestream.routing

application = ProtocolTypeRouter({    # includes index by default
    'websocket': AuthMiddlewareStack(
        URLRouter(
            livestream.routing.websocket_urlpatterns
        )
    )
})
