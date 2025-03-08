from dataclasses import asdict

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.request import SignUpRequest, SignUpRequestV2

@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_signup(api_client):
    request_data = {
        "name": "cheolhee",
        "email": "ekxk1234@naver.com",
        "password": "String1234!",
        "password_confirm": "String1234!"
    }
    response = api_client.post(reverse('sign-up'), request_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_signup_v2(api_client):
    request = SignUpRequest(
        name="cheolhee",
        email="ekxk1234@naver.com",
        password="String1234!",
        password_confirm="String1234!"
    )

    response = api_client.post(reverse('sign-up-v2'), asdict(request), format='json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_signup_v3(api_client):
    request = SignUpRequestV2(
        name="cheolhee",
        email="ekxk1234@naver.com",
        password="String1234!",
        password_confirm="String1234!"
    )

    response = api_client.post(reverse('sign-up-v2'), request.model_dump(), format='json')
    assert response.status_code == status.HTTP_201_CREATED
