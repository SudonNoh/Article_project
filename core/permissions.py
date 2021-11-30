from django.contrib.auth import get_user, get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_staff == True:
                return True
            elif hasattr(obj, 'author'):
                print('obj: ', type(obj.author.user), '  ::  ', obj.author.user)
                print('request: ', type(request.user), '  ::  ', request.user)
                return obj.author.user == request.user
            elif obj.__class__ == get_user_model():
                return obj.id == request.user.id
            return False
        else:
            False