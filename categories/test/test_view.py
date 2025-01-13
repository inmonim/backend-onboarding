import pytest
from django.urls import reverse

from .model_factory import CategoryFactory
from articles.test.model_factory import ArticleFactory

from articles.models import Article
from categories.models import Category

from users.test.auth_client import get_token, authenticated_client_and_user

@pytest.mark.django_db
class TestCategoryView:
    
    def test_category_deleted_article_inherbit(self, authenticated_client_and_user):
        client, user = authenticated_client_and_user
        grand_parent_category = CategoryFactory.create()
        parent_category = CategoryFactory.create(parent = grand_parent_category)
        child_category = CategoryFactory.create(parent = parent_category)
        
        url = reverse("categories:category_detail", kwargs={"pk": parent_category.category_id})
        
        par_id = parent_category.category_id
        
        client.delete(url)
        
        category = Category.objects.get(pk=child_category.category_id)
        child_id = category.parent.category_id
        
        assert par_id != child_id