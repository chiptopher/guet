class GuetError(Exception):
    pass


class InvalidInitialsError(GuetError):
    pass


class UnexpectedError(GuetError):
    def __init__(self, message: str):
        super().__init__(message)
