from rest_framework import serializers

from .models import Comment
from users.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    
    class Meta:
        model = Comment
        fields = (
            'comment_id',
            'comment',
            'is_deleted',
        )