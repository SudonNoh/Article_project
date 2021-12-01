from django.contrib.auth import get_user, get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_staff == True:
                return True
            elif hasattr(obj, 'author'):
                # print('obj: ', type(obj.author.user), '  ::  ', obj.author.user)
                # print('request: ', type(request.user), '  ::  ', request.user)
                return obj.author.user == request.user
            elif obj.__class__ == get_user_model():
                return obj.id == request.user.id
            return False
        else:
            False
            

# permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_staff == True:
                return True
            # method가 database에 영향이 없는 것들은 허용
            elif request.method in SAFE_METHODS:
                return True
            elif hasattr(obj, 'author'):
                return obj.author.user == request.user
            # 이 부분은 생각해 볼 필요가 있음
            elif obj.__class__ == get_user_model():
                return obj.id == request.user.id
            return False
        else:
            False