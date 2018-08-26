from apistar import Route

from .views import welcome, view_book, echo_book, save_book

routes = [
    Route("/", "GET", welcome),
    Route("/books", "GET", view_book),
    Route("/books", "POST", save_book),
]
