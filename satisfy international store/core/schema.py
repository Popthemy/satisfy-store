from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from core.serializers import UserSerializer, LoginUserSerializer, LogoutUserSerializer
from core.docstring import *


user_creation_doc = extend_schema_view(
    create=extend_schema(
        request=UserSerializer,
        summary="Add a new user to the system.",
        description=USER_CREATE,
        tags=['Authentication']
    ),
    retrieve=extend_schema(
        summary="Retrieve user by ID",
        description=USER_RETRIEVE,
        tags=['Authentication']
    ),
    partial_update=extend_schema(
        methods=['PATCH'],
        summary="Partially update user",
        description=USER_UPDATE,
        tags=['Authentication']
    ),
    destroy=extend_schema(
        summary="Delete a user by their unique identifier.",
        description=USER_DELETE,
        tags=['Authentication']
    ),
    me=extend_schema(
        summary="Retrieve or update the currently authenticated user's details.",
        methods=['GET', 'PATCH'],
        description=USER_ME,
        tags=['Authentication']
    )
)


user_login_doc = extend_schema(
    summary=USER_LOGIN_SUMMARY,
    request=LoginUserSerializer,
    responses=USER_LOGIN_RESPONSES,
    tags=['Authentication']
)

user_logout_doc = extend_schema(
    summary="Logout User",
    description=USER_LOGOUT_DESCRIPTION,
    request=LogoutUserSerializer,
    responses=USER_LOGIN_RESPONSES,
    tags=['Authentication'])

user_refresh_doc = extend_schema(
    summary="JWT Token Refresh",
    description="Refresh the JWT access token using the refresh token.",
    responses={
        200: {
            'type': 'object',
            'properties': {
                'access': {
                    'type': 'string',
                    'description': 'New access token',
                }
            }
        }
    },
    tags=['Authentication']
)
