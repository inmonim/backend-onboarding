import pytest
from rest_framework.test import APIClient
from django.contrib.auth.hashers import make_password
from django.urls import reverse

from ..models import User
from .model_factories import UserFactory

@pytest.fixture
def get_token():
    password = "testpassword123!@"
    client = APIClient()
    user = UserFactory(password=make_password(password))
    url = reverse("users:user_login")
    response = client.post(url, {'username' : user.username, "password" : password})
    assert response.status_code == 200
    
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access_token']}")
    dobule_login_response = client.post(url, {'username' : user.username, "password" : password})
    
    assert dobule_login_response.status_code == 403
    
    return response.data

@pytest.fixture
def authenticated_client(get_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access_token']}")
    return client

@pytest.fixture
def authenticated_client_and_user(get_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token['access_token']}")
    user = User.objects.get(pk=get_token['id'])
    return client, user