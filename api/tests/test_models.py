import pytest
from django.contrib.auth import get_user_model

from api import models


@pytest.mark.django_db
def test_create_user_successful():
    """test creating a new user is successful."""
    email = 'test@gmail.com'
    password = 'password'
    user = get_user_model().objects.create_user(
        email=email,
        password=password,
    )

    assert user.email == email
    assert user.check_password(password)


@pytest.mark.django_db
def test_user_email_normalized():
    """Test the email for new user is normalized"""
    email = 'test@GMAiL.COm'
    user = get_user_model().objects.create_user(email, 'password')

    assert user.email == email.lower()


@pytest.mark.django_db
def test_create_user_invalid_email():
    """Test creating user without email raise error."""
    with pytest.raises(ValueError):
        get_user_model().objects.create_user(None, 'password')


@pytest.mark.django_db
def test_create_superuser():
    """Test creating a new superuser"""
    user = get_user_model().objects.create_superuser('test.gmail.com', 'password')

    assert user.is_staff
    assert user.is_superuser


@pytest.mark.django_db
def test_movie_str():
    """Test movie string representation."""
    movie = models.Movie.objects.create(title='New Movie')

    assert movie.title == str(movie)


@pytest.mark.django_db
def test_rating_str():
    """Test rating string representation."""
    user = get_user_model().objects.create_user('test@gmail.com')
    movie = models.Movie.objects.create(title='New Movie')
    rating = models.Rating.objects.create(
        stars=5,
        movie=movie,
        user=user,
    )

    assert str(rating) == f'Rating {rating.pk} for {movie}'
