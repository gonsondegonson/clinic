from django.db import models
from django.utils import timezone

from myprivateapp.models import *


class ContentStatus(models.TextChoices):
    Published = '0', 'Publicado'
    Design = '1', 'Diseño'
    Locked = '2', 'Bloqueado'
 
class Section(models.Model):
    id = models.AutoField(primary_key=True)
    parentSection = models.ForeignKey('Section', on_delete=models.PROTECT)
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=30, blank=True, null=True)
    order = models.IntegerField(default=0)
    status = models.CharField(max_length=1, choices=ContentStatus, default=ContentStatus.Design,)
    modification = models.DateTimeField(default=timezone.now)

    class Meta():
        db_table = 'section'

    def optKey(self):
        return ('idSection=' + str(self.id))

    def __str__(self):
        return (self.name)

class Site(models.Model):
    company = models.OneToOneField(Company, on_delete=models.PROTECT)
    url = models.CharField(max_length=256, unique=True)
    logo = models.CharField(max_length=256, blank=True, null=True)
    icon = models.CharField(max_length=256, blank=True, null=True)
    menu = models.ForeignKey(AppMenuItem, on_delete=models.PROTECT, null=True)
    backgroundColor = models.ForeignKey(Color, related_name="backgroundColor", on_delete=models.PROTECT, null=True)
    windowColor = models.ForeignKey(Color, related_name="windowColor", on_delete=models.PROTECT, null=True)
    navbarColor = models.ForeignKey(Color, related_name="navbarColor", on_delete=models.PROTECT, null=True)
    footerColor = models.ForeignKey(Color, related_name="footerColor", on_delete=models.PROTECT, null=True)
    mainSection = models.ForeignKey(Section, on_delete=models.PROTECT)
    modification = models.DateTimeField(default=timezone.now)

    class Meta():
        db_table = 'site'

    def optKey(self):
        return ('idSite=' + str(self.company))

    def __str__(self):
        return self.company.name

class Social(models.Model):
    id = models.AutoField(primary_key=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT)
    name = models.CharField(max_length=25)
    tooltip = models.CharField(max_length=60, blank=True, null=True)
    link = models.CharField(max_length=60, blank=True, null=True)
    icon = models.ForeignKey(Icon, on_delete=models.PROTECT)
    modification = models.DateTimeField(default=timezone.now)

    class Meta():
        db_table = 'social'
        indexes = [models.Index(fields=['site','name']),]
        unique_together = [('site','name'),]

    def optKey(self):
        return ('idSocial=' + str(self.id))

    def __str__(self):
        return (self.name)

class ContentType(models.Model):
    id = models.AutoField(primary_key=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT, default=1)
    name = models.CharField(max_length=25)
    modification = models.DateTimeField(default=timezone.now)

    class Meta():
        db_table = 'contentType'

    def __str__(self):
        return (self.name)

class Content(models.Model):
    id = models.AutoField(primary_key=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT, default=1)
    type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    title = models.CharField(max_length=64)
    resume = models.CharField(max_length=256)
    text = models.TextField()
    status = models.CharField(max_length=1, choices=ContentStatus, default=ContentStatus.Design,)
    creation = models.DateTimeField(default=timezone.now)
    modification = models.DateTimeField(default=timezone.now)

    class Meta():
        db_table = 'content'

    def __str__(self):
        return (self.title)
