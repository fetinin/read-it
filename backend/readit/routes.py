from apistar import Route

from . import views

routes = [
    Route("/books", "GET", views.list_books),
    Route("/books", "POST", views.create_book),
    Route("/books/{book_id}", "GET", views.get_book),
    Route("/books/{book_id}", "PATCH", views.update_book),
]
