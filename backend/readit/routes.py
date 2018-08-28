from apistar import Route

from .views import get_book, list_books, update_book, welcome, create_book

routes = [
    Route("/", "GET", welcome),
    Route("/books", "GET", list_books),
    Route("/books", "POST", create_book),
    Route("/books/{book_id}", "GET", get_book),
    Route("/books/{book_id}", "PATCH", update_book),
]
