from rest_framework.serializers import ModelSerializer

from users.serializers import UserSerializer
from .models import Article, Category
from users.models import User

class UserNameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname']

class CategoryNameSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'category_name']

class ArticleSerializer(ModelSerializer):
    category = CategoryNameSerializer()
    author = UserNameSerializer()
    
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