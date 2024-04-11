import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from models.IsolationForest import isolationForestModel

class StandardUser(AbstractUser):
    otp = models.CharField(max_length=6, null=True, blank=True)
    cc_num = models.IntegerField(unique=True)
    isolation_forest_model = isolationForestModel()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='standard_users_groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='standard_users_permissions'
    )

    def save(self, *args, **kwargs):
        # StandardUser is assigned six-digit random number upon creation
        self.otp = ''.join(random.choices([str(i) for i in range(10)], k=6))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Transaction(models.Model):
    # auth user fields
    uploading_user = models.CharField(max_length=100)
    # model feature fields: 'trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'city', 'job', 'dob'
    time_of_transfer = models.CharField(max_length=100)
    cc_num = models.IntegerField()
    merchant = models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    amt = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    dob = models.DateField()
    # fields storing result of model analysis
    anomalous = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Transaction from {self.username} to {self.payee_name} of type {self.category} and amount ${self.amount}\n"

# Model identifcal to Transaction model, except with anomalous corrected
class FeedbackTransaction(Transaction):
    def __str__(self):
        return f"Feedback Transaction from {self.username} to {self.payee_name} with ' anomalous {self.anomalous}' prediction flagged"