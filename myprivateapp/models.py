from django.db import models
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

from django.conf import settings
from django.utils import timezone
from mysite import functions

class OrderType(models.TextChoices):
    NoOrder = '', 'Sin Orden'
    Ascending = '+', 'Ascendente'
    Descending = '-', 'Descendente'

class AppSession(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    secret = models.CharField(max_length=32, default=functions.get_secret())
    creation = models.DateTimeField(default=timezone.now)
    modification = models.DateTimeField(default=timezone.now)
    class Meta():
        db_table = 'appSession'

class AppEntity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    label = models.CharField(max_length=60)
    optionList = models.CharField(max_length=30)
    optionRecord = models.CharField(max_length=30)

    class Meta():
        db_table = 'appEntity'

    def __str__(self):
        return self.name

class AppEntityField(models.Model):
    id = models.AutoField(primary_key=True)
    entity = models.ForeignKey(AppEntity, on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    label = models.CharField(max_length=60)
    order = models.CharField(max_length=1, blank=True, choices=OrderType, default=OrderType.NoOrder)

    class Meta():
        db_table = 'appEntityField'

    def __str__(self):
        return self.entity.name + '/' + self.name

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)

    class Meta():
        db_table = 'company'

    def __str__(self):
        return self.name

class Member(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    user = models.ForeignKey(User, unique=True, on_delete=models.PROTECT, null=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=60)
    surname = models.CharField(max_length=60)

    class Meta():
        db_table = 'member'

    def __str__(self):
        return (self.name + " " + self.surname)
    