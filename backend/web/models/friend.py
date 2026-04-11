from django.db import models
from django.utils.timezone import now, localtime

from web.models.character import Character
from web.models.user import UserProfile


class Friend(models.Model):
    """
    me 指向 UserProfile,也就是“这条好友关系属于哪个用户”
    ForeignKey 表示 多对一关系：一个用户 UserProfile 可以对应很多条 Friend,但每条 Friend 只属于一个 UserProfile
    可以理解成：一个用户可以添加很多个 character 作为好友
    """
    me = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    # 这条关系还关联一个角色 Character
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    memory = models.TextField(default="", max_length=5000, blank=True, null=True)
    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.character.name} - {self.me.user.username} - {localtime(self.create_time).strftime('%Y-%m-%d %H:%M:%S')}"
