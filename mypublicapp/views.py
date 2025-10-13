from django.shortcuts import render
from django.template.loader import render_to_string

from .models import *

from myapp import functions
from myapp.forms import AppLogin
from myapp.views import appLogin, appLogout

def home(request):
    # Get list of parameters from URL request using project secret
    parmList = functions.parm_list(request, None)
    # Get Site object using host received in URL
    site = getSite(request, None, request.get_host())
    # Get menu option from parameter list
    idOption = parmList.get("idOption")
    # Get process selected Option (if any)
    match idOption:
        case "Login":
            return appLogin(request, site.company)
        case "Logout":
            return appLogout(request)
        #case _:

    # Get list of Social for the Site
    site.social = Social.objects.filter(site = site.company.id)
    # Get list of Sections for the Site
    site.sections = getSections(site.company.id, parmList.get("idSection"))
    # Get Carousel for the Site
    # Get list of Contents for the Site


    return render(request, 'public/home.html', {'site': site})




def getSite(request, idCompany, host):
    # Get Site Object
    if idCompany == None:
        # Get Site object using host received in URL
        site = Site.objects.get(url = host)
    else:
        # Get Site object using Company Id received in URL
        site = Site.objects.get(id = idCompany)

    # Build login modal window, if not connected
    if request.user.is_authenticated:
        site.urlLogout = '?key=' + functions.encrypt_msg('idOption=Logout', None)
    else:
        site.urlLogin = '?key=' + functions.encrypt_msg('idOption=Login', None)
        site.login = render_to_string('./loginmodal.html', {'site': site, 'form': AppLogin()}, request=request)

    return site

def getSections(idSite, idSection):
    # Get list of Sections for the Site
    contentList=[ContentStatus.Design, ContentStatus.Published]
    sections = Section.objects.filter(site = idSite, status__in=contentList).order_by('order')

    # Get current section data received in URL, otherwhise takes first on list
    if idSection == None:
        idSection = str(sections[0].id)

    for section in sections:
        if str(section.id) == idSection:
            section.current = True
        else:
            section.current = False

        url = 'idSite=' + str(section.site.company.id) + '|' + 'idSection=' + str(section.id)
        section.url = '?key=' + functions.encrypt_msg(url, None)

    return sections