import pytest

from django.urls import reverse

from users.test.auth_client import authenticated_client, get_token, authenticated_client_and_user
from users.models import User
from users.test.model_factories import UserFactory

from categories.models import Category
from categories.test.model_factory import CategoryFactory
from .model_factory import ArticleFactory
from ..models import Article

@pytest.mark.django_db
class TestArticleView:
    def test_create_article(self, authenticated_client):
        article = ArticleFactory.build()
        
        url = reverse("articles:article_crud")
        response = authenticated_client.post(url, {
            "title" : article.title, "content" : article.content
            })
        
        assert response.status_code == 201
        article_id = response.data['article_id']
        
        retrieve_url = reverse("articles:article_detail", kwargs={"pk" : article_id})
        retrieve_response = authenticated_client.get(retrieve_url)
        assert response.data['title'] == retrieve_response.data['title']
    
    
    def test_retrieve_article(self, authenticated_client):
        article = ArticleFactory()
        url = reverse("articles:article_detail", kwargs={"pk" : article.article_id})
        
        # 공개 게시물에 대한 정상적인 요청
        retrieve_article = authenticated_client.get(url)
        assert retrieve_article.status_code == 200
        
        article.is_public = 0
        article.save()
        
        # 비공개 게시물에 대한 접근
        private_retrieve_article = authenticated_client.get(url)
        assert private_retrieve_article.status_code == 403
        
    # 아티클 삭제 테스트
    def test_delete_article(self, authenticated_client_and_user):
        client, user = authenticated_client_and_user
        article = ArticleFactory(author=user)
        
        url = reverse("articles:article_detail", kwargs={"pk" : article.article_id})
        
        response = client.delete(url)
        assert response.status_code == 204
        
        retrieve_response = client.get(url)
        assert retrieve_response.status_code == 410
        
        deleted_article = Article.objects.get(pk=article.article_id)
        assert deleted_article.is_deleted == 1
    
    # 아티클 수정 테스트
    def test_update_article(self, authenticated_client_and_user):
        client, user = authenticated_client_and_user
        
        article = ArticleFactory(author = user)
        
        url = reverse("articles:article_detail", kwargs={"pk" : article.article_id})
        
        response = client.put(url, {"title" : "update title", "content" : "update content"})
        
        assert response.status_code == 200
        
        update_response = client.get(url)

        assert article.title != update_response.data['title']
        assert article.content != update_response.data['content']
    
    # 카테고리 삭제로 인한 아티클의 변화 테스트
    def test_category_deleted_article(self, authenticated_client_and_user):
        client, user = authenticated_client_and_user
        article = ArticleFactory(author = user)
        
        category = article.category
        category.delete()
        
        after_article = Article.objects.get(pk=article.article_id)
        
        assert after_article.category == None
        
    # 아티클 리스트 페이지네이션 테스트
    def test_article_list_pagenation(self, authenticated_client_and_user):
        client, user = authenticated_client_and_user
        another_user = UserFactory()
        for i in range(25):
            if i >= 22:
                ArticleFactory(author=another_user, is_public=0)
            else:
                ArticleFactory(author=user)
        
        url = reverse("articles:article_crud")
        
        response = client.get(url)
        next_url = response.data['next']
        second_response = client.get(next_url)
        
        assert len(response.data['results']) == 20
        assert len(second_response.data['results']) == 2
    
    # 검색 쿼리 테스트
    def test_article_search(self, authenticated_client_and_user):
        client, user = authenticated_client_and_user
        
        parent_category = CategoryFactory()
        child_category = CategoryFactory(parent = parent_category)
        
        a = ArticleFactory(title="a", category = parent_category)
        b = ArticleFactory(title="b", category = child_category)
        c = ArticleFactory(title="c", author = user)
        d = ArticleFactory(title="d", is_public=0)
        e = ArticleFactory(title="e", is_deleted=1)
        
        url = reverse("articles:article_crud")
        query = {}
        first_response = client.get(url)
        
        assert len(first_response.data['results']) == 3
        
        query["category"] = parent_category.category_id
        second_response = client.get(url, query)
        
        assert len(second_response.data['results']) == 2
        
        query["category"] = child_category.category_id
        third_response = client.get(url, query)
        
        assert len(third_response.data['results']) == 1
        
        del query["category"]
        query["sort_by"] = "created_at"
        query["order"] = "desc"
        fourth_response = client.get(url, query)
        
        assert fourth_response.data['results'][2]['article_id'] == a.article_id
        
        query["order"] = "asc"
        query["q"] = "a"
        
        fifth_response = client.get(url, query)
        
        assert fifth_response.data['results'][0]['article_id'] == a.article_id