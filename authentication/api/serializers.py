from django.contrib.auth import authenticate
from rest_framework import serializers

from authentication.models import User



class RegistrationSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        max_length = 128,
        min_length = 8,
        # write_only = True로 설정되면 인스턴스를 updating, creating 할 때에는
        # 사용되지만 serializing 할 때는 포함되지 않는다.
        write_only = True
    )
    
    token = serializers.CharField(
        max_length=255, 
        read_only=True
    )
    
    # serialize 할 부분을 설정한다.
    class Meta:
        model = User
        fields = [
            'email', 
            'username', 
            'password', 
            'birth_date', 
            'phone_number', 
            'token'
        ]
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    
    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        
        if email is None:
            raise serializers.ValidationError(
                'An Email address is required to log in.'
            )
        
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        
        # 'authenticate' 는 user의 email과 password의 조합을 확인하는데 사용된다.
        # 만약 email과 password 조합을 DB에서 확인한 결과가 없으면 None을 반환한다.
        user = authenticate(username=email, password=password)
        
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }

# ModelSerializer는 create method도 제공한다. 하지만 이미 RegistrationSerializer에서
# User를 생성하는 기능을 만들었기 때문에 UserSerializer에서는 update하는 기능만을
# 추가해 주었다.
class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""
    
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    
    class Meta:
        model = User
        fields = [
            'email', 
            'username', 
            'password', 
            'birth_date', 
            'phone_number', 
            'token'
        ]
        
        # 'read_only_fields' 옵션은 각 field에 'read_only=True'와 같은 역할을 한다.
        # 위에서 명시한 password field의 'write_only=True'와 같은 형태로 명시하는 것을
        # 말한다.
        # 그럼 왜 여기서 'read_only=True'로 명시하는 field를 지정하지 않고 
        # 'read_only_fields'로 지정한 걸까?
        # 그 이유는 해당 필드에 대해 따로 명시할 부분이 없기 때문이다. 
        # password field를 위에서 'write_only=True'로 명시한 이유는 우리가 password field를
        # 입력을 받을 때, 'max_length', 'min_length' 프로퍼티(property)를 지정해야 했기 
        # 때문이다. token field에 대해서는 그럴 이유가 없기 때문에 'read_only_fields'로
        # 따로 작성했다.
        read_only_fields = ('token',)
        
    def update(self, instance, validated_data):
        """Performs an update on a User."""
        
        # setattr(object, name, value) : object에 존재하는 속성의 값을 바꾸거나, 새로운
        # 속성값을 부여한다.
        
        # password는 다른 field들과 달리 'setattr'로 처리되면 안된다.
        # 그 이유는 django에서 password를 hashing, salting 처리하는 함수를 제공하기 때문이다.
        # 보안 측면에서 이 부분이 굉장히 중요하기 때문에 'setattr'로 처리하는 것이 아닌
        # 다른 방식으로 처리해야 한다. 따라서 for문이 시작되기 전에 'validated_data' 
        # dictionary에서 password를 제거해야 한다.
        
        password = validated_data.pop('password', None)
        '''
            print('validated_data:  ', validated_data)
            수정된 내용의 data가 들어옴
            validated_data:   {'birth_date': datetime.date(1992, 1, 1), 'phone_number': '010-1234-1234'}
        '''
        
        for (key, value) in validated_data.items():
            # password를 제외한 key들은 계속 남겨두고, value 값만 현재 'User'의 
            # instance로 바꿔주도록 한다.
            '''
                print('instance:  ', instance)
                instance:   test@blog.com
            '''
            setattr(instance, key, value)
            
        if password is not None:
            # '.set_password()' method는 위에서 언급한 대로 보안적인 측면에서 안전하게
            # password를 변경해준다.
            instance.set_password(password)

        # 이제 수정된 instance를 DB에 저장이 되도록 save해준다. 
        # 'set_password()'가 model에 저장하는 기능을 하지는 않습니다.
        instance.save()
        
        return instance