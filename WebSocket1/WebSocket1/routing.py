from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AuthMiddlewareStack( #此根路由配置指定当与Channels开发服务器建立连接时，ProtocolTypeRouter它将首先检查连接的类型。如果是WebSocket连接（ws：//或wss：//），则该连接将分配给AuthMiddlewareStack。
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})

