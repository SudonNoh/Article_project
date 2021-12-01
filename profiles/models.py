from django.db import models
from core.models import TimestampedModel


class Profile(TimestampedModel):
    # 언급한 대로 Profile model과 User model은 상속관계가 있다.
    # 따라서 둘 사이에 One-To-One 관계를 만들어준다.
    # 모든 사용자들은 하나의 id에 하나의 profile을 가질 수 있다.
    user = models.OneToOneField(
        'authentication.User', on_delete = models.CASCADE
    )
    
    # 사용자들이 자신을 소개할 수 있는 field로 비워놓아도 상관없기 때문에
    # 'blank=True'로 설정했다.
    introduce = models.TextField(blank=True)
    
    # 사용자의 프로필 사진을 등록할 수 있도록 한다. 등록하지 않은 경우
    # 기본 이미지가 적용되도록 설정한다.
    image = models.URLField(blank=True)
    
    # 관계의 양쪽이 동일한 model인 Many-To-Many 관계의 예시이다. 이 예시에서 model은
    # 'profile'이다. 본문에서 언급했듯 이 관계는 단방향이다. 한쪽에 follow 했다고 해서
    # 다른 한쪽이 반드시 follow했다고 볼 수 없다. 이것은 symmetrical=False로 확인할 
    # 수 있다.
    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False
    )
    
    def __str__(self):
        return self.user.username
    
    def follow(self, profile):
        """Follow 'profile' if we're not already following 'profile'."""
        self.follows.add(profile)
        
    def unfollow(self, profile):
        """Unfollow 'profile' if we're already following 'profile'."""
        self.follows.remove(profile)
        
    def is_following(self, profile):
        """
        Returns True if we're following 'profile'; False otherwise.
        "Am I following this person?"
        """
        return self.follows.filter(pk=profile.pk).exists()

    def is_followed_by(self, profile):
        """
        Returns True if 'profile' is following us; False otherwise.
        "Is this person following me?"
        """
        # related_name = 'followed_by'
        return self.followed_by.filter(pk=profile.pk).exists()