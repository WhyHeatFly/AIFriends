from django.urls import path, re_path

from web.views.create.character.create import CreateCharacterView
from web.views.create.character.get_list import GetListCharacterView
from web.views.create.character.get_single import GetSingleView
from web.views.create.character.remove import RemoveCharacterView
from web.views.create.character.update import UpdateCharacterViews
from web.views.friend.get_list import GetListFriendView
from web.views.friend.get_or_create import GetOrCreateView
from web.views.friend.remove import RemoveFriendView
from web.views.homepage.index import HomepageIndexView
from web.views.index import index
from web.views.user.account.get_user_info import GetUserInfoView
from web.views.user.account.login import LoginView
from web.views.user.account.logout import LogoutView
from web.views.user.account.refresh_token import RefreshTokenView
from web.views.user.account.register import RegisterView
from web.views.user.profile.update import UpdateProfileView

# 前面补api主要是为了区别前后端路由
# LoginView, LogoutView等等属于类 不能直接调用，因此用as_view()
urlpatterns = [
    path('api/user/account/login/', LoginView.as_view()),
    path('api/user/account/logout/', LogoutView.as_view()),
    path('api/user/account/register/', RegisterView.as_view()),
    path('api/user/account/refresh_token/', RefreshTokenView.as_view()),
    path('api/user/account/get_user_info/', GetUserInfoView.as_view()),
    path('api/user/profile/update/', UpdateProfileView.as_view()),
    path('api/create/character/create/', CreateCharacterView.as_view()),
    path('api/create/character/remove/', RemoveCharacterView.as_view()),
    path('api/create/character/update/', UpdateCharacterViews.as_view()),
    path('api/create/character/get_single/', GetSingleView.as_view()),
    path('api/create/character/get_list/', GetListCharacterView.as_view()),
    path('api/homepage/index/', HomepageIndexView.as_view()),
    path('api/friend/get_or_create/', GetOrCreateView.as_view()),
    path('api/friend/get_list/', GetListFriendView.as_view()),
    path('api/friend/remove/', RemoveFriendView.as_view()),
    path('', index),

    # 兜底路由
    re_path(r'^(?!media/|static/|assets/).*$', index), # 在前端任意路径下刷新时，django都自动路由到根路径下，剩下的路由交由前端处理。
]