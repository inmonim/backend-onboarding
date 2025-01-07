from rest_framework.viewsets import ModelViewSet

from .models import Article
from .serializers import ArticleSerializer

class ArticleViewSet(ModelViewSet):
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

article_list = ArticleViewSet.as_view({'get' : 'list'})
aritcle_detail = ArticleViewSet.as_view({'get' : 'retrieve'})