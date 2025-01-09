from typing import TypeVar
from django.db import models, connection

from common.models import BaseModel

T = TypeVar('T', bound="Category")

class Category(BaseModel):
    
    category_id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=50, null=False)
    is_public = models.SmallIntegerField(default=1, null=False)
    
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='children'
                               )
    created_user = models.ForeignKey('users.User',
                                    on_delete=models.DO_NOTHING,
                                    null=False,
                                    blank=False,
                                    related_name='created_category'
                                    )
    
    class Meta:
        db_table = 'categories'

    def get_parent_categories(self) -> tuple[T]:
        """
        특정 카테고리의 모든 상위 카테고리를 검색하여 반환합니다.
        Django ORM을 통해 재귀적으로 쿼리를 보내는 것보다, 네이티브 쿼리를 활용하는 것이 네트워크 I/O를 줄일 수 있습니다.
        
        호출한 인스턴스 객체의 정보를 토대로 쿼리를 실행하므로, 인자가 필요없습니다.
        
        - Args:
            - None
            
        - Return:
            - List[Category]
        """
        query = """
            WITH RECURSIVE parent_tree AS (
                SELECT category_id, category_name, parent_id, is_public, created_user_id
                FROM categories
                WHERE category_id = %s
                UNION ALL
                SELECT c.category_id, c.category_name, c.parent_id, c.is_public, c.created_user_id
                FROM categories c
                INNER JOIN parent_tree p ON c.category_id = p.parent_id
            )
            SELECT * FROM parent_tree
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [self.category_id])
            rows = cursor.fetchall()
            return self.convert_to_model_instances(rows)

    def get_child_categories(self) -> tuple[T]:
        query = """
            WITH RECURSIVE child_tree AS (
                SELECT category_id, category_name, parent_id, is_public, created_user_id
                FROM categories
                WHERE category_id = %s
                UNION ALL
                SELECT c.category_id, c.category_name, c.parent_id, c.is_public, c.created_user_id
                FROM categories c
                INNER JOIN child_tree p ON c.parent_id = p.category_id
            )
            SELECT * FROM child_tree;
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [self.category_id])
            rows = cursor.fetchall()
            return self.convert_to_model_instances(rows)
    
    def convert_to_model_instances(self, raw_data : tuple[dict]) -> list[T]:
        """
        native query로 반환받은 tuple[dict] 형태의 객체를 Category 인스턴스로 변환하여 반환합니다.
        
        - Args:
            tuple[dict]
        
        - Return:
            list[Category]
        """
        instances = []
        for row in raw_data:
            instance = Category(
                category_id=row[0],
                category_name=row[1],
                parent_id=row[2],
                is_public=row[3],
                created_user_id=row[4]
            )
            instances.append(instance)
        return instances
    
class Article(BaseModel):
    
    article_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)
    content = models.TextField()
    is_public = models.SmallIntegerField(null=False, default=1)
    is_deleted = models.SmallIntegerField(null=False, default=0)
    
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='articles')
    
    class Meta:
        db_table = 'articles'