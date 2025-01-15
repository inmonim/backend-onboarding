from django.urls import path
from .views import comment, comment_detail

app_name = "comments"

urlpatterns = [
    path('', comment, name="comment_crud"),
    path('<int:pk>/', comment_detail, name="comment_detail")
]