from django.contrib import admin
from .models import *

class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name"]
    fields = ["name"]
admin.site.register(Company, CompanyAdmin)

class MemberAdmin(admin.ModelAdmin):
    list_display = ["company", "user", "code", "name", "surname"]
    fields = ["company", "user", "code", "name", "surname"]
    search_fields = ("company", "code")
    ordering = ("company","code")
admin.site.register(Member, MemberAdmin)

class AppSessionAdmin(admin.ModelAdmin):
    list_display = ["session", "member", "secret", "creation", "modification"]
    fields = ["session", "member", "secret", "creation", "modification"]
admin.site.register(AppSession, AppSessionAdmin)

class AppEntityAdmin(admin.ModelAdmin):
    list_display = ["app", "name", "label"]
    fields = ["app", "name", "label"]
admin.site.register(AppEntity, AppEntityAdmin)

class AppEntityFieldAdmin(admin.ModelAdmin):
    list_display = ["entity", "name", "label", "order"]
    fields = ["entity", "name", "label", "order"]
admin.site.register(AppEntityField, AppEntityFieldAdmin)

class AppEntityOptionAdmin(admin.ModelAdmin):
    list_display = ["entity", "type", "option"]
    fields = ["entity", "type", "option"]
admin.site.register(AppEntityOption, AppEntityOptionAdmin)
