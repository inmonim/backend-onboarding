from django.urls import path

from .views import category_view_set

app_name = "categories"

urlpatterns = [
    path('category/', category_view_set, name="category_crud"),
    path('category/<int:pk>/', category_view_set, name="category_detail"),
]
