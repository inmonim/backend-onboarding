import pytest
from django.urls import reverse

from ..models import Comment
from .model_factory import CommentFactory
from articles.test.model_factory import ArticleFactory
from users.test.model_factories import UserFactory

from users.test.auth_client import get_token, authenticated_client_and_user


@pytest.fixture
def article():
    return ArticleFactory()


@pytest.mark.django_db
class TestCommentView:
    
    # 코멘트 생성 Test
    def test_comment_create(self, authenticated_client_and_user, article):
        client, user = authenticated_client_and_user
        
        url = reverse('comments:comment_crud', kwargs={'article_id' : article.article_id})
        
        response = client.post(url, {
            "comment" : "test", "article" : article.article_id, "author" : user.id
            })
        
        assert response.status_code == 201
        
        comment = Comment.objects.get(pk=response.data['comment_id'])
        
        assert comment.comment == "test"
    
    # 코멘트 read
    def test_comment_retrieve(self, authenticated_client_and_user, article):
        client, user = authenticated_client_and_user
        
        for _ in range(5):
            comment = CommentFactory(comment="수정 전 코멘트", article = article, author = user)
        
        url = reverse('comments:comment_crud', kwargs={'article_id' : article.article_id})
        
        response = client.get(url)
        
        assert response.data[-1]['author']['id'] == user.id
        assert response.data[-1]['comment'] == comment.comment
    
    # 코멘트 수정
    def test_comment_update(self, authenticated_client_and_user, article):
        client, user = authenticated_client_and_user
        
        comment = CommentFactory(article = article, author = user)
        
        url = reverse('comments:comment_detail', kwargs={
            'article_id' : article.article_id,
            'pk' : comment.comment_id
            })
        
        response = client.put(url, {
            'comment_id' : comment.comment_id, 'comment' : '수정된 코멘트'
            })
        
        another_user = UserFactory()
        another_user_comment = CommentFactory(article=article, author=another_user)
        forbidden_url = reverse('comments:comment_detail', kwargs={
            'article_id' : article.article_id,
            'pk' : another_user_comment.comment_id
            })
        
        forbbiden_response = client.put(forbidden_url, {
            'comment_id' : comment.comment_id, 'comment' : '다른 사람의 수정 요청'
        })
        
        changed_comment = Comment.objects.get(pk=comment.comment_id)
        
        
        assert comment.comment_id == changed_comment.comment_id and (
            comment.comment != changed_comment.comment
        )
        
        assert forbbiden_response.status_code == 403
    
    # 코멘트 삭제
    def test_comment_delete(self, authenticated_client_and_user, article):
        
        client, user = authenticated_client_and_user
        
        comment = CommentFactory(article=article, author=user)
        
        url = reverse('comments:comment_detail', kwargs={
            "article_id" : article.article_id,
            "pk" : comment.comment_id
        })
        
        response = client.delete(url)
        
        assert response.status_code == 204
        
        # 삭제한 코멘트 내용을 변형하여 받기
        deleted_url = reverse('comments:comment_crud', kwargs={
            "article_id" : article.article_id
        })
        
        deleted_resposne = client.get(deleted_url)
        
        assert deleted_resposne.data['comment'][0] == "삭제된 코멘트입니다"
        
        # 다른 유저의 코멘트 삭제 시도
        another_user = UserFactory()
        
        another_comment = CommentFactory(article=article, author=another_user)
        
        another_url = reverse('comments:comment_detail', kwargs={
            "article_id" : article.article_id,
            "pk" : another_comment.comment_id
        })
        
        forbbiden_response = client.delete(another_url)
        
        assert forbbiden_response.status_code == 403