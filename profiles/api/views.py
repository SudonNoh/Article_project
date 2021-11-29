from rest_framework import status
from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from profiles.models import Profile
from profiles.api.renderers import ProfileJSONRenderer
from profiles.api.serializers import ProfileSerializer
# from .exceptions import ProfileDoesNotExist

class ProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Profile.objects.select_related('user')
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer
    
    def retrieve(self, request, username, *args, **kwargs):
        # request 받은 profile을 검색해보고, 없으면 exception error를
        # 반환한다.
        try:
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('A profile with this username does not exist.')

        serializer = self.serializer_class(profile)
        
        return Response(serializer.data, status=status.HTTP_200_OK)