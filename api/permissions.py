from rest_framework import permissions



class IsOwnerOrReadOnly(permissions.BasePermission):
    message = 'You are not the the onwer'

    def has_object_permission(self, request, view, obj):
        my_safe_method = ['GET']
        if request.method in my_safe_method:
            return True
        return obj.user_id == request.user.id
