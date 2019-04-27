from django.contrib.auth import get_user_model
from factory import fuzzy, PostGenerationMethodCall
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    username = fuzzy.FuzzyText()
    password = PostGenerationMethodCall('set_password', 'password')

    class Meta:
        model = get_user_model()
