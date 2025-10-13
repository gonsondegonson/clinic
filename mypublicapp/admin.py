from django.contrib import admin

from .models import *

class SiteAdmin(admin.ModelAdmin):
    list_display = ["company", "url", "logo", "icon", "menu", "backgroundColor", "windowColor", "navbarColor", "footerColor"]
    fields = ["company", "url", "logo", "icon", "menu", "backgroundColor", "windowColor", "navbarColor", "footerColor"]
admin.site.register(Site, SiteAdmin)

class SectionAdmin(admin.ModelAdmin):
    list_display = ["site", "order", "name", "description", "status"]
    fields = ["site", "order", "name", "description", "status"]
admin.site.register(Section, SectionAdmin)

class SocialAdmin(admin.ModelAdmin):
    list_display = ["site", "name", "tooltip", "link", "icon"]
    fields = ["site", "name", "tooltip", "link", "icon"]
admin.site.register(Social, SocialAdmin)

class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ["site", "name"]
    fields = ["site", "name"]
admin.site.register(ContentType, ContentTypeAdmin)

class ContentAdmin(admin.ModelAdmin):
    list_display = ["site", "type", "title", "status", "creation", "modification"]
    fields = ["site", "type", "title", "status", "resume", "text"]
admin.site.register(Content, ContentAdmin)
