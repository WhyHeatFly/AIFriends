import uuid

from django.contrib.auth.models import User # Django 自带的用户表模型 User
from django.db import models # Django 的模型系统
from django.utils.timezone import now, localtime

# instance 是当前模型对象本身 也就是UserProfile
def photo_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4().hex[:10]}.{ext}'
    return f'user/photos/{instance.user_id}_{filename}'

# 这是在 User 表模型的基础上进行扩展
class UserProfile(models.Model): # 定义一张数据库表
    user = models.OneToOneField(User, on_delete=models.CASCADE) # UserProfile 和 User 是 一对一关系。
    # upload_to是用户上传图片放置的位置
    photo = models.ImageField(default='user/photos/default.png', upload_to=photo_upload_to)
    profile = models.TextField(default='谢谢你的关注', max_length=500)
    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField(default=now) # 修改时间

    def __str__(self):
        return f'{self.user.username} - {localtime(self.create_time).strftime('%Y-%m-%d %H:%M:%S')}'

