from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['id','fullname','email','password']

    def validate_email(self,value):
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError('')
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email is already in use')
        return value
    
    def create(self, validated_data):
        password=validated_data.pop('password')
        user=User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class LoginSerializer(serializers.Serializer):
    password=password = serializers.CharField(write_only=True)
    email=serializers.EmailField()

    def validate(self, attrs):
        email= attrs.get('email')
        password= attrs.get('password')
        user= authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError('Invalid email or password')
        
        refresh= RefreshToken.for_user(user)
        return{
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'fullname': user.fullname
            }
        }