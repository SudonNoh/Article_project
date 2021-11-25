from core.renderers import BaseJSONRenderer

class ProfileJSONRenderer(BaseJSONRenderer):
    # object_label을 override
    object_label = 'profile'