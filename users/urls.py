from django.urls import path, include

from users.views import UserViewSet

app_name = "users"

urlpatterns = [
    path("/", UserViewSet.as_view({
        "get": "list",
        "post": "create",
        })),
    
    path("<int:pk>/", UserViewSet.as_view({
        "get": "retrieve",
        })),
]