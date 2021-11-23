from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    # 일반 user가 생성될 때 실행되는 코드
    def create_user(self, username, email, password=None):
        
        if username is None:
            raise TypeError('Users must have a username.')
        
        if email is None:
            raise TypeError('Users must hve an email address.')
        
        if password is None:
            raise TypeError('Users must have a password.')
        
        user = self.model(
            username = username, 
            email=self.normalize_email(email)
            )
        user.set_password(password)
        user.save()
        
        return user
    
    # Super user가 생성될 때 실행되는 코드
    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')
        
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        return user