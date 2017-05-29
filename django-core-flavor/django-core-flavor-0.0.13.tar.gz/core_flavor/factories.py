import factory

from django.conf import settings
from django.utils.timezone import utc


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker('email')
    username = factory.Faker('name')
    password = factory.PostGenerationMethodCall('set_password', 'password')

    last_login = factory.Faker(
        'date_time_between',
        start_date='-1y',
        tzinfo=utc)

    class Meta:
        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('email',)


class AdminFactory(UserFactory):
    is_staff = True
