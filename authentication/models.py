import jwt
from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager
from core.models import TimestampedModel


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    # 만약 superuser도 반드시 갖고 있어야 하는 정보라면
    # REQUIRED_FIELDS에 넣어주도록 한다.
    REQUIRED_FIELDS = [
        'username',
        'birth_date',
        'phone_number'
        ]
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username
    
    @property
    def token(self):
        return self._generate_jwt_token()
    
    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        
        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        # decode 방법:
        # jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        return token