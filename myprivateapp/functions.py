from myapp.models import *
from .models import *

from myapp import functions

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
    # Initialize Error list
    appSession.errors = []
    # Get request URL
    #appSession.requestUrl = '?' + str(request.GET.urlencode())
    # Get list of parameters from URL request using session secret
    appSession.parmList = functions.getParmList(request, appSession.secret)
    # Get menu list
    appSession.menuList = getMenuList(appSession)
    # Get menu tree
    getMenuTree(appSession, appSession.member.company.site.menu)

    return appSession

def getEntity(entityName, appSession, isModal=False):
    # Get Entity record 
    entity = AppEntity.objects.get(name = entityName)
    # Get Entity fields
    entity.fields = entity.appentityfield_set.all()
    # Get Entity options
    entity.options = entity.appentityoption_set.all()
    entity.opt = type('opt', (), {
        'list': 'idOption=' + str(next((option.option for option in entity.options if option.type == OptionType.View), None)), 
        'edit': 'idOption=' + str(next((option.option for option in entity.options if option.type == OptionType.Add), None)),
    })
    # Get Entity authorisations
    entity.auth = type('auth', (), {
          'view': entity.hasPerm(appSession.member.user, OptionType.View), 
           'add': entity.hasPerm(appSession.member.user, OptionType.Add),
        'change': entity.hasPerm(appSession.member.user, OptionType.Change),
        'delete': entity.hasPerm(appSession.member.user, OptionType.Delete),
        'export': entity.hasPerm(appSession.member.user, OptionType.Export),
    })
    # Get Entity URLs
    entity.url = type('url', (), {
        'list': functions.getUrlEncoded(entity.opt.list, appSession.secret) if entity.auth.view else None, 
        'edit': functions.getUrlEncoded(entity.opt.edit, appSession.secret) if entity.auth.add else None,
    })
    # Get Modal Flag
    entity.isModal = True if isModal else False

    return entity


def getMenuList(appSession):
    menuItems = AppMenuItem.objects.all().order_by('label')

    for menuItem in menuItems:
        if menuItem.option != None:
            menuItem.hasPerm = menuItem.option.hasPerm(appSession.member.user)
            menuItem.url = functions.getUrlEncoded(('idOption=' + str(menuItem.option)), appSession.secret)

    return menuItems

def getMenuTree(appSession, appMenuItem):

    appMenuItem.itemList = AppMenuTree.objects.filter(parent = appMenuItem.id).order_by('order')

    for menuItem in appMenuItem.itemList:
        if menuItem.child.option != None:
            menuItem.hasPerm = menuItem.child.option.hasPerm(appSession.member.user)
            menuItem.url = functions.getUrlEncoded(('idOption=' + str(menuItem.child.option)), appSession.secret)
        # Get the next menu level
        getMenuTree(appSession, menuItem.child)

def getRecord(AppSession, AppEntity, keyFields):

    try:
        match AppEntity.name:
            case "color":
                AppEntity.record = Color.objects.get(id = keyFields[0]) if keyFields[0] != None else None
            case "icon":
                AppEntity.record = Icon.objects.get(id = keyFields[0]) if keyFields[0] != None else None
            case "letter":
                AppEntity.record = Letter.objects.get(id = keyFields[0]) if keyFields[0] != None else None
            case "menuItem":
                AppEntity.record = AppMenuItem.objects.get(id = keyFields[0]) if keyFields[0] != None else None
            case "menuTree":
                AppEntity.record = AppMenuTree.objects.get(id = keyFields[0]) if keyFields[0] != None else None
            case _:
                pass

    except Exception as Ex:
        AppSession.errors.append('¡El registro ya no existe en ' + AppEntity.label + '! (pudo ser eliminado por otro usuario)')
        return False

    if AppEntity.record is not None:
        AppEntity.getUrl(AppSession.secret)

    return True
