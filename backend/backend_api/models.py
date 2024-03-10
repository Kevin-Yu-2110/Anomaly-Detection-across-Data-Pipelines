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

class Transaction(models.Model):
    username = models.ForeignKey(StandardUser, on_delete=models.CASCADE)
    payee_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time_of_transfer = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction from {self.username.username} to {self.payee_name} - ${self.amount}"

