import pytest
from django.urls import reverse

from .model_factory import CategoryFactory
from articles.test.model_factory import ArticleFactory
from users.test.model_factories import UserFactory

from articles.models import Article
from categories.models import Category

from users.test.auth_client import get_token, authenticated_client_and_user

@pytest.mark.django_db
class TestCategoryView:
    
    # 카테고리 생성
    def test_category_create(self, authenticated_client_and_user):
        client, user = authenticated_client_and_user
        
        url = reverse("categories:category_crud")
        
        first_response = client.post(url, {
            "category_name" : "Test1",
        })
        
        assert first_response.status_code == 201
        
        parent_id = first_response.data['category_id']
        
        second_response = client.post(url, {
            "category_name" : "Test2",
            "is_public" : 1,
            "parent" : parent_id,
        })
        
        assert second_response.status_code == 201
        assert parent_id == second_response.data['parent']
    
    # 카테고리 삭제 시, 자식 카테고리를 부모 카테고리로 상속시키기
    def test_category_deleted_parent_inherbit(self, authenticated_client_and_user):
        client, user = authenticated_client_and_user
        grand_parent_category = CategoryFactory()
        parent_category = CategoryFactory(
            created_user = user, parent = grand_parent_category)
        child_category = CategoryFactory(
            created_user = user, parent = parent_category)
        
        url = reverse("categories:category_detail", kwargs={"pk": parent_category.category_id})
        
        response = client.delete(url)
        
        assert response.status_code == 204
        
        child = Category.objects.get(pk=child_category.category_id)
        
        assert child.parent == grand_parent_category
    
    # 카테고리 삭제 및 삭제 권한 확인
    def test_category_delete(self, authenticated_client_and_user):
        client, user = authenticated_client_and_user
        another_user = UserFactory()
        
        category = CategoryFactory(created_user = user)
        another_category = CategoryFactory(created_user = another_user)
        
        url = reverse("categories:category_detail",
                      kwargs={"pk": category.category_id})
        
        response = client.delete(url)
        
        assert response.status_code == 204
        assert not Category.objects.filter(pk=category.category_id).exists()
        
        url = reverse("categories:category_detail",
                      kwargs={"pk": another_category.category_id})
        
        forbidden_response = client.delete(url)
        
        assert forbidden_response.status_code == 403
        assert Category.objects.filter(pk=another_category.category_id).exists()
    
    
    # 카테고리 부모 또는 자식 포함 검색 테스트
    def test_category_retrieve(self, authenticated_client_and_user):
        client, user = authenticated_client_and_user
        
        grand_parent_category = CategoryFactory()
        parent_category = CategoryFactory(parent = grand_parent_category)
        child_category_1 = CategoryFactory(parent = parent_category)
        child_category_2 = CategoryFactory(parent = parent_category)
        child_category_3 = CategoryFactory(parent = parent_category)
        
        children_url = reverse("categories:category_detail",
                      kwargs={"pk" : parent_category.category_id})
        
        children_response = client.get(children_url, {"type" : "children"})
        
        assert len(children_response.data) == 4
        assert children_response.data[-1]['parent'] == parent_category.category_id
        
        parents_url = reverse("categories:category_detail",
                              kwargs={"pk" : child_category_1.category_id})
        
        parents_response = client.get(parents_url, {"type": "parents"})
        
        assert len(parents_response.data) == 3
        assert parents_response.data[-1]['parent'] == None