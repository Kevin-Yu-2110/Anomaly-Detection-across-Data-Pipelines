import random
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

    otp = models.CharField( #Referenced from https://stackoverflow.com/questions/71856923/django-password-reset-with-email-using-rest-apis
    max_length=6, null=True, blank=True)
    
    # Method to Put a Random OTP in the CustomerUser table.
    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]  # Use of list comprehension
        code_items_for_otp = []

        for i in range(6):
            num = random.choice(number_list)
            code_items_for_otp.append(num)

        code_string = "".join(str(item)
                                        for item in code_items_for_otp)  # list comprehension again
        # A six digit random number from the list will be saved in top field
        self.otp = code_string
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Transaction(models.Model):
    username = models.CharField(max_length=100)
    payee_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time_of_transfer = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction from {self.username.username} to {self.payee_name} - ${self.amount}"
