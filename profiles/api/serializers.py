from rest_framework import serializers
from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    birth_date = serializers.DateField(source='user.birth_date')
    introduce = serializers.CharField(allow_blank=True, required=False)
    image = serializers.CharField(allow_blank=True)
    
    class Meta:
        model = Profile
        fields = [
            'username',
            'birth_date',
            'introduce',
            'image',
        ]
        read_only_fields = ['username', 'birth_date', ]