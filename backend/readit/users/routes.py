from molten import Route

from . import views

routes = [
    Route("/auth/{auth_service_name}", views.auth_user, "GET"),
    Route("/users/{user_id}", views.get_user, "GET"),
]
