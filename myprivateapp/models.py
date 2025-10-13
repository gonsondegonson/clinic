from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from colorfield.fields import ColorField

from django.utils import timezone
import datetime

from myapp import functions
from myapp.models import Company, AppEntityOption

class Color(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=25)
    value = ColorField()
    modification = models.DateTimeField(default=datetime.datetime.now)

    class Meta():
        db_table = 'color'
        indexes = [models.Index(fields=['company','name']),]
        unique_together = [('company','name'),]

    def optKey(self):
        return ('idColor=' + str(self.id))

    def RGB(self):
        hex_color = self.value.lstrip('#').lstrip(";")
        rgb_color = str(tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)))
        return (rgb_color)

    def __str__(self):
        return (self.name)

class Letter(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=25)
    value = models.CharField(max_length=25)
    modification = models.DateTimeField(default=timezone.now)

    class Meta():
        db_table = 'letter'
        indexes = [models.Index(fields=['company','name']),]
        unique_together = [('company','name'),]

    def optKey(self):
        return ('idLetter=' + str(self.id))

    def __str__(self):
        return (self.name)

class Icon(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=25)
    value = models.CharField(max_length=25)
    modification = models.DateTimeField(default=timezone.now)

    class Meta():
        db_table = 'icon'
        indexes = [models.Index(fields=['company','name']),]
        unique_together = [('company','name'),]

    def optKey(self):
        return ('idIcon=' + str(self.id))

    def __str__(self):
        return (self.name)

class AppMenuItem(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    label = models.CharField(max_length=60)
    icon = models.ForeignKey(Icon, on_delete=models.PROTECT)
    option = models.ForeignKey(AppEntityOption, on_delete=models.PROTECT, blank=True, null=True)

    class Meta():
        db_table = 'appMenuItem'

    def optKey(self):
        return ('idMenu=' + str(self.id))

    def __str__(self):
        return self.label + (' (' + self.option.option + ')' if self.option != None else '')

class AppMenuTree(models.Model):
    parent = models.ForeignKey(AppMenuItem, on_delete=models.PROTECT, related_name='parent')
    child = models.ForeignKey(AppMenuItem, on_delete=models.PROTECT, related_name='child')
    order = models.IntegerField(default=0)

    class Meta():
        db_table = 'appMenuTree'

    def optKey(self):
        return ('idMenuTree=' + str(self.id) + '|idParent=' + str(self.parent.id) + '|idChild=' + str(self.child.id))

    def __str__(self):
        return self.parent.label + '/' + self.child.label
