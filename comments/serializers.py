from rest_framework import serializers

from .models import Comment
from users.serializers import UserNameSerializer
from articles.serializers import ArticleSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = UserNameSerializer(read_only=True)
    article = ArticleSerializer
    
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
        
    def to_representation(self, instance):
        # 기본적으로 부모 클래스의 to_representation 호출
        representation = super().to_representation(instance)
        
        # is_deleted가 1인 경우 comment 수정
        if instance.is_deleted:
            representation['comment'] = "삭제된 코멘트입니다"
        
        return representation

class CommentUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = (
            'comment',
            'is_deleted'
        )