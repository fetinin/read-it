from molten import Route

from . import views

routes = [
    Route("/books", views.list_books, "GET"),
    Route("/books", views.create_book, "POST"),
    Route("/books/{book_id}", views.get_book, "GET"),
    Route("/books/{book_id}", views.update_book, "PATCH"),
    Route("/books/{book_id}", views.delete_book, "DELETE"),
]
