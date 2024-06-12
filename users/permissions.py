from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    message = "Вы не являетесь модератором"

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator').exists()


class IsOwner(BasePermission):
    message = "Вы не являетесь владельцем"

    def has_object_permission(self, request, view, obj):
        if request.user == obj:

            return request.method in ('GET', 'PUT', 'PATCH', 'DELETE')
        return False

class IsSuperuser(BasePermission):
    message = "Вы не являетесь суперюзером"
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False