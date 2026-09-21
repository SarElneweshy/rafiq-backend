from rest_framework.authentication import (
    TokenAuthentication,
    get_authorization_header,
)
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
)


class FeelingTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        # No Authorization header
        if not auth:
            raise NotAuthenticated(
                "You need to sign in to use this feature."
            )

        try:
            return super().authenticate(request)
        except AuthenticationFailed:
            # Invalid or expired token
            raise AuthenticationFailed(
                "You need to sign in to use this feature."
            )

    def authenticate_header(self, request):
        return "Token"