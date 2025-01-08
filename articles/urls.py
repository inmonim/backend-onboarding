from django.urls import path

from .views import article_list, aritcle_detail, category_view_set

urlpatterns = [
    path('', article_list),
    path('<int:article_id>', aritcle_detail),
    path('category', category_view_set),
    path('category/<int:pk>', category_view_set),    
]