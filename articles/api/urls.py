from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    ArticleViewSet, 
    CommentListCreateAPIView, 
    CommentUpdateAPIView, 
    CommentsDestroyAPIView,
    ArticlesFavoriteAPIView,
    TagListAPIView,
    ArticlesFeedAPIView
)

# APPEND_SLASH=False : When use trailing_slash, you should put it in settings.
router = DefaultRouter(trailing_slash=False)
router.register(r'', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<str:article_slug>/comments', CommentListCreateAPIView.as_view()),
    path(
        '<str:article_slug>/comments/<int:comment_pk>/delete', 
        CommentsDestroyAPIView.as_view()
    ),
    path(
        '<str:article_slug>/comments/<int:comment_pk>', 
        CommentUpdateAPIView.as_view()
    ),
    path(
        '<str:article_slug>/favorite', 
        ArticlesFavoriteAPIView.as_view()
    ),
    path(
        'tags/all', TagListAPIView.as_view(),
    ),
    path(
        'feed/all', ArticlesFeedAPIView.as_view(),
    )
]