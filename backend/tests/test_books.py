from unittest import mock

from app import app


def test_create_book_validation_test(authorized_client):
    response = authorized_client.post(
        app.reverse_uri("create_book"), json={"invalid": "field"}
    )
    assert response.status_code == 400


def test_create_book(authorized_client):
    body = {
        "title": "Code Complete",
        "author": "Steve McConel",
        "cover": "data:image/png:base64,data:image/png;base64,iVBORw0KGgo...",
        "file": "iVBORw0KGgoweartQW==",
        "format": "pdf",
    }
    with mock.patch("readit.books.views.Converter") as converter_mock:
        converter_mock.return_value.convert.return_value = ["1", "2", "3"]

        response = authorized_client.post(app.reverse_uri("create_book"), json=body)
    assert response.status_code == 200
    assert "id" in response.json()


def test_list_books(authorized_client, books_factory):
    books = books_factory(3)
    resp = authorized_client.get(app.reverse_uri("list_books"))
    assert resp.status_code == 200
    assert len(resp.json()) == len(books)


def test_create_book_invalid_format(authorized_client):
    body = {
        "title": "Code Complete",
        "author": "Steve McConel",
        "cover": "data:image/png:base64,data:image/png;base64,iVBORw0KGgo...",
        "file": "iVBORw0KGgoweartQW==",
        "format": "jpg",
    }
    response = authorized_client.post(app.reverse_uri("create_book"), json=body)
    assert response.status_code == 400
    assert "errors" in response.json()
    assert "format" in response.json()["errors"]
