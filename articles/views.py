from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer

class ArticleViewSet(ModelViewSet):
    
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


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
                - type=parent: 부모 카테고리 목록 반환
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
        
        if instance.created_user != self.request.user:
            return Response("삭제 권한이 없습니다.", 403)
        
        children = Category.objects.filter(parent_id=instance.category_id)
        parent = instance.parent
        
        for child in children:
            child.parent = parent
            child.save()
        
        instance.delete()
        # return super().perform_destroy(instance)




article_list = ArticleViewSet.as_view({
    'get' : 'list'
})

aritcle_detail = ArticleViewSet.as_view({
    'get' : 'retrieve'
})

category_view_set = CategoryViewSet.as_view({
    'post' : 'create',
    'get' : 'retrieve',
    'delete' : 'destroy'
})