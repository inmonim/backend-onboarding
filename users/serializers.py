from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("존재하는 Username 입니다.", 409)
        return username

    def create(self, data):
        self.validate_username(data)
        data['password'] = make_password(data['password'])
        return super().create(data)

class LoginSerializer(TokenObtainPairSerializer):
        
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    refresh_token = serializers.CharField(read_only=True)
    access_token = serializers.CharField(read_only=True)
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("비밀번호 또는 아이디가 틀렸습니다.", 404)

        if not check_password(password, user.password):
            raise serializers.ValidationError("비밀번호 또는 아이디가 틀렸습니다.", 404)

        refresh = RefreshToken.for_user(user)
        data['refresh_token'] = str(refresh)
        data['access_token'] = str(refresh.access_token)
        return data