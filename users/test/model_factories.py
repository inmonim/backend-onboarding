import factory.django

from users.models import User

from faker import Faker

faker = Faker(locale='ko-KR')

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    nickname = faker.name()
    username = faker.uuid4()
    password = faker.password()