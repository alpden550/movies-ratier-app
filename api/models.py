from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


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


class Movie(models.Model):
    """Model to represent movie oblect."""

    title = models.CharField('Movie Title', max_length=100, unique=True, db_index=True)
    description = models.TextField('Movie Description', max_length=500, blank=True)

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def __str__(self):
        return self.title
