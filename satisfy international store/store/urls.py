from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, LoginUserViewSet, LogoutUserViewSet
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('login', LoginUserViewSet, basename='login_user')
router.register('logout', LogoutUserViewSet, basename='logout_user')

urlpatterns = [
    path('', include(router.urls)),

    # jwt required url for refresh i have implemented the login and obtain
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),


]
