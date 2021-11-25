from rest_framework.exceptions import APIException


class ProfileDoesNotExist(APIException):
    status_code = 400
    default_detail = 'The requested profile does not exist.'
    
    # 이번 예시는 굉장히 간단한 exception 으로, Django는 언제든 필요할 때
    # custom esception을 만들 수 있도록 한다. APIException을 상속받고 
    # `status_code`와 `default_detail`을 명시하면 된다.