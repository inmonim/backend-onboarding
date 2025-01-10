from django.urls import path

from .views import article_view_set, aritcle_detail_view_set, category_view_set

urlpatterns = [
    path('', article_view_set),
    path('<int:pk>/', aritcle_detail_view_set),
    path('category/', category_view_set),
    path('category/<int:pk>/', category_view_set),    
]