from rest_framework import status
from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from profiles.models import Profile
from profiles.api.renderers import ProfileJSONRenderer
from profiles.api.serializers import ProfileSerializer
from .exceptions import ProfileDoesNotExist

class ProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer
    
    def retrieve(self, request, username, *args, **kwargs):
        # request 받은 profile을 검색해보고, 없으면 exception error를
        # 반환한다.
        try:
            # 우리는 불필요한 데이터베이스 호출을 피하기 위해서 
            # 'select_related' method를 사용한다. 
            profile = Profile.objects.select_related('user').get(
                # 여기서 받아오는 username은 url에서 받아오는 username 이다.
                # user__username : 검색을 위한 db 상의 username 중
                # username : url에서 받아온 username에 해당하는 profile을 찾는다.
                user__username=username
            )
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist
        
        serializer = self.serializer_class(profile)
        
        return Response(serializer.data, status=status.HTTP_200_OK)