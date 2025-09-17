from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from django.http import Http404
from django.utils.html import format_html
from django.template import Context, Template
from django.template.loader import render_to_string

from .models import *
from mypublicapp.models import Site

from .forms import EditColor

from .functions import *
from mysite import functions

@login_required
def home(request):
    # Get session data
    appSession = getAppSession(request)
    # Verify that the request come from same url and user than stored on session
    if (request.user == appSession.member.user) and (request.get_host() == appSession.member.company.site.url):
        # Get menu option from parameter list
        idOption = appSession.parmList.get("idOption")
        # Get html page for selected Option
        match idOption:
            case "ListCompany":
                option = "ListCompany#"
            case "ListMember":
                option = "ListMember#"
            case "ListColor":
                return getListColor(request, appSession)
            case "ListIcon":
                return getListIcon(request, appSession)
            case "ListLetter":
                return getListLetter(request, appSession)
            case "EditColor":
                return getEditColor(request, appSession)
            case _:
                return getUnknown(request, appSession)
    else:
        #Error - redirect to...#
        return getUnknown(request, appSession)

def getListColor(request, appSession):
    # Get Entity configuration
    entity = getEntity('color', appSession)
    # Retrieve database records
    colors = Color.objects.filter(company = appSession.member.company.id)
    # Add 'detail' record link to retrieved records
    editUrl = 'idOption=' + entity.opt.edit + '|' + 'idColor='
    for color in colors:
        color.editUrl = functions.getUrlEncoded(editUrl + str(color.id), appSession.secret)
        color.modal = render_to_string('private/edit/micolor.html', {'session': appSession, 'entity': entity, 'record': color, 'form': EditColor(instance=color)}, request=request)

    return render(request, 'private/list/color.html', {'session': appSession, 'entity': entity, 'records': colors, 'form': EditColor()})

def getListIcon(request, appSession):
    # Get Entity configuration
    entity = getEntity('icon', appSession)
    # Retrieve database records
    icons = Icon.objects.filter(company = appSession.member.company.id)
    # Add 'detail' record link to retrieved records
    editUrl = 'idOption=' + entity.opt.edit + '|' + 'idIcon='
    for icon in icons:
        icon.editUrl = functions.getUrlEncoded(editUrl + str(icon.id), appSession.secret)

    return render(request, 'private/list/icon.html', {'session': appSession, 'entity': entity, 'records': icons,})

def getListLetter(request, appSession):
    # Get Entity configuration
    entity = getEntity('letter', appSession)
    # Retrieve database records
    letters = Letter.objects.filter(company = appSession.member.company.id)
    # Add 'detail' record link to retrieved records
    editUrl = 'idOption=' + entity.opt.edit + '|' + 'idLetter='
    for letter in letters:
        letter.editUrl = functions.getUrlEncoded(editUrl + str(letter.id), appSession.secret)

    return render(request, 'private/list/letter.html', {'session': appSession, 'entity': entity, 'records': letters,})

def getUnknown(request, appSession):
    entity = getEntity('icon', appSession)

    return render(request, 'private/home.html', {
        'request': request,
        'session': appSession, 
        'entity': entity,
    })

def getEditColor(request, appSession):
     # Get Entity configuration
    entity = getEntity('color', appSession)
    # Get record
    idColor = appSession.parmList.get("idColor")
    if idColor != None:
        color = Color.objects.get(id = idColor)

    if request.method == "POST":
        if 'deletecolor' in request.POST:
            # Delete existing record
            #raise Http404("Delete Color: " + color.name)
            color.delete()

        if 'updatecolor' in request.POST:
            #raise Http404("Update Color: " + color.name)
            form = EditColor(request.POST)
            if form.is_valid():
                color = form.save(commit=False)
                if idColor != None:
                    # Change existing record
                    color.id = idColor
                    color.save(update_fields=['name','value'])
                else:
                    # Create new record
                    color.company = appSession.member.company
                    color.save()

        return getListColor(request, appSession)
    else:
        if idColor != None:
            # Edit existing record
            form = EditColor(instance=color)
        else:
            # Add new record
            form = EditColor()

    return render(request, 'private/edit/color.html', {'session': appSession, 'entity': entity, 'form': form})
