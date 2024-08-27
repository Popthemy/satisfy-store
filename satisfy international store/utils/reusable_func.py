from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response


def get_jwt_token(user):
    try:
        token = RefreshToken.for_user(user=user)
        return token
    except Exception as e:
        return Response({
            'status': 'error', 'message': 'error generating authentication token', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
