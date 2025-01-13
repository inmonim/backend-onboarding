from rest_framework.serializers import ModelSerializer

from .models import Category

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