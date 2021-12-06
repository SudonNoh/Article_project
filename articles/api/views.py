from functools import partial
from rest_framework import generics, mixins, serializers, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.views import APIView

from articles.models import (
    Article, Comment, Tag
    )
from .renderers import ArticleJSONRenderer, CommentJSONRenderer
from .serializers import (
    ArticleSerializer, CommentSerializer, TagSerializer
    )
from core.permissions import IsOwnerOnly

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
        serializer_context = {
            'author': request.user.profile,
            'request': request
            }
        serializer_data = request.data
        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, slug):
        serializer_context = {'request': request}
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')
        
        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context
            )
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # update시에 title이 변경되어도 기존에 있던 slug는 변경되지 않는다.
    def update(self, request, slug):
        serializer_context = {'request': request}
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')
        
        serializer_data = request.data
        
        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context,
            data=serializer_data, 
            partial=True
        )
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        # 해당 유저가 favorite을 했는지 안했는지 여부를 알기 위해 context를 추가
        # 로그인 유저의 정보를 함께 보내줌
        serializer_context = {'request': request}
        serializer_instances = self.queryset.all()
        
        serializer = self.serializer_class(
            serializer_instances,
            context=serializer_context,
            many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentListCreateAPIView(generics.ListCreateAPIView):
    lookup_field ='article__slug'
    # url에서 만약 '<str:artiicle_slug>' 부분이 있다면
    # lookup_url_kwarg가 갖는 값은 url에서 '<str:article_slug>' 부분이다.
    # 즉, url이 article-qwa/comments 였으면 lookup_url_kwarg = 'article-qwa'
    # 가 되는 것
    lookup_url_kwarg = 'article_slug'
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.select_related(
        'article', 'article__author', 'article__author__user',
        'author', 'author__user'
    )
    renderer_classes = (CommentJSONRenderer,)
    serializer_class = CommentSerializer
    
    def filter_queryset(self, queryset):
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        # print('self.kwargs:  ', self.kwargs)
        # self.kwargs:   {'article_slug': 'title-example5-aeh5wg'}
        return queryset.filter(**filters)
    
    def create(self, request, article_slug=None):
        print('request.data:  ', request.data)
        # request.data:   {'body': 'comment example8'}
        data = request.data
        # context:   {'author': <Profile: client99>, 'article': <Article: updated title  example5>}
        context = {'author': request.user.profile}
        
        try:
            context['article'] = Article.objects.get(slug=article_slug)
            print('context:  ', context)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')
        
        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentsDestroyAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Comment.objects.all()

    def destroy(self, request, article_slug=None, comment_pk=None):
        try:
            comment = Comment.objects.get(pk=comment_pk)
        except Comment.DoesNotExist:
            raise NotFound('A comment with this ID does not exist.')

        comment.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CommentUpdateAPIView(generics.UpdateAPIView):
    lookup_url_kwarg = 'comment_pk'
    permission_classes = (IsOwnerOnly,)
    renderer_classes = (CommentJSONRenderer,)
    serializer_class = CommentSerializer
    
    def get_object(self):
        try:
            comment = Comment.objects.get(pk=self.kwargs[self.lookup_url_kwarg])
            self.check_object_permissions(self.request, comment)
            return comment
        except Comment.DoesNotExist:
            raise NotFound('A comment with this Id does not exist.')
        
    def patch(self, request, article_slug=None, comment_pk=None):
        comment = self.get_object()
        data = request.data

        serializer = self.serializer_class(
            comment, data=data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class ArticlesFavoriteAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer
    
    def delete(self, request, article_slug=None):
        profile = self.request.user.profile
        serializer_context = {'request': request}
        
        try:
            article = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug was not found.')

        profile.unfavorite(article)
        
        serializer = self.serializer_class(
            article,
            context=serializer_context
        )
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, article_slug=None):
        # user 의 profile을 불러온다.
        profile = self.request.user.profile
        # serializer_context로 request 
        serializer_context = {'request': request}
        
        try:
            article = Article.objects.get(slug=article_slug)
            
        except Article.DoesNotExist:
            raise NotFound('An article with this slug was not found.')
        
        profile.favorite(article)
        
        serializer = self.serializer_class(
            article,
            context=serializer_context
        )
        
        return Response(serializer.data, status.HTTP_201_CREATED)
    

class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    
    def get(self, request):
        serializer_data = self.get_queryset()
        serializer = self.serializer_class(serializer_data, many=True)
        
        return Response({
            'tags': serializer.data
        }, status=status.HTTP_200_OK)