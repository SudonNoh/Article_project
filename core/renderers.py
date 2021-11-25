import json

from rest_framework.renderers import JSONRenderer

class BaseJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    object_label = 'object'
    
    def render(self, data, media_type=None, renderer_context=None):
        # 만약 view에서 error를 받아오면, 'data' 안에는 'errors' key가 포함되어
        # 있는 상태이다. 'data'에 'errors'가 포함되어 있는지 확인하고, 'errors'를 
        # 처리할 때 기본 JSONRenderer가 처리하도록 한다. 
        errors = data.get('errors', None)
        
        if errors is not None:
            # 앞서 언급한 것과 같이 우리는 기본 JSONRenderer를 이용해 errors를
            # rendering 할 것이다.
            return super(BaseJSONRenderer, self).render(data)
        
        return json.dumps({
            self.object_label: data
        })