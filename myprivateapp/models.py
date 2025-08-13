from django.db import models
from django.contrib.sessions.models import Session

from django.conf import settings
from django.utils import timezone
from mysite import functions

class AppSession(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    secret = models.CharField(max_length=32, default=functions.get_secret())
    creation = models.DateTimeField(default=timezone.now)
    modification = models.DateTimeField(default=timezone.now)
    class Meta():
        db_table = 'S0001'

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)

    class Meta():
        db_table = 'V0001'

    def __str__(self):
        return self.name

class Member(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=60)
    surname = models.CharField(max_length=60)

    class Meta():
        db_table = 'V0002'

    def __str__(self):
        return (self.name + " " + self.surname)
    