from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from core.utils import generate_random_string

from .models import Article


@receiver(pre_save, sender=Article)
def add_slug_to_article_if_not_exists(sender, instance, *args, **kwargs):
    MAXIMUM_SLUG_LENGTH = 255
    
    if instance and not instance.slug:
        slug = slugify(instance.title)
        unique = generate_random_string()
        
        if len(slug) > MAXIMUM_SLUG_LENGTH:
            slug = slug[:MAXIMUM_SLUG_LENGTH]
            
        while len(slug + '-' + unique) > MAXIMUM_SLUG_LENGTH:
            parts = slug.split('-')
            
            if len(parts) is 1:
                # 만약에 slug가 hyphen을 갖고있지 않은 경우 추가 unique 문자열을
                # 추가하고, hyphen을 넣기 위해 끝에 unique자리와 hyphen 자리 1을
                # 제거합니다.
                slug = slug[:MAXIMUM_SLUG_LENGTH - len(unique) - 1]
            else:
                slug = '-'.join(parts[:-1])
                
        instance.slug = slug + '-' + unique