import datetime
import uuid
import jwt
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import UserInfo
from django.http import HttpResponse
SALT = "3rlnefjwo3ruowfn03u@(&#(h"


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user_obj = UserInfo.objects.filter(username=username, password=password).first()
        if not user_obj:
            return Response({"code": 1000, "error": "用户名密码错误"})
        random_string = str(uuid.uuid4())
        user_obj.token = random_string
        user_obj.save()
        return Response({"code": 1001, "data": random_string})


class OrderView(APIView):

    def get(self, request):
        token = request.query_params.get("token")
        if not token:
            return Response({"code": 2000, "error": "请先登录"})
        user_obj = UserInfo.objects.filter(token=token).first()
        if not user_obj:
            return Response({"code": 2000, "error": "token无效"})
        return Response('订单列表')


class JwtLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user_obj = UserInfo.objects.filter(username=username, password=password).first()
        if not user_obj:
            return Response({"code": 1000, "error": "用户名密码错误"})

        headers = {
            'typ': 'jwt',
            'alg': 'HS256'
        }
        # 构造payload
        payload = {
            'user_id': user_obj.id,  # 自定义用户ID
            'username': user_obj.username,  # 自定义用户名
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1)  # 超时时间
        }
        token = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers).decode('utf-8')
        return Response({"code": 1001, "data": token})


class JwtOrderView(APIView):

    def get(self, request):
        token = request.query_params.get("token")
        verified_payload = None
        msg = None
        try:
            verified_payload = jwt.decode(token, SALT, True)
        except exceptions.ExpiredSignatureError:
            msg = 'token已失效'
        except jwt.DecodeError:
            msg = 'token认证失败'
        except jwt.InvalidTokenError:
            msg = '非法的token'
        if not verified_payload:
            return Response({"code": 20003, "error": msg})
        print(request.query_params.get('aaa'))
        print(type(request.query_params.get('aaa')))
        print(verified_payload['user_id'], verified_payload['username'])
        return Response("订单列表")


from rest_framework_jwt.settings import api_settings


class ProLogin(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user_obj = UserInfo.objects.filter(username=username, password=password).first()
        if not user_obj:
            return Response({"code": 1000, "error": "用户名密码错误"})
        else:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user_obj)
            token = jwt_encode_handler(payload)
            return Response(token)

from rest_framework.authentication import BaseAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

        jwt_value = request.GET.get('token')
        userid = int(request.GET.get('userid',0))
        try:
            payload = jwt_decode_handler(jwt_value)  # 校验
        except jwt.ExpiredSignature:
            msg = '签名已过期'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = '认证失败'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            msg = '认证失败'
            raise exceptions.AuthenticationFailed(msg)
        # print(payload)  # 检验后的第二段数据
        if userid != payload['user_id']:
            msg = '数据伪造'
            raise exceptions.AuthenticationFailed(msg)
        return (jwt_value, userid)


class ProOrder(APIView):

    authentication_classes = [MyAuthentication]
    def post(self, request):
        print(request.auth)
        return Response('ok')