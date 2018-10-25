from functools import partial
from typing import Tuple

import mongoengine
import pytest
from molten import testing

from app import app
from readit import components
from tests.stubs_factory import BookFactory, UserFactory


@pytest.fixture(scope="session", autouse=True)
def test_db():
    mongoengine.register_connection(alias="core", host="mongomock://localhost")


@pytest.fixture(scope="session")
def client():
    return testing.TestClient(app)


@pytest.fixture
def user():
    user = UserFactory.create()
    yield user
    user.delete()


@pytest.fixture
def book(user):
    book = BookFactory(owner_id=user.id)
    yield book
    book.delete()


@pytest.fixture
def books_factory(user):
    books = []

    def make_books(amount=1) -> Tuple[BookFactory]:
        nonlocal books
        for _ in range(amount):
            book = BookFactory(owner_id=user.id)
            books.append(book)
        return tuple(books)

    yield make_books

    for book in books:
        book.delete()


@pytest.fixture
def authorized_client(user):
    class AuthClient(testing.TestClient):
        pass

    def add_auth_header(req):
        req.headers["authentication"] = components.User(str(user.id)).as_token()
        return req

    client = AuthClient(app)
    client.request = partial(client.request, auth=add_auth_header)
    return client
