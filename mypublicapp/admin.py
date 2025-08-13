from django.contrib import admin

from .models import Site
from .models import Section

admin.site.register(Site)
admin.site.register(Section)
