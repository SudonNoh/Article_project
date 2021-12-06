import json

from rest_framework.renderers import JSONRenderer

class BaseJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'
    pagination_object_label = 'objects'
    pagination_object_count = 'count'
    
    def render(self, data, media_type=None, renderer_context=None):
        if data.get('results', None) is not None:
            return json.dumps({
                self.pagination_object_label: data['results'],
                self.pagination_count_label: data['count']
            })
            
            # 만약 view에서 error를 받아오면, 'data' 안에는 'errors' key가 포함되어
            # 있는 상태이다. 'data'에 'errors'가 포함되어 있는지 확인하고, 'errors'를 
            # 처리할 때 기본 JSONRenderer가 처리하도록 한다.
        elif data.get('errors', None) is not None:
            return super(BaseJSONRenderer, self).render(data)
        
        else:
            return json.dumps({
                self.object_label: data
            })