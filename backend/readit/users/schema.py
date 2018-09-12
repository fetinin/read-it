from apistar import types, validators


class User(types.Type):
    id = validators.String()
    name = validators.String()
    surname = validators.String()
