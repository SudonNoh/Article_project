from core.renderers import BaseJSONRenderer


class ArticleJSONRenderer(BaseJSONRenderer):
    object_label = 'article'
    object_label_plural = 'articles'