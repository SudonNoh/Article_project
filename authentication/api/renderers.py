import json

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # 우리가 token key를 받을 때 token key의 타입은 byte형입니다.
        # byte형은 직렬화가 되지 않기 때문에 User 객체를 rendering 하기 전에
        # decode 해주어야 합니다.
        token = data.get('token', None)
        
        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')

        return json.dumps({
            'user': data
        })