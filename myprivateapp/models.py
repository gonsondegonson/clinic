from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

from django.utils import timezone


class OptionType(models.TextChoices):
    View   = 'view',   'Consultar'
    Add    = 'add',    'Añadir'
    Change = 'change', 'Modificar'
    Delete = 'delete', 'Suprimir'
    Export = 'export', 'Exportar'
    Exec   = 'exec',   'Ejecutar'

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
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=60)
    surname = models.CharField(max_length=60)

    class Meta():
        db_table = 'member'

    def __str__(self):
        return (self.name + " " + self.surname)

class Color(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=25)
    value = models.CharField(max_length=10)

    class Meta():
        db_table = 'color'

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

    class Meta():
        db_table = 'letter'

    def __str__(self):
        return (self.name)

class Icon(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=25)
    value = models.CharField(max_length=25)

    class Meta():
        db_table = 'icon'

    def __str__(self):
        return (self.name)
    
class AppSession(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    secret = models.CharField(max_length=44)
    creation = models.DateTimeField(default=timezone.now)
    modification = models.DateTimeField(default=timezone.now)

    class Meta():
        db_table = 'appSession'

class AppEntity(models.Model):
    id = models.AutoField(primary_key=True)
    app = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=30)
    label = models.CharField(max_length=60)

    class Meta():
        db_table = 'appEntity'

    def hasPerm(self, user, type=OptionType):
        return user.has_perm(self.app + "." + type + "_" + self.name)

    def __str__(self):
        return self.label

class AppEntityField(models.Model):
    id = models.AutoField(primary_key=True)
    entity = models.ForeignKey(AppEntity, on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    label = models.CharField(max_length=60)
    order = models.BooleanField(default=False)

    class Meta():
        db_table = 'appEntityField'

    def __str__(self):
        return self.entity.label + '/' + self.label

class AppEntityOption(models.Model):
    id = models.AutoField(primary_key=True)
    entity = models.ForeignKey(AppEntity, on_delete=models.PROTECT)
    type = models.CharField(max_length=10, choices=OptionType, default=OptionType.View,)
    option = models.CharField(max_length=60, unique=True)

    class Meta():
        db_table = 'appEntityOption'

    def hasPerm(self, user):
        return user.has_perm(self.entity.app + "." + self.type + "_" + self.entity.name)

    def __str__(self):
        return self.option

class AppMenuItem(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    label = models.CharField(max_length=60)
    icon = models.ForeignKey(Icon, on_delete=models.PROTECT)
    option = models.ForeignKey(AppEntityOption, on_delete=models.PROTECT, blank=True, null=True)

    class Meta():
        db_table = 'appMenuItem'

    def __str__(self):
        return self.label

class AppMenuTree(models.Model):
    parent = models.ForeignKey(AppMenuItem, on_delete=models.PROTECT, related_name='parent')
    child = models.ForeignKey(AppMenuItem, on_delete=models.PROTECT, related_name='child')
    order = models.IntegerField(default=0)

    class Meta():
        db_table = 'appMenuTree'

    def __str__(self):
        return self.parent.label + '/' + self.child.label
