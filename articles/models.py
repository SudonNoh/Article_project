from django.db import models

from core.models import TimestampedModel


class Article(TimestampedModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(db_index=True, max_length=255)
    
    description = models.TextField()
    body = models.TextField()
    
    # 모든 article은 author를 가져야합니다. 작성한 사용자를 명시해야하기 때문입니다.
    # Profile과는 다르게 one-to-one 관계가 아닌 one-to-many 관계를 갖습니다. 왜나하면
    # 한 명의 사용작 여러 개의 기사를 작성할 수 있기 때문입니다. 따라서 이번 Article
    # model에서는 foreign key relationship을 맺어주어야 합니다.
    author = models.ForeignKey(
        'profiles.Profile', on_delete=models.CASCADE, related_name='articles'
    )
    
    tags = models.ManyToManyField(
        'articles.Tag', related_name='article'
    )
    
    def __str__(self):
        return self.title
    
    
class Comment(TimestampedModel):
    body = models.TextField()
    
    article = models.ForeignKey(
        'articles.Article', related_name='comments', on_delete=models.CASCADE
    )
    
    author = models.ForeignKey(
        'profiles.Profile', related_name='comments', on_delete=models.CASCADE
    )
    

class Tag(TimestampedModel):
    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)
    
    def __str__(self):
        return self.tag
    
    