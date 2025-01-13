from django.urls import path

from .views import category_view_set

urlpatterns = [
    path('category/', category_view_set),
    path('category/<int:pk>/', category_view_set),
]
