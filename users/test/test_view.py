import pytest
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.test import APIClient
from django.urls import reverse

from .model_factories import UserFactory
from .auth_client import get_token, authenticated_client

# 로그인 테스트
@pytest.mark.django_db
class TestUsersView:
    
    # 로그인 테스트
    def test_login(self, authenticated_client, get_token):
        
        auth_header = authenticated_client._credentials.get("HTTP_AUTHORIZATION")
        assert auth_header == f"Bearer {get_token['access_token']}"
        
        url = reverse("users:user_crud")
        response = authenticated_client.get(url)
        
        assert response.status_code == 200

    # 유저 생성 테스트
    @pytest.mark.django_db
    def test_user_created(self, client):
        nickname = "테스터"
        username = "test_username"
        password = "test_user_password123!@"
        
        url = reverse("users:user_crud")
        
        response = client.post(url, {'nickname':nickname, 'username':username, 'password':password})
        
        assert response.status_code == 201
        assert response.data['last_login'] == None
        
        duplicate_response = client.post(url, {'nickname': nickname, 'username': username, 'password': password})
        
        assert duplicate_response.data['username'][0].code == 'unique'

    # 유저 수정 테스트
    @pytest.mark.django_db
    def test_user_update(self, authenticated_client):
        url = reverse("users:user_crud")
        
        response = authenticated_client.put(url, {"nickname" : "변경한 닉네임"})
        
        assert response.status_code == 200
        assert response.data['nickname'] == "변경한 닉네임"
        
        user_response = authenticated_client.get(url)
        
        assert user_response.data['nickname'] == response.data['nickname']

    # 유저 삭제 테스트
    @pytest.mark.django_db
    def test_user_delete(self, authenticated_client):
        url = reverse("users:user_crud")
        
        response = authenticated_client.delete(url)
        
        assert response.status_code == 204
        
        user_response = authenticated_client.get(url)
        
        assert user_response.status_code == 401
        assert user_response.data['detail'] == "비활성화된 사용자입니다"

    # 로그아웃 테스트
    @pytest.mark.django_db
    def test_logout(self, client, get_token):
        url = reverse("users:user_logout")
        refresh_token = get_token['refresh_token']
        
        response = client.post(url, {"refresh" : refresh_token})
        is_success = False
        try:
            BlacklistedToken.objects.filter(token__jti=RefreshToken(refresh_token).get("jti"))
        except TokenError as e:
            is_success = True
        
        assert is_success
        assert response.status_code == 200

    # 비밀번호 변경 테스트
    @pytest.mark.django_db
    def test_change_password(self, ):
        old_password = "oldpassword123"
        new_password = "newpassword321"
        
        client = APIClient()
        user = UserFactory(password=make_password(old_password))
        
        login_url = reverse("users:user_login")
        token_response = client.post(login_url, {"username" : user.username, "password" : old_password})
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_response.data['access_token']}")
        
        url = reverse("users:change_password")
        client.put(url, {"old_password" : old_password, "new_password" : new_password})
        client.credentials()
        new_token_response = client.post(login_url, {"username":user.username, "password":new_password})
        
        assert new_token_response.status_code == 200
        