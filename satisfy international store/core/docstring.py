USER_GET_QUERYSET = """
- If the user is a staff member, returns all users.
- If the user is authenticated and is querying their own details, returns only their details.
- Otherwise, returns an empty queryset.
"""

USER_CREATE = "Create a new user with the provided information."

USER_DELETE = """  Permanently removes a user account from the system.
        This action is irreversible and should be used with caution."""
USER_RETRIEVE = "Retrieve the details of a specific user by ID. Admins can retrieve any user's details,while regular users can only access their own details."
USER_UPDATE = "Allows partial updates to the user's details. Only accessible to the authenticated user for their own details."
USER_ME = """This endpoint allows an authenticated user to retrieve or update their own details.
        - **GET**: Retrieves the current user's details.
        - **PATCH**: Partially updates the current user's details with the data provided."""

USER_LOGIN_RESPONSES = responses = {
    200: {
        'description': 'Successful login',
        'examples': {
            'status': 'Authorized',
            'message': 'Login successful',
            'details': {
                'Token': {
                    'refresh': 'string',
                    'access': 'string'
                },
                'user': {
                    'id': 'string',
                    'email': 'string'
                }
            }
        }
    },
    422: {
        'description': 'Unprocessable entity',
        'examples': {
            'status': 'Unprocessable Entity',
            'message': 'Login unsuccessful',
            'statusCode': 422,
            'errors': {
                'email': ['user with this email does not exist.']
            }
        }
    }
}
USER_LOGIN_SUMMARY = """Allows a user to authenticate by providing valid credentials (email and password) 
                        and receive JWT tokens (access and refresh) for session management.
                        """


USER_LOGOUT_SUMMARY = """This endpoint allows users to log out by submitting their refresh token.
                        The token will be blacklisted, making it unusable for future authentication requests.
                        """


USER_LOGOUT_RESPONSES = """ responses={
        status.HTTP_205_RESET_CONTENT: {
            'description': 'Logout successful, token has been invalidated.'
        },
        status.HTTP_400_BAD_REQUEST: {
            'description': 'Invalid or missing refresh token.'
        }
    }
    """

USER_LOGOUT_DESCRIPTION ="""
    This endpoint allows authenticated users to log out by blacklisting the refresh token.
    The client needs to provide the refresh token in the POST request body. 
    Once logged out, the token will be invalidated and cannot be used for future access.
    """

