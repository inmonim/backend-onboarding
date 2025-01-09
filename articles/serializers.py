from rest_framework.serializers import ModelSerializer

from users.serializers import UserSerializer
from .models import Article, Category

class ArticleSerializer(ModelSerializer):
    
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
            'category',
            'author',
        )
        extra_kwargs = {
            'author' : {"read_only" : True}
        }
        
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