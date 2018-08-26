from apistar import types, validators, exceptions


class HasId(types.Type):
    id = validators.String()


class Book(types.Type):
    title = validators.String(description="Book title.")
    author = validators.String(description="Book author.", max_length=100)
    content = validators.String(description="Book content.")


class BookDB(HasId, Book):
    pass
