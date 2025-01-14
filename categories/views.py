from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Category
from .serializer import CategorySerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_user=self.request.user)
        return super().perform_create(serializer)
    
    def retrieve(self, request, *args, **kwargs):
        """
        특정 카테고리를 조회하거나 부모 또는 자식 카테고리를 반환합니다.

        - 입력값:
            - path param:
                - <int:pk> : 기준이 되는 지정 카테고리 id
            - query param:
                - type=parents: 부모 카테고리 목록 반환
                - type=children: 자식 카테고리 목록 반환
                - type 미지정: 현재 카테고리 반환
        
        - 반환값:
            - type에 따라 현재 카테고리 자신 또는 부모/자식 카테고리 목록 반환
        """
        query_type = request.query_params.get('type')
        if not kwargs.get('pk'):
            return Response("데이터가 없습니다", 404)
        category = self.get_object()
        many = query_type in ['parents', 'children']
        if query_type == 'parents':
            category = category.get_parent_categories()
        elif query_type == 'children':
            category = category.get_child_categories()
        serializer = self.get_serializer(category, many=many)
        return Response(serializer.data, 200)
    
    def perform_destroy(self, instance):
        """
        카테고리 삭제 시, 하위(자식) 카테고리를 삭제한 카테고리의 상위(부모) 카테고리의 자식 카테고리로 입양시킵니다.
        """
        user = self.request.user
        if instance.created_user and instance.created_user != user:
            raise PermissionDenied("삭제 권한이 없습니다.", 403)
        
        parent = instance.parent
        Category.objects.filter(parent_id=instance.category_id).update(parent=parent)
        
        instance.delete()

category_view_set = CategoryViewSet.as_view({
    'post' : 'create',
    'get' : 'retrieve',
    'delete' : 'destroy'
})