import logging

from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.db.utils import IntegrityError
from .custom_exception import NotFoundException, AuthenticationFailedException


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailedException):
        logging.log(logging.WARN, exc)
        response = Response(
            {
                "message": exc.message
            },
            status=exc.status_code,
        )

    if isinstance(exc, NotFoundException):
        response = Response(
            {
                "message": exc.message
            },
            status=exc.status_code,
        )

    if isinstance(exc, IntegrityError):
        response = Response(
            {
                "message": exc.args[1]
            },
            status=400,
        )

    if response is None:
        logging.log(logging.ERROR, exc)
        response = Response(
            {
                "message": "Internal server error"
            },
            status=500,
        )

    return response
