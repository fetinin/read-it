from molten import schema


@schema
class User:
    id: str
    name: str
    surname: str
    avatar: str
