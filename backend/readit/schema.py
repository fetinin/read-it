from apistar import types, validators


class HasID(types.Type):
    id = validators.String()


class BookFields(types.Type):
    title = validators.String(description="Book title.", allow_null=True)
    author = validators.String(
        description="Book author.", max_length=100, allow_null=True
    )


class BookContent(types.Type):
    content = validators.Array(description="Book content.", items=validators.String())


class BookNoContent(HasID, BookFields):
    """A book without content"""


class Book(HasID, BookFields, BookContent):
    """Full book data from DB"""


class BookWithFile(BookFields):
    """Create book schema"""

    file = validators.String(description="Book content as binary string.")
    format = validators.String(description="Book format.")
