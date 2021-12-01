from rest_framework import serializers
from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    birth_date = serializers.DateField(source='user.birth_date')
    introduce = serializers.CharField(allow_blank=True, required=False)
    image = serializers.CharField(allow_blank=True)
    following = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = [
            'username',
            'birth_date',
            'introduce',
            'image',
            'following'
        ]
        read_only_fields = [
            'username', 
            'birth_date', 
            ]
    
    # get 요청시에 요청자(request.user)가 instance를 follow 했는지 여부에 대해 확인
    def get_following(self, instance):
        request = self.context.get('request', None)
        
        if request is None:
            return False
        
        if not request.user.is_authenticated:
            return False
        
        follower = request.user.profile
        followee = instance

        # print('follower:  ', follower)
        # print('followee:  ', followee)
        
        return follower.is_following(followee)