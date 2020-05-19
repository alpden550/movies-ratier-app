import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


@pytest.fixture(scope='module')
def superuser(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        superuser = get_user_model().objects.create_superuser(
            'admin@gmail.com',
            'password',
        )
        yield superuser


@pytest.fixture(scope='module')
def user(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user = get_user_model().objects.create_user(
            email='user@gmail.com',
            password='password',
            name='User',
        )
        yield user


@pytest.mark.django_db
def test_admin_available_for_superuser(superuser, client):
    """Test admin page is available for admins."""
    client.force_login(superuser)
    response = client.get('/admin/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_admin_forbiden_for_user(user, client):
    """Test admin page is not available for common users."""
    client.force_login(user)
    response = client.get('/admin/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_users_listed(superuser, user, client: Client):
    """Test that user are listed on the admin user page."""
    client.force_login(superuser)
    url = reverse('admin:api_user_changelist')
    response = client.get(url)

    assert response.status_code == 200
    assert user.email in response.rendered_content
    assert user.name in response.rendered_content


@pytest.mark.django_db
def test_userchange_page(superuser, user, client: Client):
    """Test that ther user edit page works."""
    client.force_login(superuser)
    url = reverse('admin:api_user_change', args=[user.id])
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_create_user_page(superuser, user, client: Client):
    """Test that creating user page works."""
    client.force_login(superuser)
    url = reverse('admin:api_user_add')
    response = client.get(url)

    assert response.status_code == 200
