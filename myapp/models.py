from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

from django.utils import timezone

from myapp.functions import getUrlEncoded, getFormLabels

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

    def getUrl(self, secret):
        # Add 'Edit record' URL for one record on the Entity
        self.record.url = type('url', (), {
            'edit': getUrlEncoded((self.opt.edit + '|idOperation=Edit|' + self.record.optKey()), secret) if (self.auth.add or self.auth.change or self.auth.delete) else None,
        })

    def getUrls(self, secret, formFunction=None):
        if formFunction != None:
            # Build 'add record form' for modal maintenance
            self.form = getFormLabels(self, formFunction())

        for record in self.records:
            # Add 'Edit record' URL for each record on the Entity
            record.url = type('url', (), {
                'edit': getUrlEncoded((self.opt.edit + '|idOperation=Edit|' + record.optKey()), secret) if (self.auth.add or self.auth.change or self.auth.delete) else None,
            })
            if formFunction != None:
                # Build 'edit record form' for modal maintenance
                record.form = getFormLabels(self, formFunction(instance=record))


    def getTreeUrls(self, pathList, secret):
        recordCount = 0
        self.selList = pathList
        for record in self.records:
            recordCount += 1
            # Add 'List sub-records', 'Edit record' and 'Delete record' URLs for each record on the Entity Tree
            record.url = type('url', (), {
                  'list': None if not self.auth.view else getUrlEncoded((self.opt.list + '|idOperation=List|idParent=' + str(record.child.id) + '|pathList=' + pathList), secret),
                  'edit': None if not self.auth.add else getUrlEncoded((self.opt.edit + '|idOperation=Edit|' + record.optKey() + '|pathList=' + pathList), secret),
                'delete': None if not self.auth.delete else getUrlEncoded((self.opt.edit + '|idOperation=Delete|' + record.optKey() + '|pathList=' + pathList), secret),
                    'up': None if recordCount == 1 else getUrlEncoded((self.opt.edit + '|idOperation=SwitchUp|' + record.optKey() + '|pathList=' + pathList), secret),
                  'down': None if recordCount == self.records.count() else getUrlEncoded((self.opt.edit + '|idOperation=SwitchDown|' + record.optKey() + '|pathList=' + pathList), secret)
           })
            # Add record id to the list of path records to exclude it in select for insert
            self.selList = self.selList + ',' + str(record.child.id)

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


