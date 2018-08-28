from apistar import http

from typing import List

from apistar.exceptions import NotFound

from . import schema
from .models import BookMongo


def welcome(name=None) -> dict:
    if name is None:
        return {"message": "Welcome to API Star!"}
    return {"message": f"Welcome to API Star, {name}!"}


def list_books(
    limit: http.QueryParam, offset: http.QueryParam
) -> List[schema.BookNoContent]:
    limit = int(limit) if limit is not None else 20
    offset = int(offset) if offset is not None else 0
    return [
        schema.BookNoContent(id=str(book.id), title=book.title, author=book.author)
        for book in BookMongo.objects.exclude("content")[offset:limit]
    ]


def get_book(book_id: str) -> schema.Book:
    book = BookMongo.get_by_id(book_id)
    if not book:
        raise NotFound()
    return schema.Book(
        id=str(book.id), title=book.title, author=book.author, content=book.content
    )


def update_book(book_id: str, book_fields: schema.BookFields, r_data: http.RequestData):
    book = BookMongo.get_by_id(book_id)
    if not book:
        raise NotFound()
    book.update(pk=book_id, **r_data)


def create_book(data: http.RequestData) -> schema.BookNoContent:
    book_db = BookMongo(title="Jack", author="Daniels", content=["page1", "page2"])
    return schema.BookNoContent(
        id=str(book_db.id), title=book_db.title, author=book_db.author
    )
