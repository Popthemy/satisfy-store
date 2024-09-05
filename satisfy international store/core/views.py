from django.contrib.auth import get_user_model

from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from core.serializers import UserSerializer, LoginUserSerializer, LogoutUserSerializer
from utils.permissions import IsAuthenticatedOrReadOnly
from core.schema import user_creation_doc, user_login_doc, user_logout_doc, user_refresh_doc

from utils.reusable_func import get_jwt_token

# Create your views here.

CustomUser = get_user_model()


@user_creation_doc
class UserViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['post', 'patch', 'delete', 'get', 'head', 'options']

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
            response_data = {'status': 'Success', 'message': 'Registration successful', 'details': {
                'Token': auth_token,
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


class LoginUserView(APIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]

    @user_login_doc
    def post(self, request, *args, **kwargs):
        serializer = LoginUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data
            auth_token = get_jwt_token(user)

            response_data = {'status': 'Authorized',
                             'message': 'Login successful',
                             'details': {
                                 'Token': auth_token,
                                 'user': {'id': user.id,
                                          'email': user.email}
                             }}
            return Response(response_data, status=status.HTTP_200_OK)

        return Response({
            "status": "Unprocessable Entity",
            "message": "Login unsuccessful",
            "statusCode": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "errors": serializer.errors
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get_serializer_context(self):
        return {'request': self.request}


class LogoutUserView(APIView):
    permission_classes = [IsAuthenticated]

    @user_logout_doc
    def post(self, request, *args, **kwargs):
        serializer = LogoutUserSerializer(data=request.data)
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"status": "Success", "message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "Error", "message": "Logout failed", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@user_refresh_doc
class CustomTokenRefreshView(TokenRefreshView):
    pass
