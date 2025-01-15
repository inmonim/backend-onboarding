import factory.django
from faker import Faker

from ..models import Category
from users.test.model_factories import UserFactory

faker = Faker('ko-KR')

class CategoryFactory(factory.django.DjangoModelFactory):
    
    class Meta:
        model = Category
    
    category_name = faker.text(max_nb_chars=50)
    is_public = 1
    
    parent = None
    created_user = factory.SubFactory(UserFactory)