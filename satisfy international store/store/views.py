from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation

from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from store.serializers import UserSerializer,LoginUserSerailzer
from store.permissions import IsAuthenticatedOrReadOnly
from store.schema import user_creation_doc

from utils.reusable_func import get_jwt_token

# Create your views here.

CustomUser = get_user_model()


@user_creation_doc
class UserViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['post', 'patch','delete','get', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        user_id = self.kwargs.get('pk')

        if user.is_staff:
            return CustomUser.objects.all()

        # For regular users, only return their own details
        if user.is_authenticated and str(user.id) == user_id:
            return CustomUser.objects.filter(id=user_id)
        return CustomUser.objects.none()

    def get_object(self):
        obj = self.get_queryset().filter(id=self.kwargs.get('pk')).first()
        if obj is None:
            raise NotFound('User not found')
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            auth_token = get_jwt_token(user=user)
            response_data = {'status': 'Success', 'message': 'Registration successful', 'detials': {
                'accessToken': str(auth_token.access_token),
                'user': serializer.data
            }}

            return Response(response_data, status=status.HTTP_201_CREATED)

        # If serializer is not valid, return validation errors with status code 422
        return Response({
            "status": "Unprocessable Entity",
            "message": "Registration unsuccessful",
            "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "errors": serializer.errors
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = self.request.user

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def get_serializer_context(self):
        return {'request': self.request}

class LoginUserViewset(RetrieveModelMixin,GenericViewSet):
    serializer_class = LoginUserSerailzer

    def get_queryset(self):
        email = self.request.get('email')
        password = self.request.get('pasword')


        return super().get_queryset()