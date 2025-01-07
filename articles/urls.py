from django.urls import path

from .views import ArticleViewSet

urlpatterns = [
    path('', ArticleViewSet.as_view({
        'get' : 'list'
        })),
    
    path('<int:pk>', ArticleViewSet.as_view({
        'get' : 'retrieve'
    }))
]