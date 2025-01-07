from django.urls import path
from .views import comment, comment_detail

urlpatterns = [
    path('', comment),
    path('<int:comment_id>', comment_detail)
]