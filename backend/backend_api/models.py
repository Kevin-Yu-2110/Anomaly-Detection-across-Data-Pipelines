import random
from django.contrib.auth.models import AbstractUser
from django.db import models

class StandardUser(AbstractUser):
    otp = models.CharField(max_length=6, null=True, blank=True)
    cc_num = models.IntegerField(unique=True)
    city = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    dob = models.DateField()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='standard_users_groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='standard_users_permissions'
    )
    
    # Method to Put a Random OTP in the CustomerUser table.
    def save(self, *args, **kwargs):
        # A six digit random number from the list will be saved in top field
        self.otp = ''.join(random.choices([str(i) for i in range(10)], k=6))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Transaction(models.Model):
    username = models.CharField(max_length=100)
    payee_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time_of_transfer = models.CharField(max_length=100)

    def __str__(self):
        return f"Transaction from {self.username} to {self.payee_name} - ${self.amount}\n"
