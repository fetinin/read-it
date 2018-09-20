from apistar import types, validators


class HasID(types.Type):
    id = validators.String()


class BookFields(types.Type):
    title = validators.String(description="Book title.", allow_null=True)
    author = validators.String(
        description="Book author.", max_length=100, allow_null=True
    )
    cover = validators.String(
        description="Book cover image as base64.", allow_null=True
    )
    page_active = validators.Integer(
        description="Current active page number.", allow_null=True, default=1
    )


class BookContent(types.Type):
    pages = validators.Array(description="Book content.", items=validators.String())


class BookNoContent(HasID, BookFields):
    """A book without content"""


class Book(HasID, BookFields, BookContent):
    """Full book data from DB"""


class BookWithFile(BookFields):
    """Create book schema"""

    file = validators.String(description="Book content as base64 string.")
    format = validators.String(description="Book format.")
