import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


@pytest.fixture
def client():
    client = APIClient()
    yield client


@pytest.fixture
def user():
    user = get_user_model().objects.create_user(
        email='test@gmail.com',
        password='password',
        name='Name',
    )
    yield user
    user.delete()


class TestPublicUserApi:
    """Test user api public parts."""

    @pytest.mark.django_db
    def test_create_valis_user_is_successful(self, client: APIClient):
        """Test creating a user with valid payload is successful."""
        payload = {
            'email': 'user@mail.com',
            'password': 'password',
            'name': 'User Name',
        }
        response = client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(**response.data)

        assert response.status_code == status.HTTP_201_CREATED
        assert user.check_password(payload['password'])
        assert 'password' not in response.data

    @pytest.mark.django_db
    def test_user_alredy_exists(self, client: APIClient, user):
        """Test creating user already exists fails."""
        payload = {'email': 'test@gmail.com', 'password': 'password', 'name': 'Test'}
        response = client.post(CREATE_USER_URL, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_create_user_password_too_short(self, client: APIClient):
        """Test that password must be more that 5 characters."""
        payload = {'email': 'test@email.com', 'password': 'pw', 'name': 'Test'}
        response = client.post(CREATE_USER_URL, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not get_user_model().objects.filter(email='test@email.com').exists()

    @pytest.mark.django_db
    def test_create_token_for_user(self, client: APIClient, user):
        """Test getting token for an existed user."""
        payload = {'email': 'test@gmail.com', 'password': 'password'}
        response = client.post(TOKEN_URL, payload)

        assert 'token' in response.data
        assert response.status_code == status.HTTP_200_OK
