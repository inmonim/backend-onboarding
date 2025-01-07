from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer, LoginSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class LoginViewSet(ModelViewSet):
    queryset = User.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        user.id = user.user_id
        
        refresh = RefreshToken.for_user(user=user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        return Response({
            'user_id' : user.user_id,
            'nickname' : user.nickname,
            'access_token' : access_token,
            'refresh_token' : refresh_token
        })

user_view_set = UserViewSet.as_view({
    "get": "list",
    "post": "create",
})

user_detail_view_set = UserViewSet.as_view({
    "get": "retrieve",
})

login_view_set = LoginViewSet.as_view({
    "post": "create"
})