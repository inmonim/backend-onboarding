from django.urls import path

from .views import article_view_set, aritcle_detail_view_set

app_name = "articles"

urlpatterns = [
    path('', article_view_set, name="article_crud"),
    path('<int:pk>/', aritcle_detail_view_set, name="article_detail"),
]