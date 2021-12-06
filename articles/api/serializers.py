from rest_framework import serializers
from rest_framework.utils import serializer_helpers

from profiles.api.serializers import ProfileSerializer

from articles.models import Article, Comment, Tag
from .relations import TagRelatedField


class ArticleSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    description = serializers.CharField(required=False)
    slug = serializers.SlugField(required=False)
    
    favorited = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField(
        method_name='get_favorites_count'
    )
    
    tagList = TagRelatedField(many=True, required=False, source = 'tags')
    
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'slug',
            'author',
            'body',
            'description',
            'favorited',
            'favoritesCount',
            'tagList',
            'createdAt',
            'updatedAt',
        ]
        
    def create(self, validated_data):
        author = self.context.get('author', None)
        
        tags = validated_data.pop('tags', [])
        
        article = Article.objects.create(author=author, **validated_data)
        
        for tag in tags:
            article.tags.add(tag)
            
        return article
    
    def get_created_at(self, instance):
        # timestampedmodel에서 만들어진 created_at 을 isoformat을 통해 형태를 바꾸어
        # get 요청이 있을 때 뿌려줌
        return instance.created_at.isoformat()
    
    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()
    
    # Favorite methods
    def get_favorited(self, instance):
        request = self.context.get('request', None)
        
        if request is None:
            return False
        
        if not request.user.is_authenticated:
            return False
        
        return request.user.profile.has_favorited(instance)
    
    def get_favorites_count(self, instance):
        return instance.favorited_by.count()

class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)
    
    createAt = serializers.SerializerMethodField(method_name='get_created_at')
    updateAt = serializers.SerializerMethodField(method_name='get_updated_at')
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'body',
            'createAt',
            'updateAt'
        ]
        
    def create(self, validated_data):
        article = self.context['article']
        author = self.context['author']
        
        return Comment.objects.create(
            author=author, article=article, **validated_data
        )
        
    def get_created_at(self, instance):
        return instance.created_at.isoformat()
    
    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag',)
        
    def to_representation(self, instance):
        return instance.tag