from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from time import gmtime, strftime


def get_avatar_directory_path(instance, filename):
    upload_time = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
    email_formatted = instance.email.replace('@', '_')
    return f'user_{email_formatted}/{upload_time}/{filename}'


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_male = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to=get_avatar_directory_path, null=True, default=None)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
