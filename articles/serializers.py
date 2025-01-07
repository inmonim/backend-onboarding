from rest_framework.serializers import ModelSerializer

from users.serializers import UserSerializer
from .models import Article

class ArticleSerializer(ModelSerializer):
    author = UserSerializer()
    
    class Meta:
        model = Article
        fields = (
            'article_id',
            'title',
            'content',
            'is_public',
            'is_deleted',
            'created_at',
            'updated_at',
            'category_id',
        )