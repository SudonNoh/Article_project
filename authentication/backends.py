import jwt

from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'
    
    def authenticate(self, request):
        
        """
            'authenticate' method는 endpoint에 인증이 필요한지 여부와 상관없이 
            모든 요청(request)에서 호출된다.
            
            'authenticate'는 두 종류의 value값을 반환한다.
            
            1) 'None' - 어떤 요청의 header에 'token'을 포함하지 않는 경우 'None'값을
                        반환한다. 보통 우리는 이런 경우를 인증에 실패한 경우라고 생각하면 된다. 

            2) '(user, token)' - 인증이 성공적으로 이루어졌을 때는 user/token 조합을 반환한다.
            
            만약 두 경우 외에 다른 경우가 생긴다면 그것은 어떤 error가 발생했음을 의미한다.
            error가 발생한 경우 우리는 어떤 것도 반환하지 않는다. 단지 'AuthenticationFailed' 
            error를 보내고, 나머지는 DRF가 처리하도록 한다.
        """
        request.user = None
        
        # 'auth_header'는 두 가지 요소(element)를 배열로 갖고 있어야 한다.
        # 1) authentication header의 이름(여기에서는 'Token')
        # 2) 인증해야 하는 JWT
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()
    
        if not auth_header:
            return None
        
        if len(auth_header) == 1:
            # Invalid token header. 
            return None
        
        elif len(auth_header) > 2:
            # Invalid token header. 'token'은 하나의 string으로 구성되어야 하고,
            # 공백을 포함해서는 안된다. 앞서 split()했을 때 더 많은 수의 원소로 쪼개지는
            # 경우 invalid 처리 하기 위함이다.
            return None
        
        # 초반부에서 언급한 것처럼 우리가 사용하는 JWT library는 'byte' type을 처리할 수 
        # 없다. 그렇기 때문에 우리는 'prefix'와 'token' 부분을 decode해주어야 한다.
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None
        
        return self._authenticate_credentials(request, token)
    
    def _authenticate_credentials(self, request, token):
        """
            위의 과정을 통과한 user에게 접근을 허용하도록 한다. 만약 인증이 성공적이라면
            user와 token을 반환해주고, 그렇지 않은 경우에는 error를 반환한다.
        """
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        except:
            msg = 'Invalid authentication. Could not decode token'
            raise exceptions.AuthenticationFailed(msg)
        
        try:
            user = User.objects.get(pk=payload['id'])
            
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)
        
        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)
        
        return (user, token)