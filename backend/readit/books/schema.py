from typing import List, Optional

from molten import Field, schema


@schema
class WithID:
    id: Optional[str] = Field(response_only=True)


@schema
class BookNoContent(WithID):
    title: str = Field(description="Book title.")
    author: str = Field(description="Book author.", max_length=100, strip_spaces=True)
    cover: str = Field(description="Book cover image as base64.")


@schema
class BookWithFile(BookNoContent):
    file: str = Field(description="Book content as base64 string.", request_only=True)
    # todo: add choices? It's better to validate supported formats here
    # (https://trello.com/c/uOiV0slb)
    format: str = Field(description="Book format.", request_only=True)


@schema
class BookContent(BookNoContent):
    pages: List[str] = Field(description="Book content.", response_only=True)
    page_active: Optional[int] = Field(
        description="Current active page number.", response_only=True
    )
