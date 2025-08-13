#from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings

from .models import *
from mysite import functions

#@login_required
def home(request):
    secret = AppSession.objects.get(session = request.session.session_key).secret
    parmList = functions.parm_list(request, secret)

    return render(request, 'private/home.html', {
        'STATIC_URL': settings.STATIC_URL,
        'STATIC_ROOT': settings.STATIC_ROOT,
        'STATICFILES_DIRS': settings.STATICFILES_DIRS,
    })
