
from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet,LoginUserViewset

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('login', LoginUserViewset, basename='login')

urlpatterns = [
    path('', include(router.urls)),
]
