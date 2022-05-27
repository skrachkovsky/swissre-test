class BaseError(Exception):
    ...


class BadOperation(BaseError):
    ...


class ValidationError(BaseError):
    ...
