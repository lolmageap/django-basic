class NotFoundException(Exception):
    def __init__(self, message):
        self.message = message
        self.status_code = 404
    def __str__(self):
        return self.message