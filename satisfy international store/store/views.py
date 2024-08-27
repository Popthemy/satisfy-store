from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status


from store.serializers import UserSerializer
from utils.reusable_func import get_jwt_token
from store.schema import user_creation_doc
# Create your views here.

CustomUser = get_user_model()


class PartialUpdateOnlyMixin:
    '''FOR THE PATCH METHOD ALONE ON THE USER MODEL'''

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

@user_creation_doc
class UserViewSet(CreateModelMixin, PartialUpdateOnlyMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    # http_method_names = ['post', 'delete', 'get',]


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
