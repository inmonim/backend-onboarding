from rest_framework.serializers import ModelSerializer

from users.serializers import UserSerializer
from .models import Article, Category

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
        
class CategorySerializer(ModelSerializer):
    
    class Meta:
        model = Category
        fields = (
            'category_id',
            'category_name',
            'is_public',
            'created_user',
            'parent',
        )
        extra_kwargs = {
            "created_user" : {"read_only" : True}
        }