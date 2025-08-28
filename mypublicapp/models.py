from django.db import models
from django.utils import timezone

from myprivateapp.models import Company

class ContentStatus(models.TextChoices):
    PUBLISHED = '0', 'Publicado'
    DESIGN = '1', 'Diseño'
    LOCKED = '2', 'Bloqueado'

class Color(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, default=1)
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

class Site(models.Model):
    company = models.OneToOneField(Company, on_delete=models.PROTECT)
    url = models.CharField(max_length=256)
    logo = models.CharField(max_length=256, blank=True, null=True)
    icon = models.CharField(max_length=256, blank=True, null=True)
    backgroundColor = models.ForeignKey(Color, related_name="backgroundColor", on_delete=models.PROTECT, null=True)
    headerColor = models.ForeignKey(Color, related_name="headerColor", on_delete=models.PROTECT, null=True)
    navbarColor = models.ForeignKey(Color, related_name="navbarColor", on_delete=models.PROTECT, null=True)
    footerColor = models.ForeignKey(Color, related_name="footerColor", on_delete=models.PROTECT, null=True)

    class Meta():
        db_table = 'site'

    def __str__(self):
        return self.company.name
 
class Section(models.Model):
    id = models.AutoField(primary_key=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT)
    order = models.IntegerField(default=0)
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=1, choices=ContentStatus, default=ContentStatus.DESIGN,)

    class Meta():
        db_table = 'section'

    def __str__(self):
        return (self.name)

class ContentType(models.Model):
    id = models.AutoField(primary_key=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT, default=1)
    name = models.CharField(max_length=25)

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
    status = models.CharField(max_length=1, choices=ContentStatus, default=ContentStatus.DESIGN,)
    creation = models.DateTimeField(default=timezone.now)
    modification = models.DateTimeField(default=timezone.now)

    class Meta():
        db_table = 'content'

    def __str__(self):
        return (self.title)
