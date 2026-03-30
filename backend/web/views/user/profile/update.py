from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models.user import UserProfile
from web.views.utils.photo import remove_old_photo


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            username = request.data.get('username').strip()
            profile = request.data.get('profile').strip()[:500]
            # 头像是文件 在 FILES 获取, 且头像文件大小较大，若不更新头像则不往后传
            photo = request.FILES.get('photo', None)

            if not username:
                return Response({
                    'result': '用户名不能为空'
                })
            if not profile:
                return Response({
                    'result': '简介不能为空'
                })
            if username != user.username and User.objects.filter(username=username).exists():
                return Response({
                    'result': '用户名已存在'
                })
            # 有修改头像
            if photo:
                remove_old_photo(user_profile.photo)
                user_profile.photo = photo

            user_profile.profile = profile
            user_profile.update_time = now()
            user_profile.save()
            # 用户名是在Django自带的后端里
            user.username = username
            user.save()
            return Response({
                'result': 'success',
                'user_id': user.id,
                'username': user.username,
                'profile': user_profile.profile,
                'photo': user_profile.photo.url,
            })
        except:
            return Response({
                'result': '更新信息失败，请稍后再试'
            })
