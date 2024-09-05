from django.urls import path, include
from rest_framework import routers
from core.views import UserViewSet, LoginUserView, LogoutUserView, CustomTokenRefreshView

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),

    # jwt required url for refresh i have implemented the login and obtain
    path('token/refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),


]
