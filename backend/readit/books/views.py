import base64

from apistar import http

from typing import List

from apistar.exceptions import NotFound
from .convertor import Converter
from . import schema
from .models import Book
from readit.components import User


def list_books(
    limit: http.QueryParam, offset: http.QueryParam
) -> List[schema.BookNoContent]:
    limit = int(limit) if limit is not None else 20
    offset = int(offset) if offset is not None else 0
    return [
        schema.BookNoContent(
            id=str(book.id), title=book.title, author=book.author, cover=book.cover
        )
        for book in Book.objects.exclude("pages").order_by("created_date")[offset:limit]
    ]


def get_book(book_id: str, user: User) -> schema.Book:
    book = Book.get_by_id(book_id)
    if not book:
        raise NotFound()
    return schema.Book(
        id=str(book.id),
        title=book.title,
        author=book.author,
        pages=book.pages,
        cover=book.cover,
        page_active=book.page_active,
    )


def update_book(book_id: str, book_fields: schema.BookFields, r_data: http.RequestData):
    book = Book.get_by_id(book_id)
    if not book:
        raise NotFound()
    book.update(pk=book_id, **r_data)


def create_book(book_data: schema.BookWithFile) -> schema.HasID:
    import datetime

    now = datetime.datetime.now()
    print(now)
    pages = Converter(book_data.format).convert(base64.b64decode(book_data.file))
    print("Took %s", datetime.datetime.now() - now)
    book = Book(
        title=book_data.title,
        author=book_data.author,
        pages=pages,
        cover=book_data.cover,
    )
    book.save()
    return schema.HasID(id=str(book.id))


def delete_book(book_id: str):
    book = Book.get_by_id(book_id)
    if not book:
        raise NotFound()
    book.delete()
