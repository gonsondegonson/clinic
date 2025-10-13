from django.shortcuts import render
import datetime

from .models import *
from .forms import *
from .functions import *

from myapp import functions
from myapp.views import appLogin

from mypublicapp.models import Site, Social

#raise Exception("Id: " + str(idColor))

#@login_required
def home(request):

    if not request.user.is_authenticated:
        # Build login window, if not connected.
        site = Site.objects.get(url = request.get_host())
        site.social = Social.objects.filter(site = site.id)
        return appLogin(request, site)
    else:
        # Get session data
        appSession = getAppSession(request)
        # Verify that the request come from same url and user than stored on session
        if (request.user == appSession.member.user) and (request.get_host() == appSession.member.company.site.url):
            # Get menu option from parameter list
            #idOption = '' if appSession.parmList.get("idOption") == None else appSession.parmList.get("idOption")
            idOption = functions.getParmValue(appSession.parmList, "idOption", "")
            # Get html page for selected Option
            match idOption.upper():
                case "LISTCOLOR":
                    return getListColor(request, appSession)
                case "LISTICON":
                    return getListIcon(request, appSession)
                case "LISTLETTER":
                    return getListLetter(request, appSession)
                case "LISTMENUITEM":
                    return getListMenuItem(request, appSession)
                case "LISTMENUTREE":
                    return getListMenuTree(request, appSession)
                case "EDITCOLOR":
                    return getEditColor(request, appSession)
                case "EDITLETTER":
                    return getEditLetter(request, appSession)
                case "EDITICON":
                    return getEditIcon(request, appSession)
                case "EDITMENUITEM":
                    return getEditMenuItem(request, appSession)
                case "EDITMENUTREE":
                    return getEditMenuTree(request, appSession)
                case _:
                    return getUnknown(request, appSession)
        else:
            #Error - redirect to...#
            return getUnknown(request, appSession)


def getListColor(request, appSession):
    # Get Entity configuration
    entity = getEntity('color', appSession)
    # Retrieve database records
    entity.records = Color.objects.filter(company = appSession.member.company.id).order_by('name')
    entity.getUrls(appSession.secret)

    return render(request, 'private/list/color.html', {'session': appSession, 'entity': entity, 'records': entity.records,})

def getListIcon(request, appSession):
    # Get Entity configuration
    entity = getEntity('icon', appSession, False)
    # Retrieve database records
    entity.records = Icon.objects.filter(company = appSession.member.company.id).order_by('name')
    entity.getUrls(appSession.secret)

    return render(request, 'private/list/icon.html', {'session': appSession, 'entity': entity, 'records': entity.records,})

def getListLetter(request, appSession):
    # Get Entity configuration
    entity = getEntity('letter', appSession, True)
    # Retrieve database records
    entity.records = Letter.objects.filter(company = appSession.member.company.id).order_by('name')
    entity.getUrls(appSession.secret, EditLetter)

    return render(request, 'private/list/letter.html', {'session': appSession, 'entity': entity, 'records': entity.records,})

def getListMenuItem(request, appSession):
    # Get Entity configuration
    entity = getEntity('menuItem', appSession, False)
    # Retrieve database records
    entity.records = AppMenuItem.objects.filter(company = appSession.member.company.id).order_by('name')
    entity.getUrls(appSession.secret)

    return render(request, 'private/list/menuItem.html', {'session': appSession, 'entity': entity, 'records': entity.records,})

def getListMenuTree(request, appSession):
    # Get Entity configuration
    entity = getEntity('menuTree', appSession, True)
    # Retrieve parent record key
    idParent = appSession.parmList.get("idParent")
    if idParent == None:
        #idParent = str(appSession.member.company.menu.id)
        idParent = str(7)

    # Retrieve parent path records
    pathList = appSession.parmList.get("pathList")
    pathList = idParent if pathList == None else (pathList + ',' + idParent) if idParent not in [id for id in pathList.split(',')] else pathList
    urlList = None
    entity.pathObjects = []
    for objectId in pathList.split(','):
        urlList = objectId if urlList == None else (urlList + ',' + objectId)
        pathObject = AppMenuItem.objects.get(id = int(objectId))
        pathObject.url = getUrlEncoded(entity.opt.list + '|idParent=' + str(pathObject.id) + '|pathList=' + urlList, appSession.secret)
        entity.pathObjects.append(pathObject)

    # Disable standard 'add record' URL
    entity.url.edit = None

    # Retrieve child records
    entity.records = AppMenuTree.objects.filter(parent = idParent).order_by('order')
    entity.getTreeUrls(pathList, appSession.secret)
    for record in entity.records:
        # Disable standard 'edit record' URL
        record.url.edit = None

    # Retrieve select records for insert
    entity.select = []
    entity.select.append(getEntity('menuItem', appSession, False))
    entity.select.append(getEntity('color', appSession, False))

    entity.select[0].records = AppMenuItem.objects.filter(company = appSession.member.company.id).exclude(id__in = list(map(int, entity.selList.split(',')))).order_by('label')
    for record in entity.select[0].records:
        # Insert record URL
        record.url = getUrlEncoded((entity.opt.edit + '|idOperation=Insert|idParent=' + idParent + '|idChild=' + str(record.id) + '|pathList=' + pathList), appSession.secret)

    entity.select[1].records = Color.objects.filter(company = appSession.member.company.id)

    return render(request, 'private/list/menuTree.html', {'session': appSession, 'entity': entity, 'records': entity.records,})

def getUnknown(request, appSession):
    entity = getEntity('icon', appSession, False)

    return render(request, 'private/home.html', {
        'request': request,
        'session': appSession, 
        'entity': entity,
    })

def getEditMenuItem(request, appSession):
     # Get Entity configuration
    entity = getEntity('menuItem', appSession, False)
    # Get record
    idMenu = appSession.parmList.get("idMenu")
    if not getRecord(appSession, entity, [idMenu]):
        # The record no longer exists
        return getListMenuItem(request, appSession)
    else:
        if request.method == "POST":
            # Update record
            try:
                form = EditMenuItem(request.POST)
                if 'deletemenu' in request.POST:
                    # Delete existing record
                    entity.record.delete()
                if 'updatemenu' in request.POST:
                    if form.is_valid():
                        if entity.record != None:
                            if 1 != 1:
                            #if str(entity.record.modification) != str(request.POST.get("modification")):
                                # The record was changed by another user
                                appSession.errors.append('¡Registro modificado por otro usuario!')
                            else:
                                # Change existing record
                                entity.record = form.save(commit=False)
                                entity.record.id = idMenu
                                #entity.record.modification = datetime.datetime.now()
                                entity.record.save(update_fields=['name','label','icon', 'option'])
                        else:
                            # Create new record
                            entity.record = form.save(commit=False)
                            entity.record.company = appSession.member.company
                            #entity.record.modification = datetime.datetime.now()
                            entity.record.save()
                    else:
                        # Errors in Form
                        raise Exception('Errores en el formulario')
                # Go back to data list
                return getListMenuItem(request, appSession)
            except Exception as Ex:
                # Error updating record
                #del entity.record
                appSession.errors.append(functions.getException(Ex))
        #else:
        # Send data to form, if exists
        form = EditMenuItem() if entity.record == None else EditMenuItem(instance=entity.record)

    return render(request, 'private/edit/base.html', {'session': appSession, 'entity': entity, 'form': functions.getFormLabels(entity, form),})

def getEditMenuTree(request, appSession):
     # Get Entity configuration
    entity = getEntity('menuTree', appSession, False)

    # Get Parameters
    idOperation = functions.getParmValue(appSession.parmList, "idOperation", "").upper()
    idParent = functions.getParmValue(appSession.parmList, "idParent", "")
    idChild = functions.getParmValue(appSession.parmList, "idChild", "")
    idMenuTree = functions.getParmValue(appSession.parmList, "idMenuTree", "")
    try:
        if idOperation == "INSERT":
            # Create new record
            entity.record = AppMenuTree.objects.filter(parent = idParent).order_by('order').last()
            entity.record.id = None
            entity.record.child_id = int(idChild)
            entity.record.order += 10
            entity.record.save()
        else:
            # Get existing record
            if getRecord(appSession, entity, [idMenuTree]):
                match idOperation:
                    case "DELETE":
                        # Delete existing record
                        entity.record.delete()
                    case "SWITCHUP":
                        raise Exception('SWITCHUP')
                    case "SWITCHDOWN":
                        raise Exception('SWITCHDOWN')
    except Exception as Ex:
        # Error updating record
        appSession.errors.append(functions.getException(Ex))

    return getListMenuTree(request, appSession)

def getEditColor(request, appSession):
     # Get Entity configuration
    entity = getEntity('color', appSession, False)
    # Get record
    idColor = appSession.parmList.get("idColor")
    if not getRecord(appSession, entity, [idColor]):
        # The record no longer exists
        return getListColor(request, appSession)
    else:
        if request.method == "POST":
            # Update record
            try:
                form = EditColor(request.POST)
                if 'deletecolor' in request.POST:
                    # Delete existing record
                    entity.record.delete()
                if 'updatecolor' in request.POST:
                    if form.is_valid():
                        if entity.record != None:
                            if str(entity.record.modification) != str(request.POST.get("modification")):
                                # The record was changed by another user
                                appSession.errors.append('¡Registro modificado por otro usuario!')
                            else:
                                # Change existing record
                                entity.record = form.save(commit=False)
                                entity.record.id = idColor
                                entity.record.modification = datetime.datetime.now()
                                entity.record.save(update_fields=['name','value','modification'])
                        else:
                            # Create new record
                            entity.record = form.save(commit=False)
                            entity.record.company = appSession.member.company
                            entity.record.modification = datetime.datetime.now()
                            entity.record.save()
                    else:
                        # Errors in Form
                        raise Exception('Errores en el formulario')
                # Go back to data list
                return getListColor(request, appSession)
            except Exception as Ex:
                # Error updating record
                #del entity.record
                appSession.errors.append(functions.getException(Ex))
        #else:
        # Send data to form, if exists
        form = EditColor(initial={'value': '#000000',}) if entity.record == None else EditColor(instance=entity.record)

    return render(request, 'private/edit/base.html', {'session': appSession, 'entity': entity, 'form': functions.getFormLabels(entity, form),})

def getEditLetter(request, appSession):
     # Get Entity configuration
    entity = getEntity('letter', appSession, False)
    # Get record
    idLetter = appSession.parmList.get("idLetter")
    if not getRecord(appSession, entity, [idLetter]):
        # The record no longer exists
        return getListLetter(request, appSession)
    else:
        if request.method == "POST":
            # Update record
            try:
                form = EditLetter(request.POST)
                if 'deleteletter' in request.POST:
                    # Delete existing record
                    entity.record.delete()
                if 'updateletter' in request.POST:
                    if form.is_valid():
                        if entity.record != None:
                            if str(entity.record.modification) != str(request.POST.get("modification")):
                                # The record was changed by another user
                                appSession.errors.append('¡Registro modificado por otro usuario!')
                            else:
                                # Change existing record
                                entity.record = form.save(commit=False)
                                entity.record.id = idLetter
                                entity.record.modification = datetime.datetime.now()
                                entity.record.save(update_fields=['name','value','modification'])
                        else:
                            # Create new record
                            entity.record = form.save(commit=False)
                            entity.record.company = appSession.member.company
                            entity.record.modification = datetime.datetime.now()
                            entity.record.save()
                    else:
                        # Errors in Form
                        raise Exception('Errores en el formulario')
                # Go back to data list
                return getListLetter(request, appSession)
            except Exception as Ex:
                # Error updating record
                #del entity.record
                appSession.errors.append(functions.getException(Ex))
        else:
            # Send data to form, if exists
            form = EditLetter() if entity.record == None else EditLetter(instance=entity.record)

    return render(request, 'private/edit/base.html', {'session': appSession, 'entity': entity, 'form': functions.getFormLabels(entity, form),})

def getEditIcon(request, appSession):
     # Get Entity configuration
    entity = getEntity('icon', appSession, False)
    # Get record
    idIcon = appSession.parmList.get("idIcon")
    if not getRecord(appSession, entity, [idIcon]):
        # The record no longer exists
        return getListIcon(request, appSession)
    else:
        if request.method == "POST":
            # Update record
            try:
                form = EditIcon(request.POST)
                if 'deleteicon' in request.POST:
                    # Delete existing record
                    entity.record.delete()
                if 'updateicon' in request.POST:
                    if form.is_valid():
                        if entity.record != None:
                            if str(entity.record.modification) != str(request.POST.get("modification")):
                                # The record was changed by another user
                                appSession.errors.append('¡Registro modificado por otro usuario!')
                            else:
                                # Change existing record
                                entity.record = form.save(commit=False)
                                entity.record.id = idIcon
                                entity.record.modification = datetime.datetime.now()
                                entity.record.save(update_fields=['name','value','modification'])
                        else:
                            # Create new record
                            entity.record = form.save(commit=False)
                            entity.record.company = appSession.member.company
                            entity.record.modification = datetime.datetime.now()
                            entity.record.save()
                    else:
                        # Errors in Form
                        raise Exception('Errores en el formulario')
                # Go back to data list
                return getListIcon(request, appSession)
            except Exception as Ex:
                # Error updating record
                #del entity.record
                appSession.errors.append(functions.getException(Ex))
        else:
            # Send data to form, if exists
            form = EditIcon() if entity.record == None else EditIcon(instance=entity.record)

    return render(request, 'private/edit/base.html', {'session': appSession, 'entity': entity, 'form': functions.getFormLabels(entity, form),})

