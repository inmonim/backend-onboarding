from datetime import datetime
import pytz

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

tz = pytz.timezone('UTC')

class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'username', 'password', 'last_login']
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True},
            'last_login': {'read_only': True}}

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("존재하는 Username 입니다.", 409)
        return username

    def create(self, data):
        self.validate_username(data)
        data['password'] = make_password(data['password'])
        return super().create(data)

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname']
        
    def update(self, instance, validated_data):
        validated_data.pop('username', None)
        validated_data.pop('password', None)
        
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.save()
        return instance

class UserPasswordChagneSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password'] 

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

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
        
        res = {
            'refresh_token' : str(refresh),
            'access_token' : str(refresh.access_token),
            'nickname' : user.nickname,
        }
        
        user.last_login = datetime.now(tz=tz)
        user.save()
        
        return res