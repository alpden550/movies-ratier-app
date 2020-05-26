import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
USER_URL = reverse('user:update')


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

    @pytest.mark.django_db
    def test_create_token_invalid_credentials(self, client: APIClient, user):
        """Test that token isn't created if invalid credentials given."""
        payload = {'email': 'test@gmail.com', 'password': 'wrong'}
        response = client.post(TOKEN_URL, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'token' not in response.data

    @pytest.mark.django_db
    def test_create_token_without_user(self, client: APIClient):
        """Test that token isn't created if user doesn't exist."""
        payload = {'email': 'test@test.com', 'password': 'password'}
        response = client.post(TOKEN_URL, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'token' not in response.data

    @pytest.mark.django_db
    def test_create_token_with_missed_fields(self, client: APIClient):
        """Test that email and password are required."""
        payload = {'email': 'email', 'password': ''}
        response = client.post(TOKEN_URL, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'token' not in response.data

    def test_retrieve_user_unathorized(self, client: APIClient):
        """Test that authentication is required to change user info."""
        response = client.get(USER_URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestPrivateUserApi:
    """Test user api that required authentication."""

    @pytest.mark.django_db
    def test_retrieve_user_successful(self, client: APIClient, user):
        client.force_authenticate(user)
        response = client.get(USER_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'email': 'test@gmail.com', 'name': 'Name'}

    @pytest.mark.django_db
    def test_method_post_not_allowed(self, client: APIClient, user):
        """Test that POST method is not allowed in the profile."""
        client.force_authenticate(user)
        response = client.post(USER_URL, data={})

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    @pytest.mark.django_db
    def test_updating_user_profile(self, client: APIClient, user):
        """Test that an authenticated user can update profile."""
        client.force_authenticate(user)
        payload = {'name': 'New Full Name', 'password': 'new_password'}
        response = client.patch(USER_URL, payload)

        user.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert user.name == payload['name']
        assert user.check_password(payload['password'])
