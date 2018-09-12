from apistar import Route

from . import views

routes = [
    Route("/auth/{auth_service_name}", "GET", views.auth_user),
    Route("/users/{user_id}", "GET", views.get_user),
]
