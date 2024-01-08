import re

import jwt
from django.apps import apps as django_apps
from django.conf import settings
from django.http import HttpRequest
from rest_framework import authentication, exceptions


class JWTAuthentication(authentication.BaseAuthentication):
    regex_bearer = re.compile(r"^[Bb]earer (.*)$")

    def __init__(self, *args, **kwargs):
        self.jwks_client = jwt.PyJWKClient(
            settings.USER_SERVICE_JWKS_URL, cache_keys=True
        )

    def authenticate(self, request: HttpRequest):
        auth_header = request.headers.get("authorization")
        if not auth_header:
            raise exceptions.AuthenticationFailed(
                "Authorization header is not present."
            )
        # Extract raw JWT
        match = self.regex_bearer.match(auth_header)
        if not match:
            raise exceptions.AuthenticationFailed(
                "Authorization header must be of the"
                "following format: 'Bearer <jwt_token>'"
            )

        raw_jwt = match.groups()[-1]
        # Extract key ID
        try:
            sig_key = self.jwks_client.get_signing_key_from_jwt(raw_jwt)
            data = jwt.decode(raw_jwt, sig_key.key, algorithms=["RS256"])
        except (jwt.DecodeError, jwt.PyJWKClientError, jwt.InvalidTokenError) as e:
            raise exceptions.AuthenticationFailed("Bearer token is invalid.") from e

        UserModel = django_apps.get_model("users.BlogUser", require_ready=False)
        user = UserModel.objects.filter(pk=data["sub"])
        if not user.exists():
            raise exceptions.AuthenticationFailed(
                "No user associated with this token was found."
            )

        return user.get(), data
