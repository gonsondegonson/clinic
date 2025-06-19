from django.conf import settings
from django.db import models
from django.utils import timezone

class Company(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class Member(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=60)
    surname = models.CharField(max_length=60)

    def __str__(self):
        return (self.surname + ", " + self.name)
    