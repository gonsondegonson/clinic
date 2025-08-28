from django.contrib import admin

from .models import *

class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name"]
    fields = ["name"]

admin.site.register(Company, CompanyAdmin)

class MemberAdmin(admin.ModelAdmin):
    list_display = ["company", "user", "code", "name", "surname"]
    fields = ["company", "user", "code", "name", "surname"]

admin.site.register(Member, MemberAdmin)

class AppSessionAdmin(admin.ModelAdmin):
    list_display = ["session", "secret", "creation", "modification"]
    fields = ["session", "secret", "creation", "modification"]

admin.site.register(AppSession, AppSessionAdmin)

class AppEntityAdmin(admin.ModelAdmin):
    list_display = ["name", "label", "optionList", "optionRecord"]
    fields = ["name", "label", "optionList", "optionRecord"]

admin.site.register(AppEntity, AppEntityAdmin)

class AppEntityFieldAdmin(admin.ModelAdmin):
    list_display = ["entity", "name", "label", "order"]
    fields = ["entity", "name", "label", "order"]

admin.site.register(AppEntityField, AppEntityFieldAdmin)
