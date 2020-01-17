from rest_framework import permissions
import logging

class IsSuperUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    #logger = logging.getLogger(__name__)

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        # return obj == request.user
        # logging.debug("HELLO")
        return request.user.is_staff()
