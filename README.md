# First Day

1. Secret Key와 settings.py 파일을 분리하기 위해 <b>*secrests.json*</b>을 manage.py이 있는 project 상위 폴더에 만듭니다. Secret Key가 git에 upload할 때 포함되지 않도록 <b>*.gitignore*</b> 파일에 추가해줍니다.

2. User, 인증 관련 app을 만들기 위해 authentiction app을 만들어줍니다.
> django-admin startapp authentication


3. BaseUserManager를 만들기 위해 <b>*managers.py*</b> 파일을 authentication app 안에 만들어줍니다. 그 안에 class Usermanager를 정의합니다.

4. User 모델을 만들기 위해 <b>*authentication*</b> 폴더 내부에 있는 <b>*models.py*</b> 파일을 열어 수정해줍니다. 이 과정에서 <b>*settings.py*</b> 파일을 열어 AUTH_USER_MODEL을 설정해줍니다. 이후 제대로 작동하는지 super user를 생성해 확인합니다.
> python manage.py createsuperuser

> > 여기에서 django.db.utils.OperationalError: no such table: 오류가 발생했습니다.
> > 계속해서 createsuperuser를 실행하는 과정에서 db의 table을 지웠고, db.sqlite3 파일도
> > 지워버리면서 생긴 오류 같았습니다.
> > 이를 해결하기 위해 db.sqlite3 파일을 삭제하고, makemigrations을 우선 진행했습니다.
> > 다음으로
> > """ python manage.py migrate --run-syncdb """ 를 실행했습니다.
> > --run-syncdb 옵션은 migration을 하지 않고 앱에 대한 테이블을 만드는 것입니다.

5. superuser를 만들어 테스트가 끝나면 인증 부분을 수정해보도록 하겠습니다.


