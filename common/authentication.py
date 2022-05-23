import datetime
import jwt
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from app import settings
from core.models import User


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        is_manager = 'api/manager' in request.path
        token = request.COOKIES.get('jwt')

        if not token:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])  # get payload
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Unauthenticated')

        if (is_manager and payload['scope'] != 'manager') or (not is_manager and payload['scope'] != 'admin'): # later add simple user type
            raise exceptions.AuthenticationFailed('Invalid Scope!')

        user = User.objects.get(pk=payload['user_id'])

        if user is None:
            raise exceptions.AuthenticationFailed('User not found!')

        return user, None  # for error

    @staticmethod  # no need to declare a class
    def generate_jwt(id, scope):
        payload = {
            'user_id': id,
            'scope': scope,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')  # USE 'HS256' ALGORITHM
