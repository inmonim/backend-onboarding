import pytest
from django.contrib.auth.hashers import check_password
from django.test import Client
from django.urls import reverse

from .model_factories import UserFactory
from ..models import User

@pytest.fixture
def get_token():
    client = Client()
    create_user = UserFactory()
    url = reverse("users:user_login")
    response = client.post(
        url, {"username" : create_user.username, "password" : create_user.password}
    )
    token = response.data["access_token"]
    print(token)
    return token

@pytest.mark.django_db
class TestUsersView:
    def test_login_api_view(self, client):
        user = UserFactory()
        url = reverse("users:user_login")
        response = client.post(url, {"username" : user.username, "password" : user.password})
        
        assert "access_token" in response.data
        