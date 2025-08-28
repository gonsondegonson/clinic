from django.contrib import admin

from .models import *

class SiteAdmin(admin.ModelAdmin):
    list_display = ["company", "url", "logo", "icon", "backgroundColor", "headerColor", "navbarColor", "footerColor"]
    fields = ["company", "url", "logo", "icon", "backgroundColor", "headerColor", "navbarColor", "footerColor"]

admin.site.register(Site, SiteAdmin)

class SectionAdmin(admin.ModelAdmin):
    list_display = ["site", "order", "name", "description", "status"]
    fields = ["site", "order", "name", "description", "status"]

admin.site.register(Section, SectionAdmin)

class ColorAdmin(admin.ModelAdmin):
    list_display = ["company", "name", "value"]
    fields = ["company", "name", "value"]

admin.site.register(Color, ColorAdmin)

class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ["site", "name"]
    fields = ["site", "name"]

admin.site.register(ContentType, ContentTypeAdmin)

class ContentAdmin(admin.ModelAdmin):
    list_display = ["site", "type", "title", "status", "creation", "modification"]
    fields = ["site", "type", "title", "status", "resume", "text"]

admin.site.register(Content, ContentAdmin)
