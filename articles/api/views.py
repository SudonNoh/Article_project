from functools import partial
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from articles.models import (
    Article, Comment
    )
from .renderers import ArticleJSONRenderer
from . serializers import (
    ArticleSerializer, CommentSerializer
    )


class ArticleViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
    ):
    
    lookup_field = 'slug'
    queryset = Article.objects.select_related('author', 'author__user')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer
    
    def create(self, request):
        serializer_context = {'author': request.user.profile}
        serializer_data = request.data
        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, slug):
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')
        
        serializer = self.serializer_class(serializer_instance)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # update시에 title이 변경되어도 기존에 있던 slug는 변경되지 않는다.
    def update(self, request, slug):
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')
        
        serializer_data = request.data
        
        serializer = self.serializer_class(
            serializer_instance, data=serializer_data, partial=True
        )
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)

# 나를 기준으로
# 글을 기준으로
class CommentViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):

lookup_field = 'article'

