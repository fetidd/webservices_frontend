class InvalidFieldError(Exception):
    def __init__(self, field):
        super().__init__(f"{field} field is invalid")

