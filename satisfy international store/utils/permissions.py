from rest_framework.permissions import BasePermission

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Custom permission to only allow unauthenticated users to access the create endpoint,
    and authenticated users to access the partial_update and delete endpoints.
    """

    def has_permission(self, request, view):
        # Allow unauthenticated users to POST (create)
        if request.method == 'POST':
            return not request.user.is_authenticated
        
        # Allow authenticated users to PATCH (partial update) and DELETE
        if request.method in ['PATCH', 'DELETE']:
            return request.user.is_authenticated
        
        # Allow GET requests for everyone
        return True
