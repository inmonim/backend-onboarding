import factory.django
from faker import Faker

from ..models import Comment
from articles.test.model_factory import ArticleFactory
from users.test.model_factories import UserFactory

faker = Faker('ko-KR')


class CommentFactory(factory.django.DjangoModelFactory):
    
    class Meta:
        model = Comment
    
    comment = faker.text()
    is_deleted = 0
    article = factory.SubFactory(ArticleFactory)
    author = factory.SubFactory(UserFactory)