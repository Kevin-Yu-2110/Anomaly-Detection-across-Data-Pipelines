from django.contrib.auth.models import AbstractUser
from django.db import models

class StandardUser(AbstractUser):
    accountType = models.CharField(max_length=100)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='standard_users_groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='standard_users_permissions'
    )

    def __str__(self):
        return self.username
