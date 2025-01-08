from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, LoginSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, 200)

user_view_set = UserViewSet.as_view({
    "get": "list",
    "post": "create",
})

user_detail_view_set = UserViewSet.as_view({
    "get": "retrieve",
})

login_view_set = LoginView.as_view()