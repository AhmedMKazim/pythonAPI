from rest_framework import permissions



class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profile."""
    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile."""
        if request.method in permissions.SAFE_METHODS: # if user the method is get only
            return True
        # here if obj data is updated
        return obj.id == request.user.id # obj is the object which edited by the user
