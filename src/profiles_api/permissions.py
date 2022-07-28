from urllib import request
from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Permite a usuarios editar sus propios perfiles"""

    def has_object_permission(self, request, view, obj):
        """Chequear si el usuario esta intentando editar su propio perfil"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


# Con esta editacion hacer que si publicamos algo en nuestra feed no nos de un error


class UpdateOwnStatus(permissions.BasePermission):
    """Permite actualizar propio status feed"""

    def has_object_permission(self, request, view, obj):
        """Chequear si el usuario esta intentando editar su propio perfil"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_profile_id == request.user.id
