from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Comment
from .serializers import CommentSerializer, CommentUpdateSerializer

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        if self.action in ['list']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentDetailViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == "update":
            return CommentUpdateSerializer
        return CommentSerializer
    
    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionDenied("수정 권한이 없음")
        serializer.save()
        
    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied("삭제 권한이 없음")
        
        instance.is_deleted = 1
        instance.save()
        
    
comment = CommentViewSet.as_view({
    'get' : 'list',
    'post' : 'create',
})

comment_detail = CommentDetailViewSet.as_view({
    'put' : 'update',
    'delete' : 'destroy'
})