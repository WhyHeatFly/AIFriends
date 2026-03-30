from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings # 读取Django配置

class RefreshTokenView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return Response({
                    'result': 'refresh token 不存在'
                }, status=401)
            refresh = RefreshToken(refresh_token)  # 会自动检验refresh_token是否过期，如果过期会报异常
            if settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS']:
                refresh.set_jti() # 刷新refresh
                response = Response({
                    'result': 'success',
                    'access': str(refresh.access_token),
                })
                # 将refresh_token设置在cookie
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh),
                    httponly=True,  # 这个 cookie 不能被 JavaScript 读取
                    samesite='Lax',
                    secure=True,
                    max_age=86400 * 7,
                )
                return response
            # 不用刷新refresh，直接返回access
            return Response({
                'result': 'success',
                'access': str(refresh.access_token),
            })
        except:
            return Response({
                'result': 'refresh token 过期了'
            }, status=401)