from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


from store.serializers import UserSerializer
from utils.reusable_func import get_jwt_token
# Create your views here.

CustomUser = get_user_model()


class UserViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    http_method_names = ['post']
    # permission_classes = [AllowAny]

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
