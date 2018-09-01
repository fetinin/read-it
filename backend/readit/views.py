import base64

from apistar import http

from typing import List

from apistar.exceptions import NotFound

from .convertor import Converter
from . import schema
from .models import Book


def list_books(
    limit: http.QueryParam, offset: http.QueryParam
) -> List[schema.BookNoContent]:
    limit = int(limit) if limit is not None else 20
    offset = int(offset) if offset is not None else 0
    return [
        schema.BookNoContent(
            id=str(book.id), title=book.title, author=book.author, cover=book.cover
        )
        for book in Book.objects.exclude("content")[offset:limit]
    ]


def get_book(book_id: str) -> schema.Book:
    book = Book.get_by_id(book_id)
    if not book:
        raise NotFound()
    return schema.Book(
        id=str(book.id),
        title=book.title,
        author=book.author,
        content=book.content,
        cover=book.cover,
    )


def update_book(book_id: str, book_fields: schema.BookFields, r_data: http.RequestData):
    book = Book.get_by_id(book_id)
    if not book:
        raise NotFound()
    book.update(pk=book_id, **r_data)


def create_book(book_data: schema.BookWithFile) -> schema.HasID:
    pages = Converter(book_data.format).convert(base64.b64decode(book_data.file))
    book = Book(
        title=book_data.title,
        author=book_data.author,
        content=pages,
        cover=book_data.cover,
    )
    book.save()
    return schema.HasID(id=book.id)
