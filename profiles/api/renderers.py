from core.renderers import BaseJSONRenderer

class ProfileJSONRenderer(BaseJSONRenderer):
    # object_label을 override
    object_label = 'profile'
    pagination_object_label = 'profiles'
    pagination_count_label = 'profilesCount'