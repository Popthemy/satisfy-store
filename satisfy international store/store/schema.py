from drf_spectacular.utils import extend_schema, extend_schema_view
from store.serializers import UserSerializer
from store.docstring import *


# user_creation_doc = extend_schema(
#   request = UserSerializer,
#   responses = {201:UserSerializer},
# )

user_creation_doc = extend_schema_view(
    partial_update=extend_schema(request=UserSerializer,  methods=[
                         'PATCH'], summary="Partially update user",description=USER_UPDATE),
                         
    create=extend_schema(request=UserSerializer,
                         summary="Add a new user to the system.",description=USER_CREATE),

    destroy=extend_schema(summary="Delete a user by their unique identifier.", 
                          description=USER_DELETE)
)
