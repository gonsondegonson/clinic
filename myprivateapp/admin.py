from django.contrib import admin

from .models import Company
from .models import Member

admin.site.register(Company)
admin.site.register(Member)
