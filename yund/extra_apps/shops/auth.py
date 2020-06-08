import jwt
from jwt import exceptions
from rest_framework.authentication import BaseAuthentication
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

class JwtQuertParamsAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get("token",None)
        if not token:
            token = request.data.get('token',None)
        salt = settings.SECRET_KEY
        try:
            result = jwt.decode(token, salt, True)
        except exceptions.ExpiredSignatureError:
            msg = "token失效"
            raise AuthenticationFailed({"code": 1001, "msg": msg})
        except exceptions.DecodeError:
            msg = "token认证失败"
            raise AuthenticationFailed({"code": 1002, "msg": msg})

        except exceptions.InvalidTokenError:
            msg = "非法token"
            raise AuthenticationFailed({"code": 1003, "msg": msg})

        return (result, token)