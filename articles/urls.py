from django.urls import path

from .views import article_list, aritcle_detail

urlpatterns = [
    path('', article_list),
    path('<int:article_id>', aritcle_detail),
]