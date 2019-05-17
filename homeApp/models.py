from django.db import models
from django.contrib.auth.models import User
class UserSignUp(User):
    phonenumber=models.IntegerField()
    role=models.CharField(max_length=12)
    phonenumber_verified=models.BooleanField(default=False)
    email_verified=models.BooleanField(default=False)
    phonenumber_otp=models.IntegerField(null=True)
