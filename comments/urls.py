from django.urls import path
from .views import CommentViewSet

urlpatterns = [
    path('<int:pk>/', CommentViewSet.as_view({
        'get' : 'retrieve'
        }))
]