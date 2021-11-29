from rest_framework.views import exception_handler

def core_exception_handler(exc, context):
    # 만약 넘어온 exception이 우리가 명확하게 여기서 handle하지 못한다면
    # DRF에서 제공하는 exception handler에 넘겨줄 예정이다.
    # 우리가 넘어온 exception type을 handle 할 수 있다고 하더라도 여전히
    # DRF에서 넘어온 response를 받아 사용하고 싶기 때문에 해당 response를 먼저 
    # 받도록 한다.
    response = exception_handler(exc, context)
    '''
        print('exception_handler, response: ', response)
        exception_handler, response:  <Response status_code=400, "text/html; charset=utf-8">
    '''
    
    # 우리가 처리할 수 있는 exception error를 이곳에 넣어둔다.
    handlers = {
        'NotFound': _handle_not_found_error,
        # 'ProfileDoesNotExist': _handle_generic_error,
        'ValidationError': _handle_generic_error
    }
    
    # 이것은 우리가 현재 exception type이 무엇인지를 식별하는 방법이다.
    # 우리는 이것으로 우리가 처리해야 하는 오류인지, DRF에서 처리해야하는
    # 것인지를 판단할 떄 사용한다.
    exception_class = exc.__class__.__name__
    '''
        print('exception_class:  ', exception_class)
        exception_class:   ValidationError
    '''
    
    if exception_class in handlers:
        # exception_class로 받아온 exception이 우리가 처리할 수 있는 것이라면
        # 처리하고, 그렇지 않다면 기본 exception_handler를 이용한 response를
        # 반환한다.
        return handlers[exception_class](exc, context, response)
    
    # 우리가 처리할 수 없는 exception 일 경우에 위에서 받아온 response를 반환
    return response

def _handle_generic_error(exc, context, response):
    # 이것은 우리가 만들 수 있는 가장 simple한 exception handler이다.
    # 아래 코드에서 우리는 DRF에 의해 반환된 response를 받고, 그 response를
    # 'errors' Key에 포함시켜 반환합니다.
    '''
        print('response:  ', response)
        response:   <Response status_code=400, "text/html; charset=utf-8">
        print('response.data:  ', response.data)
        {'error': [ErrorDetail(string='A user with this email and password was not found.', code='invalid')]}
    '''
    response.data = {
        'errors': response.data
    }
    
    '''
        print('update_response: ', response)
        update_response:  <Response status_code=400, "text/html; charset=utf-8">
        print('update_response.data: ', response.data)
        update_response.data:  {
            'errors': {
                'error': [
                    ErrorDetail(string='A user with this email and password was not found.', code='invalid')
                    ]
                }
            }
    '''
    return response

def _handle_not_found_error(exc, context, response):
    view = context.get('view', None)
    
    if view and hasattr(view, 'queryset') and view.queryset is not None:
        error_key = view.queryset.model._meta.verbose_name
        
        response.data = {
            'errors': {
                error_key:response.data['detail']
            }
        }
    else:
        response = _handle_generic_error(exc, context, response)
    
    return response