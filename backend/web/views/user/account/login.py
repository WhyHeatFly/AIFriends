from django.contrib.auth import authenticate
from rest_framework.views import APIView # DRF（Django REST framework）里的类视图基类
from rest_framework.response import Response # DRF 用来返回接口数据的响应对象。
from rest_framework_simplejwt.tokens import RefreshToken

from web.models.user import UserProfile


class LoginView(APIView):
    def post(self, request, *args, **kwargs): # request是前端请求对象
        try:
            username = request.data['username'].strip()
            password = request.data['password'].strip()
            if not username or not password:
                return Response({
                    'result': '用户名和密码不能为空'
                })
            # Django自带的验证用户名和密码是否匹配，默认情况下，这个认证后端会去查 Django 的用户表
            # 验证成功 返回 user对象，验证失败返回 None
            user = authenticate(username=username, password=password)

            if user: # 用户名和密码正确
                user_profile = UserProfile.objects.get(user=user) # 取出用户信息
                refresh = RefreshToken.for_user(user) # 生成jwt
                # 构造Response返回给前端
                response = Response({
                    'result': 'success',
                    'access': str(refresh.access_token),
                    'user_id': user.id,
                    'username': user.username,
                    'photo': user_profile.photo.url,
                    'profile': user_profile.profile,
                })
                # 将refresh_token设置在cookie
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True, # 这个 cookie 不能被 JavaScript 读取
                    samesite='Lax',
                    secure=True,
                    max_age=86400 * 7,
                )
                return response
            # 不正确
            else:
                return Response({
                    'result': '用户名或密码错误'
                })
        except:
            return Response({
                'result': '登录异常，请稍后重试'
            })