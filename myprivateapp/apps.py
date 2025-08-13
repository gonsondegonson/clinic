from django.apps import AppConfig

class MyPrivateAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myprivateapp'
