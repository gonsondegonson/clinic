from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.utils import timezone

from .models import *
from mypublicapp.models import *
from mysite import functions

@login_required
def home(request):
    # Get session data
    appSession = getAppSession(request)
    # Get list of parameters from URL request using session secret
    parmList = functions.parm_list(request, appSession.secret)
    # Get Site object using Company Id received
    site = getSite(parmList.get("idCompany"), request.get_host())
    if site.url == request.get_host():
        # Get member using User Id received
        member = Member.objects.get(user = request.user)
        # Get menu option from parameter list
        idOption = parmList.get("idOption")
        # Get 
        match idOption:
            case "ListCompany":
                option = "ListCompany#"
            case "ListMember":
                option = "ListMember#"
            case "ListColor":
                return getListColor(request, site, member, appSession, parmList)
            case _:
                return getUnknown(request, member, appSession, parmList)
    #else:
        #Error - redirect to#


def getAppSession(request):
    # Create or Update application session data
    appSession, created = AppSession.objects.update_or_create(
        session_id = request.session.session_key,
        defaults={'modification': timezone.now}
    )
    
    return appSession

def getSite(idCompany, host):
    # Get Site Object
    if idCompany == None:
        # Get Site object using host received in URL
        site = Site.objects.get(url = host)
    else:
        # Get Site object using Company Id received in URL
        site = Site.objects.get(id = idCompany)

    return site

def getEntityFields(entity, OrderBy, parmList, appSession):
    # Get list of entity fields
    entityFields = entity.appentityfield_set.all()
    # Add order link to fields for headers
    for field in entityFields:
        if field.order != OrderType.NoOrder:
            if field.name == OrderBy.replace('-',''):
                # If current order field, switchs Asc <--> Dsc
                url = 'idOption=' + field.entity.optionList + '|' + 'OrderBy=' + ('' if OrderBy.startswith('-') else '-') + field.name
                # 
                if OrderBy.startswith('-'):
                    field.iconDown = ' '
                else:
                    field.iconUp = ' '
            else:
                # If not, assigns defined order
                url = 'idOption=' + field.entity.optionList + '|' + 'OrderBy=' + ('-' if field.order == OrderType.Descending else '') + field.name

            # Save Url encoded
            field.url = functions.getUrlEncoded(parmList, url, appSession.secret)
    
    return entityFields

def getListColor(request, site, member, appSession, parmList):
    # Get Parameters
    OrderBy = functions.getParameter(parmList, "OrderBy", "name")
    RecordLimit = functions.getParameter(parmList, "RecordLimit", 100)
    # Get Entity record
    entity = AppEntity.objects.get(name = 'Color')

    # Retrieve database records
    colors = Color.objects.filter(company = site.company.id).order_by(OrderBy)[:int(RecordLimit)]
    # Add detail link to retrieved records
    for color in colors:
        url = 'idOption=' + entity.optionRecord + '|' + 'idColor=' + str(color.id)
        color.url = functions.getUrlEncoded(parmList, url, appSession.secret)

    entity.entityFields = getEntityFields(entity, OrderBy, parmList, appSession)

    return render(request, 'private/ListColor.html', {'site': site, 'member': member, 'entity': entity, 'colors': colors,})


def getUnknown(request, member, appSession, parmList):

    #url = 'idCompany=' + str(parmList.get("idCompany")) + '|' + 'idOption=' + str(parmList.get("idOption"))
    url = 'idCompany=' + '1' + '|' + 'idOption=' + 'ListColor'
    url = '?key=' + functions.encrypt_msg(url, appSession.secret)

    return render(request, 'private/home.html', {
        'STATIC_URL': appSession.secret,
        'STATIC_ROOT': appSession.creation,
        'STATICFILES_DIRS': appSession.modification,
        'idOption': member,
        'URL': url,
    })

