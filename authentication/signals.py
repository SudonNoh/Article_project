from django.db.models.signals import post_save
from django.dispatch import receiver

from profiles.models import Profile

from .models import User

@receiver(post_save, sender=User)
def created_related_profile(sender, instance, created, *args, **kwargs):
    # 우리는 User instance가 처음으로 만들어졌을 때만 이것이 동작하도록 해야한다.
    # 즉, 이 구간에서 instance 가 created 된 것인지를 확인해야 한다.
    # 이 signal을 실행하는 요소가 update 라면 해당 User는 이미 profile을 갖고
    # 있다는 것을 알 수 있다.
    if instance and created:
        instance.profile = Profile.objects.create(user=instance)
