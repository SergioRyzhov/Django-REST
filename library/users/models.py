from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class Profile(AbstractBaseUser):
    username = models.CharField(max_length=64, default='noname')
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
