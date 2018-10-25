import factory
from factory import fuzzy
from factory.faker import faker
from factory.mongoengine import MongoEngineFactory
from readit.users.models import User
from readit.books.models import Book


class UserFactory(MongoEngineFactory):
    class Meta:
        model = User

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    avatar = ""
    external_id = factory.Sequence(lambda n: f"aba123cd{n}")
    auth_type = fuzzy.FuzzyChoice([x for x in range(3)])


class BookFactory(MongoEngineFactory):
    class Meta:
        model = Book

    title = factory.Faker("catch_phrase")
    pages = factory.LazyFunction(lambda: [text for text in faker.Faker().text()])
    author = factory.Faker("name")
    cover = ""
    page_active = 1
