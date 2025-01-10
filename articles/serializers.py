from rest_framework.serializers import ModelSerializer

from users.serializers import UserNameSerializer
from .models import Article, Category

class CategoryNameSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'category_name']

class ArticleSerializer(ModelSerializer):
    category = CategoryNameSerializer(read_only=True)
    author = UserNameSerializer(read_only=True)
    
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
            'author' : {"read_only" : True},
            'category' : {"read_only" : True}
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