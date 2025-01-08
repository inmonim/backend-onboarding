from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from .models import User
from .serializers import UserSerializer, UserPasswordChagneSerializer, LoginSerializer, UserProfileUpdateSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    
    def get_object(self):
        return User.objects.get(id=self.request.user.id)
    
    def get_serializer_class(self):
        if self.action == 'update':
            return UserProfileUpdateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def perform_destroy(self, instance):
        user = instance
        if not user:
            return Response("유저를 찾을 수 없음", 404)
        user.is_active = False
        user.save()
        

class UserPasswordChangeViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserPasswordChagneSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return User.objects.get(id=self.request.user.id)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        # 이미 로그인 한 사용자일 경우 반려
        if request.user.is_authenticated:
            return Response("이미 로그인한 사용자", 403)
        
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, 200)
    
    
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response('유효하지 않은 토큰', 401)
        except Exception as e:
            return Response('유효하지 않은 토큰', 401)


user_view_set = UserViewSet.as_view({
    "get": "retrieve",
    "post": "create",
    "delete": "destroy",
    "put" : "update",
})

user_password_change_view_set = UserPasswordChangeViewSet.as_view({
    "put" : "update"
})

login_view = LoginView.as_view()

logout_view = LogoutView.as_view()

refresh_view = TokenRefreshView.as_view()

class ProtectView(APIView):
    permission_classes = [IsAuthenticated]    
    def get(self, request):
        return Response("토큰 검증 성공", 200)
protect_view = ProtectView.as_view()