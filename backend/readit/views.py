
from .schema import Book, BookDB
from .models import BookMongo


def welcome(name=None) -> dict:
    if name is None:
        return {"message": "Welcome to API Star!"}
    return {"message": "Welcome to API Star, %s!" % name}


def view_book(book_id: int) -> BookDB:
    book = BookDB(name="Jack", author="Daniels", pages=66, content="Adult", id=15)
    return book


def save_book(book: Book) -> BookDB:
    book = BookMongo(title="Jack", author="Daniels", content=["page1", "page2"])
    book.save()
    return BookDB(
        id=str(book.id), title=book.title, author=book.author, content=book.content[0]
    )


def echo_book(book: Book) -> Book:
    return book
