import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from models.IsolationForest import isolationForestModel
from models.XGBoost import XGBoostModel
from models.NeuralNetwork import NeuralNetworkModel

class StandardUser(AbstractUser):
    otp = models.CharField(max_length=6, null=True, blank=True)
    cc_num = models.IntegerField(unique=True)
    model_list = {}
    
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

    def get_models(self):
        self.model_list['IF'] = isolationForestModel(self.cc_num)
        self.model_list['XG'] = XGBoostModel(self.cc_num)
        self.model_list['NN'] = NeuralNetworkModel(self.cc_num)
    
    def call_model(self, model):
        return self.model_list[model]
    
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
    # fields required for model analysis and training
    is_flagged = models.BooleanField(default=False)
    anomalous = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Transaction from {self.cc_num} to {self.merchant} of type {self.category} and amount ${self.amount}\n"
