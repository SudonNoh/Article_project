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
    
    def __str__(self):
        return self.user.username