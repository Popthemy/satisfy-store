from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from store.serializers import UserSerializer,LoginUserSerializer
from store.docstring import *


user_creation_doc = extend_schema_view(

    create=extend_schema(request=UserSerializer,
                         summary="Add a new user to the system.", description=USER_CREATE),
    retrieve=extend_schema(
        summary="Retrieve user by ID",
        description=USER_RETRIEVE,
    ),
    partial_update=extend_schema(methods=[
        'PATCH'], summary="Partially update user", description=USER_UPDATE),

    destroy=extend_schema(summary="Delete a user by their unique identifier.",
                          description=USER_DELETE),

    me=extend_schema(summary="Retrieve or update the currently authenticated user's details.", methods=['GET', 'PATCH'],
                     description=USER_ME)
)

user_login_doc = extend_schema(
  request = LoginUserSerializer,
  summary= 'Handle user login requests.',
  description=USER_LOGIN
)

