from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

class TokenAuthMiddleware:
    """
    Middleware для ASGI 3 (Channels 4+)
    Проверяет Authorization: Token <key> в заголовках
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        scope["user"] = await self.get_user(scope)
        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user(self, scope):
        headers = dict((k.decode().lower(), v.decode()) for k, v in scope.get("headers", []))
        auth_header = headers.get("authorization")
        if auth_header and auth_header.startswith("Token "):
            token_key = auth_header.split(" ")[1]
            try:
                token = Token.objects.get(key=token_key)
                return token.user
            except Token.DoesNotExist:
                return AnonymousUser()
        return AnonymousUser()


# Обёртка для использования с AuthMiddlewareStack
def TokenAuthMiddlewareStack(inner):
    from channels.auth import AuthMiddlewareStack
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))
