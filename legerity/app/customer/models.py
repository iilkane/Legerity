from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(
        'Email',
        max_length=255,
        unique=True,
        validators=[EmailValidator(message="Enter a valid email address.")],
        db_index=True
    )
    username = models.CharField(max_length=255, null=True)
    fullname = models.CharField(
        'Fullname', max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    objects = CustomUserManager()

    class Meta:
        indexes = [
            models.Index(fields=['email'], name='email_idx'),
            models.Index(fields=['is_active'], name='active_idx'),
            models.Index(fields=['is_staff'], name='staff_idx'),
        ]

    def __str__(self):
        return self.email
