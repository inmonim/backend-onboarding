import factory.django
from django.contrib.auth.hashers import make_password

from users.models import User

from faker import Faker

faker = Faker(locale='ko-KR')

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    nickname = factory.LazyAttribute(lambda _: faker.name())
    username = factory.LazyAttribute(lambda _: faker.uuid4())
    password = factory.LazyAttribute(lambda _: make_password(faker.password()))