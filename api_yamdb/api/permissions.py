from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed 


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method not in SAFE_METHODS:
            return (
                request.user.is_authenticated
                and (request.user.role == 'admin' or request.user.is_staff)
            )
        return True

        # if request.method in SAFE_METHODS:
        #     return True
        # return request.user and request.user.is_staff
    
        # return (
        #     request.method in SAFE_METHODS
        #     or (request.user and request.user.is_authenticated)
        # )


class IsAdminAndIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == 'admin'
                or request.user.is_staff
            )


class IsAdminOrModerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user and request.user.is_authenticated)
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST' and request.user.is_authenticated:
            return True
        return (
            request.user.is_staff
            or request.user.role == 'admin'
            or request.user.role == 'moderator'
            or obj.author == request.user
        )
