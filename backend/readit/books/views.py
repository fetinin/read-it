import base64
from typing import List

from molten import RequestData, http, HTTP_404
from molten.errors import HTTPError

from readit.components import User
from . import schema
from .convertor import Converter
from .models import Book


def list_books(user: User) -> List[schema.BookNoContent]:
    books = Book.objects(owner_id=user.id).exclude("pages").order_by("created_date")
    return [
        schema.BookNoContent(
            id=str(book.id), title=book.title, author=book.author, cover=book.cover
        )
        for book in books
    ]


def get_book(book_id: str, user: User) -> schema.BookContent:
    book = Book.get_user_book(book_id, owner_id=user.id)
    if not book:
        raise HTTPError(http.HTTP_404)
    return schema.BookContent(
        id=str(book.id),
        title=book.title,
        author=book.author,
        pages=book.pages,
        cover=book.cover,
        page_active=book.page_active,
    )


def update_book(book_id: str, r_data: RequestData, user: User):
    book = Book.get_user_book(book_id, owner_id=user.id)
    if not book:
        raise HTTPError(http.HTTP_404)
    book.update(pk=book_id, **r_data)


def create_book(book_data: schema.BookWithFile, user: User) -> schema.WithID:
    pages = Converter(book_data.format).convert(base64.b64decode(book_data.file))
    book = Book(
        title=book_data.title,
        author=book_data.author,
        pages=pages,
        cover=book_data.cover,
        owner_id=user.id,
    )
    book.save()
    return schema.WithID(id=str(book.id))


def delete_book(book_id: str, user: User):
    book = Book.get_user_book(book_id, user.id)
    if not book:
        raise HTTPError(HTTP_404)
    book.delete()
