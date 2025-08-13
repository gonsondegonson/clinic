from django.shortcuts import render
from .models import *

from mypublicapp.models import Site
from mysite import functions

def home(request):
    # Get list of parameters from URL request
    parmList = functions.parm_list(request, None)

    # Get Site object using Company Id received
    site = getSite(parmList.get("idCompany"), request.get_host())

    # Get list of Sections for the Site
    sections = getSections(site.company.id, parmList.get("idSection"))

    #Get list of Contents for the Section

    return render(request, 'public/home.html', 
        {'Site': site, 'Sections': sections, })

def getSite(idCompany, host):

    if idCompany == None:
        # Get Site object using host received in URL
        site = Site.objects.get(url = host)
    else:
        # Get Site object using Company Id received in URL
        site = Site.objects.get(id = idCompany)

    return site


def getSections(idSite, idSection):
    # Get list of Sections for the Site
    contentList=[ContentStatus.DESIGN, ContentStatus.PUBLISHED]
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