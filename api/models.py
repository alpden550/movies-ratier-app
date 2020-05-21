from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


class UserManager(BaseUserManager):
    """Custom user manager for custom user."""

    def create_user(self, email, password=None, **kwargs):
        """Create and save a new user."""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **kwargs):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model support using email instead of username."""

    USERNAME_FIELD = 'email'

    email = models.EmailField('Email', max_length=254, unique=True, db_index=True)
    name = models.CharField('Name', max_length=255, blank=True)
    is_active = models.BooleanField('Is active', default=True)
    is_staff = models.BooleanField('Is staff', default=False)

    objects = UserManager()

    def __str__(self):
        return self.name


class Movie(models.Model):
    """Model to represent movie oblect."""

    title = models.CharField('Movie Title', max_length=100, unique=True, db_index=True)
    description = models.TextField('Movie Description', max_length=500, blank=True)
    poster = models.ImageField(
        'Movie Poster',
        upload_to='uploads/%Y/%m/%d/',
        blank=True,
    )

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def __str__(self):
        return self.title

    def average_rating(self):
        """Calculate average rating for a movie."""
        return Movie.objects.filter(id=self.id).aggregate(average_rating=Avg('ratings__stars'))


class Rating(models.Model):
    """Rating for a movie object."""

    stars = models.PositiveIntegerField(
        'Stars',
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    movie = models.ForeignKey(
        'api.Movie',
        verbose_name='Rating',
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='User',
        on_delete=models.CASCADE,
        related_name='ratings',
    )

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        unique_together = ['movie', 'user']
        index_together = ['movie', 'user']

    def __str__(self):
        return f'Rating {self.pk} for {self.movie}'
