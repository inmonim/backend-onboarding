from rest_framework import serializers

from .models import Comment
from users.serializers import UserNameSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = UserNameSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = (
            'comment_id',
            'comment',
            'article',
            'is_deleted',
            'created_at',
            'updated_at',
            'author',
        )

class CommentUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = (
            'comment',
            'is_deleted'
        )