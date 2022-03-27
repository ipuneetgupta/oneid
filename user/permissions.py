from rest_framework import permissions
from rest_framework import serializers
from user1.serializers import UserSerializer, User

class IsLoggedInUserOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # try:
        #     if User.objects.filter(email__iexact=request.data["email"]).exists():
        #         raise serializers.ValidationError("email already exists")
        # except Exception as e:
        #     error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
        #     raise serializers.ValidationError(error)
        return obj == request.user or request.user.is_staff


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff