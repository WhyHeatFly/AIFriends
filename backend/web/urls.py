from django.urls import path
from web.views.index import index
from web.views.user.account.login import LoginView
from web.views.user.account.logout import LogoutView
from web.views.user.account.refresh_token import RefreshTokenView
from web.views.user.account.register import RegisterView

# 前面补api主要是为了区别前后端路由
# LoginView, LogoutView等等属于类 不能直接调用，因此用as_view()
urlpatterns = [
    path('api/user/account/login/', LoginView.as_view()),
    path('api/user/account/logout/', LogoutView.as_view()),
    path('api/user/account/register/', RegisterView.as_view()),
    path('api/user/account/refresh_token/', RefreshTokenView.as_view()),
    path('', index),
]