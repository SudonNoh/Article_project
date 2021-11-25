from rest_framework import serializers
from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    birth_date = serializers.DateField(source='user.birth_date')
    introduce = serializers.CharField(allow_blank=True, required=False)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = (
            'username',
            'birth_date',
            'introduce',
            'image',
        )
        read_only_fields = ('username', 'birth_date', )
        
    def get_image(self, obj):
        if obj.image:
            return obj.image
        
        return 'https://static.productionready.io/images/smiley-cyrus.jpg'