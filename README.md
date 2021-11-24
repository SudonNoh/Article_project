# First Day

1. Secret Key와 settings.py 파일을 분리하기 위해 <b>*blog/secrests.json*</b>을 manage.py이 있는 project 상위 폴더에 만듭니다. Secret Key가 git에 upload할 때 포함되지 않도록 <b>*blog/.gitignore*</b> 파일에 추가해줍니다.

2. User, 인증 관련 app을 만들기 위해 authentiction app을 만들어줍니다.  
`django-admin startapp authentication`

3. BaseUserManager를 만들기 위해 <b>*blog/authentication/managers.py*</b> 파일을 authentication app 안에 만들어줍니다. 그 안에 class Usermanager를 정의합니다.

4. User 모델을 만들기 위해 <b>*blog/authentication/models.py*</b> 파일을 열어 수정해줍니다. 이 과정에서 <b>*blog/blog/settings.py*</b> 파일을 열어 AUTH_USER_MODEL을 설정해줍니다. 이후 제대로 작동하는지 super user를 생성해 확인합니다.  
`python manage.py createsuperuser`

----
> 여기에서 django.db.utils.OperationalError: no such table: 오류가 발생했는데요. createsuperuser를 실행하는 과정에서 db의 table을 지웠고, db.sqlite3 파일을 지워버리면서 생긴 오류 같았습니다.<br><br>이를 해결하기 위해 db.sqlite3 파일을 삭제하고, makemigrations을 우선 진행했습니다. 다음으로 `python manage.py migrate --run-syncdb` 를 실행했습니다. `--run-syncdb` 옵션은 migration을 하지 않고 앱에 대한 테이블을 만드는 것입니다.
----

> django shell에서 model들을 한번에 import 하고 사용하기 위해서 extensions를 설치해줄 필요가 있습니다. `pip install django-extensions` 으로 설치하고 터미널에 `python manage.py shell_plus`를 입력해주면 django와 관련된 모듈들이 import 되는 것을 확인할 수 있습니다.<br><br>이제 본인이 정의한 모델명으로 객체에 접근할 수 있습니다. 다음 명령어로 조회해보시기 바랍니다. `User.objects.all()` 여기서 User는 각자 정의한 모델명이므로 작성자에 따라 다를 수 있습니다.
> 
# Second Day

5. superuser를 만들어 테스트가 끝나면 인증 부분을 수정해보도록 하겠습니다. 먼저 <b>*blog/authentication/models.py*</b> 파일에 `@property`를 추가해 token을 만들기 위한 함수를 정의해줍니다. 제대로 적용이 되었는지 확인해봅니다. 위에서 언급한 `shell_plus`로 shell을 열고, `User.objects.first().token`으로 token이 잘 나오는지 확인합니다.
----
> pyjwt의 버전이 1.7.1 이하이면 decode를 적용시켜야 합니다. return 부분에 token.decode('utf-8')을 작성해줍니다. 
----

6. 이제, model에 등록하기 위한 serializer를 만들어보도록 하겠습니다. 우선 폴더를 하나 더 만들도록 하겠습니다. <b>*blog/authentication/api*</b> api 폴더를 만들어서 serializer 혹은 view, 각 앱에서 사용되는 modelue들을 모아두도록 하겠습니다. 다음으로 해당 폴더에 serializer를 만들도록 하겠습니다. <b>*blog/authentication/api/serializers.py*</b>

7. 

