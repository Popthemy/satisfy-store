USER_GET_QUERYSET = """
- If the user is a staff member, returns all users.
- If the user is authenticated and is querying their own details, returns only their details.
- Otherwise, returns an empty queryset.
"""

USER_CREATE = "Create a new user with the provided information."

USER_DELETE = """  Permanently removes a user account from the system.
        This action is irreversible and should be used with caution."""
USER_RETRIEVE="Retrieve the details of a specific user by ID. Admins can retrieve any user's details,while regular users can only access their own details."
USER_UPDATE = "Allows partial updates to the user's details. Only accessible to the authenticated user for their own details."
USER_ME = """This endpoint allows an authenticated user to retrieve or update their own details.
        - **GET**: Retrieves the current user's details.
        - **PATCH**: Partially updates the current user's details with the data provided."""

USER_LOGIN = 'Logs user in with the provided information (email and password) and return their details.'

"""
class LoginUserView(APIView):
    serializer_class = LoginUserSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data

            refresh_token = get_jwt_token(user)

            user_obj =User.objects.get(email=user.email)
            serializer= UserSerializer(user_obj)

            response_data = {
                "status": "success",
                "message": "Login successful",
                "data": {
                    "accessToken": str(refresh_token.access_token),
                    "user": serializer.data
                }
            }

            return Response(response_data, status=status.HTTP_200_OK)

        return Response({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": status.HTTP_401_UNAUTHORIZED
        }, status=status.HTTP_401_UNAUTHORIZED)


        
        def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = User.objects.filter(email=email).first()
            if user:
                if user.check_password(password):
                    return user
                raise serializers.ValidationError(
                    [{'field': 'password', 'message': 'Incorrect password'}])
            raise serializers.ValidationError(
                [{'field': 'email', 'message': 'Incorrect email'}])
        raise serializers.ValidationError(
            [{'field': 'email and password', 'message': 'Email and password cannot be empty'}])
"""