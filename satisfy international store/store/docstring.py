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

USER_LOGIN =  """
       

        Validates the provided email and password. If valid, generates a JWT token for 
        the user and returns it along with the user's ID and email. If the credentials are 
        invalid, returns an error response.

        Parameters
        ----------
        request : Request
            The incoming HTTP request containing the user's email and password.

        Returns
        -------
        Response
            A Response object containing the JWT token on success, or an error message 
            on failure.
        """

USER_LOGOUT = 