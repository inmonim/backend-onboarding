from faker import Faker
import factory.django

from ..models import Article

from users.test.model_factories import UserFactory
from categories.test.model_factory import CategoryFactory

faker = Faker(locale='ko-KR')

class ArticleFactory(factory.django.DjangoModelFactory):
    
    class Meta:
        model = Article
        
    title = faker.sentence()
    content = faker.paragraph()
    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    is_public = 1