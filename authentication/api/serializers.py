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