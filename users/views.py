from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer

from django.contrib.auth.hashers import make_password

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        hashed_password = make_password(request.data['password'])
        request.data['password'] = hashed_password
        return super().create(request, *args, **kwargs)
    

user_view_api = UserViewSet.as_view({
    "get": "list",
    "post": "create",
})

user_detail_view_api = UserViewSet.as_view({
    "get": "retrieve",
})