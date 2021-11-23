# First Day

1. Secret Key와 settings.py 파일을 분리하기 위해 <b>*secrests.json*</b>을 manage.py이 있는 project 상위 폴더에 만듭니다. Secret Key가 git에 upload할 때 포함되지 않도록 <b>*.gitignore*</b> 파일에 추가해줍니다.

2. User, 인증 관련 app을 만들기 위해 authentiction app을 만들어줍니다.
> django-admin startapp authentication


3. BaseUserManager를 만들기 위해 <b>*managers.py*</b> 파일을 authentication app 안에 만들어줍니다. 그 안에 class Usermanager를 정의합니다.

4. User 모델을 만들기 위해 <b>*authentication*</b> 폴더 내부에 있는 <b>*models.py*</b> 파일을 열어 수정해줍니다.
