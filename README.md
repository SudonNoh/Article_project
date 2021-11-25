# Custom User
## First Day

### Creating the User model
1. Secret Key와 settings.py 파일을 분리하기 위해 <b>*blog/secrests.json*</b>을 manage.py이 있는 project 상위 폴더에 만듭니다. Secret Key가 git에 upload할 때 포함되지 않도록 <b>*blog/.gitignore*</b> 파일에 추가해줍니다.

2. User, 인증 관련 app을 만들기 위해 authentiction app을 만들어줍니다.  
`django-admin startapp authentication`

3. BaseUserManager를 만들기 위해 <b>*blog/authentication/managers.py*</b> 파일을 authentication app 안에 만들어줍니다. 그 안에 class Usermanager를 정의합니다.

4. User 모델을 만들기 위해 <b>*blog/authentication/models.py*</b> 파일을 열어 수정해줍니다. 이 과정에서 <b>*blog/setting/settings.py*</b> 파일을 열어 AUTH_USER_MODEL을 설정해줍니다. 이후 제대로 작동하는지 super user를 생성해 확인합니다.  
`python manage.py createsuperuser`

----
>여기에서 django.db.utils.OperationalError: no such table: 오류가 발생했는데요. createsuperuser를 실행하는 과정에서 db의 table을 지웠고, db.sqlite3 파일을 지워버리면서 생긴 오류 같았습니다.<br><br>이를 해결하기 위해 db.sqlite3 파일을 삭제하고, makemigrations을 우선 진행했습니다. 다음으로 `python manage.py migrate --run-syncdb` 를 실행했습니다. `--run-syncdb` 옵션은 migration을 하지 않고 앱에 대한 테이블을 만드는 것입니다.
----
>django shell에서 model들을 한번에 import 하고 사용하기 위해서 extensions를 설치해줄 필요가 있습니다. `pip install django-extensions` 으로 설치하고 터미널에<br>`python manage.py shell_plus`를 입력해주면 django와 관련된 모듈들이 import 되는 것을 확인할 수 있습니다.<br><br>이제 본인이 정의한 모델명으로 객체에 접근할 수 있습니다. 다음 명령어로 조회해보시기 바랍니다. `User.objects.all()` 여기서 User는 각자 정의한 모델명이므로 작성자에 따라 다를 수 있습니다.
----

## Second Day

5. superuser를 만들어 테스트가 끝나면 인증 부분을 수정해보도록 하겠습니다. 먼저 <b>*blog/authentication/models.py*</b> 파일에 `@property`를 추가해 token을 만들기 위한 함수를 정의해줍니다. 제대로 적용이 되었는지 확인해봅니다. 위에서 언급한 `shell_plus`로 shell을 열고, `User.objects.first().token`으로 token이 잘 나오는지 확인합니다.
----
>pyjwt의 버전이 1.7.1 이하이면 decode를 적용시켜야 합니다. return 부분에 token.decode('utf-8')을 작성해줍니다. 
----
### Registering new users
6. 이제 모델의 내용을 create하거나 update할 때 내용을 직렬화 하기 위한 serializer를 만들어보도록 하겠습니다. 우선 폴더를 하나 더 만들도록 하겠습니다. <b>*blog/authentication/api*</b> api 폴더를 만들어서 serializer 혹은 view, 각 앱에서 사용되는 modelue들을 모아두도록 하겠습니다. 다음으로 해당 폴더에 serializer를 만들도록 하겠습니다. <b>*blog/authentication/api/serializers.py*</b>

7. 실질적으로 새로운 user를 create할 때 사용되는 View를 작성해보도록 하겠습니다. 마찬가지로 <b>*blog/authentication/api/views.py*</b> 파일을 만들어주겠습니다.

8. 지금까지 만든 api들이 정상적으로 작동하는지 확인하기 위해 url 파일에서 바꾸어야 하는 부분을 바꾸도록 하겠습니다. 우선 <b>*blog/authentication/api/urls.py*</b> 파일을 만들고 수정해보도록 하겠습니다. 다음으로는 <b>*blog/setting/urls.py*</b> 파일을 수정하도록 하겠습니다.<br><br>그 후에 postman을 이용해서 사용자 등록이 잘 작동하는지 확인해보겠습니다.

9. 다음은 Rendering 과정을 처리하기 위해 <b>*blog/authentication/api/renderers.py*</b> 파일을 만듭니다. 만든 renderer를 <b>*blog/authentication/api/views.py*</b> 파일에 import 합니다.

### Logging users in
10. 등록된 ID로 Login하는 기능을 만들기 위해 serializer를 먼저 만들어줍니다. 우선 <b>*blog/authentication/api/serializers.py*</b> 파일을 열어줍니다. 파일 내부에 있는 `RegistrationSerializer` 아래에 `LoginSerializer`를 만들어줍니다.

11. 이번엔 View를 수정해보도록 하겠습니다. <b>*blog/authentication/api/views.py*</b> 파일을 열어 `LoginAPIView`를 추가해줍니다. 추가한 후 <b>*blog/authentication/api/urls.py*</b> 파일을 열어 url을 설정합니다. 이후 postman에서 login이 정상적으로 이루어지는지 확인해봅니다.

----
>이 과정에서 post가 정상적으로 이루어지지 않는 경우 "non_field_errors" 라는 오류를 반환합니다. 여기에는 한 가지 문제가 있는데요.<br><br> 일반적으로 이 오류는 serializer가 유효성 검사를 실패하게 만든 모든 필드에 해당됩니다. 즉, 포괄적인 전체 error를 보여줄 때 설정됩니다. 우리가 만든 validator의 경우 validate_email과 같은 필드별 method 대신에 validate method 자체를 override했기 때문에 DRF는 오류에서 반환할 필드를 알지 못하기 때문에 특정 field error를 반환하지 못하고, "non_field_errors"를 반환한 것 입니다.<br><br> client는 보여지는 error(여기서는 "non_field_errors")를 사용해 표시하기 때문에 저는 간단하게 "non_field_errors"를 "error"로 변경하도록 하겠습니다. <br><br> 이 문제를 해결하기 위해 기본 error 처리를 override하도록 하겠습니다.
----

### Overriding EXCEPTION_HANDLER and NON_FIELD_ERRORS_KEY

12. DRF setting 중 하나가 EXCEPTION_HANDLER입니다. 기본 exception handler는 단순하게 오류 dictionary를 반환합니다. 저는 EXCEPTION_HANDLER를 override 하고, NON_FIELD_ERRORS_KEY를 앞서 언급한대로 override하도록 하겠습니다.<br><br> 우선 <b>*blog/core*</b> 라는 폴더를 만들고 그 안에 <b>*blog/core/exceptions.py*</b> 파일을 만들어 줍니다.

13. 그 다음으로 <b>*blog/setting/settings.py*</b> 파일에서 새로운 setting을 추가해줍니다. 그 다음 postman에서 email/password를 invalid data로 전송해봅니다. 그러면 다음과 같은 error message가 뜹니다.
```json
{
    "user": {
        "errors": {
            "error": [
                "A user with this email and password was not found."
            ]
        }
    }
}
```

14. 현재 user key 아래에 모든 errors key, error가 존재합니다. 이런 형태는 좋지 못하기 때문에 수정해줄 필요가 있습니다. Rendering할 때 error가 발생하면 user key에서 보여지는 것이 아닌 errors만 보여지도록 하겠습니다. <b>*blog/authentication/api/renderers.py*</b> 파일을 열어서 일부분 추가해줍니다. 그 다음 다시 login 과정에서 invalid data를 보내면 아래와 같은 결과를 얻을 수 있습니다.
```json
{
    "errors": {
        "error": [
            "A user with this email and password was not found."
        ]
    }
}
```