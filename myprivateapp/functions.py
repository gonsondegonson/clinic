from .models import *
from mypublicapp.models import Site

from mysite import functions

def getAppSession(request):
    # Create or Update application session data
    appSession, created = AppSession.objects.update_or_create(
        session_id = request.session.session_key,
        defaults={
            'modification': timezone.now,
        },
        create_defaults={
            'member': Member.objects.get(user = request.user),
            'secret':  functions.get_secret(),
        }
    )
    # Get request URL
    appSession.requestUrl = '?' + str(request.GET.urlencode())
    # Get list of parameters from URL request using session secret
    appSession.parmList = functions.getParmList(request, appSession.secret)
    # Get menu list
    appSession.menuList = getMenuList(appSession)
    # Get menu tree
    getMenuTree(appSession, appSession.member.company.site.menu)

    return appSession

def getEntity(entityName, appSession):
    # Get Entity record
    entity = AppEntity.objects.get(name = entityName)
    # Get Entity fields
    entity.fields = entity.appentityfield_set.all()
    # Get Entity options
    entity.options = entity.appentityoption_set.all()
    entity.opt = type('opt', (), {
        'list': str(next((option for option in entity.options if option.type == OptionType.View), None)), 
        'edit': str(next((option for option in entity.options if option.type == OptionType.Add), None)),
    })
    # Get Entity authorisations
    entity.auth = type('auth', (), {
        'view': entity.hasPerm(appSession.member.user, OptionType.View), 
        'add': entity.hasPerm(appSession.member.user, OptionType.Add),
        'change': entity.hasPerm(appSession.member.user, OptionType.Change),
        'delete': entity.hasPerm(appSession.member.user, OptionType.Delete),
        'export': entity.hasPerm(appSession.member.user, OptionType.Export),
    })
    # Get URLs
    entity.url = type('url', (), {
        'list': functions.getUrlEncoded(('idOption=' + entity.opt.list), appSession.secret), 
        'edit': functions.getUrlEncoded(('idOption=' + entity.opt.edit), appSession.secret),
    })
    #entity.listOption = str(next((option for option in entity.options if option.type == OptionType.View), None))
    #entity.listUrl = functions.getUrlEncoded(('idOption=' + entity.opt.list), appSession.secret)

    #entity.editOption = str(next((option for option in entity.options if option.type == OptionType.Add), None))
    #entity.editUrl = functions.getUrlEncoded(('idOption=' + entity.opt.edit), appSession.secret)

    return entity


def getMenuList(appSession):
    menuItems = AppMenuItem.objects.all().order_by('label')

    for menuItem in menuItems:
        if menuItem.option != None:
            menuItem.hasPerm = menuItem.option.hasPerm(appSession.member.user)
            menuItem.url = functions.getUrlEncoded(('idOption=' + str(menuItem.option)), appSession.secret)

    return menuItems

def getMenuTree(appSession, appMenuItem):

    appMenuItem.itemList = AppMenuTree.objects.filter(parent = appMenuItem.id)

    for menuItem in appMenuItem.itemList:
        if menuItem.child.option != None:
            menuItem.hasPerm = menuItem.child.option.hasPerm(appSession.member.user)
            menuItem.url = functions.getUrlEncoded(('idOption=' + str(menuItem.child.option)), appSession.secret)
        # Get the next menu level
        getMenuTree(appSession, menuItem.child)

