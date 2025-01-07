from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password, check_password

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
        
    class Meta:
        model = User
        fields = ['username', 'password']
    
    def validate(self, data):
        username, password = data['username'], data['password']
        user = User.objects.filter(username=username)
        if user:
            if not check_password(password, user[0].password):
                raise serializers.ValidationError("비밀번호 또는 아이디가 틀렸습니다.", 404)
        else:
            raise serializers.ValidationError("비밀번호 또는 아이디가 틀렸습니다.", 404)
        return user[0]