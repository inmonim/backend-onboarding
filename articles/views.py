from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q

from .models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer

class ArticlePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 40

class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.select_related('category', 'author')
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
    
    def get_permissions(self):
        if self.action in ['list']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """
        게시글 검색 쿼리를 설정하는 메서드입니다.
        
        category, author(user)에 대해서는 추가 쿼리가 발생할 우려가 있기에,
        기본적으로 select_related로 가져옵니다.
        이를 해제할 경우, serializer 변환 과정에서 모든 카테고리 row마다 쿼리를 발생시킵니다.
        
        유저를 파악한 뒤, is_deleted, is_public을 검사합니다.
        
        다음은 쿼리 파라미터 값에 따라 추가적인 질의를 진행하여 값을 반환합니다.
        
        Query Params:
            q : 질의문, 포함관계를 검색하며, title, content에 대해 수행합니다.
            sort_by : [created_at, title]을 선택하여 정렬할 수 있습니다. 기본값은 생성일입니다.
            order : [asc, desc]
            category : [category_id] 자신 및 자식 카테고리에 대항하는 아티클을 검색합니다. 기본값은 없습니다.
        """
        queryset = super().get_queryset()
        
        queryset = queryset.filter(is_deleted=0)
        
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.filter(Q(is_public=1) | Q(author=user))
        else:
            queryset = queryset.filter(is_public=1)
        
        sort_by = self.request.query_params.get('sort_by', 'created_at')
        order = self.request.query_params.get('order', 'asc')
        category = self.request.query_params.get('category', None)
        search_query = self.request.query_params.get('q', None)
        
        if sort_by not in ['created_at', 'title']:
            sort_by = 'created_at'
        if order == 'desc':
            sort_by = f'-{sort_by}'
            
        queryset = queryset.order_by(sort_by)
        
        if category:
            children = Category.objects.get(pk=category).get_child_categories()
            children_keys = [c.category_id for c in children]
            queryset = queryset.filter(category__in=children_keys)
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )
        
        return queryset
        
        
    def perform_create(self, serializer):
        category = serializer.validated_data.get('category')
        is_public = serializer.validated_data.get('is_public')
        
        if category:
            if not (category.is_public or (category.created_user.id == self.request.user.id)):
                return Response("해당 카테고리에 대한 접근 권한이 없음", 403)

        if is_public is None:
            if category:
                is_public = category.is_public
            else:
                is_public = 1

        serializer.save(author=self.request.user, is_public=is_public)
        

    def list(self, request, *args, **kwargs):
        """        
        쿼리 파라미터로 들어온 page에 따라 페이지네이션 범위를 정합니다.

        기본 페이지 사이즈는 20입니다.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class ArticleDetailViewSet(ModelViewSet):
    queryset = Article.objects.select_related('author', 'category')
    serializer_class = ArticleSerializer
    
    def get_permissions(self):
        if self.action == 'retrieve':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def perform_destroy(self, instance):
        if self.request.user.id != instance.author.id:
            return Response("해당 게시물에 대한 접근 권한 없음", 403)
        instance.is_deleted = 1
        instance.save()


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
        """
        카테고리 삭제 시, 하위(자식) 카테고리를 삭제한 카테고리의 상위(부모) 카테고리의 자식 카테고리로 입양시킵니다.
        """
        user = self.request.user
        if instance.created_user != user:
            return Response("삭제 권한이 없습니다.", 403)
        
        # 레거시 코드
        # ===============
        # children = Category.objects.filter(parent_id=instance.category_id)
        # parent = instance.parent
        
        # for child in children:
        #     child.parent = parent
        #     child.save()
        # ===============
        parent = instance.parent
        Category.objects.filter(parent_id=instance.category_id).update(parent=parent)
        
        instance.delete()


aritcle_detail_view_set = ArticleDetailViewSet.as_view({
    'get' : 'retrieve',
    'delete' : 'destroy'
})

article_view_set = ArticleViewSet.as_view({
    'post' : 'create',
    'get' : 'list'
})

category_view_set = CategoryViewSet.as_view({
    'post' : 'create',
    'get' : 'retrieve',
    'delete' : 'destroy'
})