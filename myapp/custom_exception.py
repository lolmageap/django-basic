class NotFoundException(Exception):
    def __init__(self, message, *args):
        super().__init__(*args)
        self.message = message
        self.status_code = 404
    def __str__(self):
        return self.message

class AuthenticationFailedException(Exception):
    def __init__(self, message, *args):
        super().__init__(*args)
        self.message = message
        self.status_code = 401
    def __str__(self):
        return self.message
