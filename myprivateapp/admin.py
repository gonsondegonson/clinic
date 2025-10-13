from django.contrib import admin

from .models import *

admin.site.site_header = 'AppaaS - Application as a Service'
admin.site.index_title = 'Control Pannel'
admin.site.site_title = 'Application as a Service'


class ColorAdmin(admin.ModelAdmin):
    list_display = ["company", "name", "value"]
    fields = ["company", "name", "value"]
admin.site.register(Color, ColorAdmin)

class LetterAdmin(admin.ModelAdmin):
    list_display = ["company", "name", "value"]
    fields = ["company", "name", "value"]
admin.site.register(Letter, LetterAdmin)

class IconAdmin(admin.ModelAdmin):
    list_display = ["company", "name", "value"]
    fields = ["company", "name", "value"]
admin.site.register(Icon, IconAdmin)

class AppMenuItemAdmin(admin.ModelAdmin):
    list_display = ["company", "name", "label", "icon", "option"]
    fields = ["company", "name", "label", "icon", "option"]
admin.site.register(AppMenuItem, AppMenuItemAdmin)

class AppMenuTreeAdmin(admin.ModelAdmin):
    list_display = ["parent", "child", "order"]
    fields = ["parent", "child", "order"]
admin.site.register(AppMenuTree, AppMenuTreeAdmin)
