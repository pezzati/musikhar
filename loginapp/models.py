from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    male = 0
    female = 1
    GenderTypes = (
        (male, 'Male'),
        (female, 'Female')
    )
    mobile = models.CharField(max_length=20, null=True, blank=True)
    gender = models.IntegerField(choices=GenderTypes, default=male)
    age = models.IntegerField(default=0)
