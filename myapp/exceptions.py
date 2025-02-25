from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.db.utils import IntegrityError


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, IntegrityError):
        response = Response(
            {
                "error": {
                    "code": 400,
                    "message": exc.args[1]
                }
            },
            status=400
        )

    if response is None:
        response.data = {
            "error": {
                "code": 500,
                "message": response.data.get('detail', 'Internal server error')
            }
        }

    return response
