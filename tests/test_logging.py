import pytest
from collections.abc import Callable
from django.test import TestCase
from django.test import override_settings

from common.logging import query_logging
from users.models import Users


@override_settings(DEBUG=True)
@query_logging
def test_select_all():
    return list(Users.objects.all())

@pytest.mark.django_db
class TestLogging(TestCase):
    def test_logging(self):
        test_select_all()
