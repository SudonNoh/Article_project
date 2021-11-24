from django.contrib.auth import authenticate
from rest_framework import serializers

from authentication.models import User



class RegistrationSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        max_length = 128,
        min_length = 8,
        # write_only = True로 설정되면 인스턴스를 updating, creating 할 때에는
        # 사용되지만 serializing 할 때는 포함되지 않는다.
        write_only = True
    )
    
    token = serializers.CharField(
        max_length=255, 
        read_only=True
    )
    
    # serialize 할 부분을 설정한다.
    class Meta:
        model = User
        fields = [
            'email', 
            'username', 
            'password', 
            'birth_date', 
            'phone_number', 
            'token'
        ]
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    
    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        
        if email is None:
            raise serializers.ValidationError(
                'An Email address is required to log in.'
            )
        
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        
        # 'authenticate' 는 user의 email과 password의 조합을 확인하는데 사용된다.
        # 만약 email과 password 조합을 DB에서 확인한 결과가 없으면 None을 반환한다.
        user = authenticate(username=email, password=password)
        
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }