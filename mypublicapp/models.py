from django.db import models
from myprivateapp.models import Company

class ContentStatus(models.TextChoices):
    PUBLISHED = '0', 'Publicado'
    DESIGN = '1', 'Diseño'
    LOCKED = '2', 'Bloqueado'

class Site(models.Model):
    company = models.OneToOneField(Company, on_delete=models.PROTECT)
    url = models.CharField(max_length=256)

    class Meta():
        db_table = 'B0001'

    def __str__(self):
        return Company.name
 
class Section(models.Model):
    id = models.AutoField(primary_key=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT)
    order = models.IntegerField(default=0)
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=1, choices=ContentStatus, default=ContentStatus.DESIGN,)

    class Meta():
        db_table = 'B0002'

    def __str__(self):
        return (self.name)

