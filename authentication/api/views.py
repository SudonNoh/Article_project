from rest_framework import renderers, serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView

from .serializers import (
    RegistrationSerializer, LoginSerializer, UserSerializer
)
from .renderers import UserJSONRenderer


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer
    
    def post(self,request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer
    
    def get(self, request, *args, **kwargs):
        # 이 부분에서 validate 하거나 save 하지 않습니다. 다만 'User' object들을
        # client에게 보내기 위해 serialize 할 뿐입니다.
        serializer = self.serializer_class(request.user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        user_data = request.data
        
        serializer_data = {
            'username': user_data.get('username', request.user.username),
            'email': user_data.get('email', request.user.email),
            'birth_date': user_data.get('birth_date', request.user.birth_date),
            'phone_number': user_data.get('phone_number', request.user.phone_number),
            
            'profile': {
                'introduce': user_data.get('introduce', request.user.profile.introduce),
                'image': user_data.get('image', request.user.profile.image)
            }
        }
        
        # 이곳에 serialize, validate, save pattern등 전에 얘기했던 기능들을 추가합니다.
        # 여기서 partial 옵션은 부분적으로 업데이트가 가능하도록 하는 기능입니다.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)