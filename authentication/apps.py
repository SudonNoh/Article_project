from django.apps import AppConfig


class AuthenticationAppConfig(AppConfig):
    name = 'authentication'
    label = 'authentication'
    verbose_name = 'Authentication'
    
    def ready(self):
        import authentication.signals

# Django에 custom app 설정을 등록하는 방법이다. Django는 등록된 각 앱의
# 'default_app_config' 속성(property)을 찾고 해당 값을 기반으로 올바른
# app config를 사용합니다.
default_app_config = 'authentication.AuthenticationAppConfig'