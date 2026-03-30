from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# 退出登录：删除 refresh_token，只是让浏览器以后不能继续刷新 access_token。
class LogoutView(APIView):
    permission_classes = [IsAuthenticated] # 强制用户必须处于登录状态才能访问, 若没有登录，返回401
    def post(self, request):
        response = Response({
            'result': 'success'
        })
        response.delete_cookie('refresh_token')
        return response
