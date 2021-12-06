from rest_framework import serializers

from articles.models import Tag


class TagRelatedField(serializers.RelatedField):
    def get_queryset(self):
        return Tag.objects.all()
    
    # get_or_create method : 객체(object)를 조회할 때 유용하게 사용
    # 객체가 DB에 존재하는 경우 DB에서 객체를 얻고, 존재하지 않으면 생성
    # (object,created) 라는 tuple 형식으로 반환
    # 첫번째 인자(object)는 우리가 검색해서 불러오려고 하는 instance
    # 두번째 인자(created)는 boolean flag
    # created가 True일 때 get_or_create method가 생성된 것을 의미
    # created가 False일 때 instance를 DB에서 불러왔음을 의미
    def to_internal_value(self, data):
        tag, created = Tag.objects.get_or_create(tag=data, slug=data.lower())
        
        return tag
    
    def to_representation(self, value):
        return value.tag