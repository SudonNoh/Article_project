from core.renderers import BaseJSONRenderer


class ArticleJSONRenderer(BaseJSONRenderer):
    object_label = 'article'
    pagination_object_label = 'articles'
    pagination_count_label = 'articlesCount'


class CommentJSONRenderer(BaseJSONRenderer):
    object_label = 'comment'
    pagination_object_label = 'comments'
    pagination_count_label = 'commentsCount'