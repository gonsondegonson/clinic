from cryptography.fernet import Fernet
from django.conf import settings

def get_secret():
    # Get secret key
    return Fernet.generate_key().decode()

def encrypt_msg(msg, secret):
    # Get secret key
    if (secret == None or secret == ''):
        secret = settings.SECURE_KEY
    # Encrypt message using secure key
    fnet = Fernet(secret)
    encrypted_msg = fnet.encrypt(msg.encode())
    return encrypted_msg.decode()

def decrypt_msg(msg, secret):
    # Get secret key
    if (secret == None or secret == ''):
        secret = settings.SECURE_KEY
    # Decrypt message using secure key
    fnet = Fernet(secret)
    decrypted_msg = fnet.decrypt(msg)
    return decrypted_msg.decode()

def getParm(request, secret):
    # Initialize parm
    parm = None
    # Get secret key
    if (secret == None or secret == ''):
        secret = settings.SECURE_KEY
    # Get encrypted list of params received on URL 
    parm = request.GET.get('key', None)
    if parm != None:
        # Get decrypted list of params received on URL
        parm = decrypt_msg(parm, secret)

    return parm

def getParmList(request, secret):
    # Initialize parameter list
    parmList = {}
    # Get list of params received on URL
    parm = getParm(request, secret)
    if parm != None:
        # Splits each param to separate name and value and adds it to the param collection
        keyList = parm.split('|')
        for key in keyList:
            value = key.split('=')
            parmList[value[0]] = value[1]

    return parmList

def parm_list(request, secret):
    # Initialize parameter list
    parmList = {}

    # Get secret key
    if (secret == None or secret == ''):
        secret = settings.SECURE_KEY

    # Get encrypted list of params received on URL 
    keyList = request.GET.get('key', '**empty**')
    if keyList != '**empty**':
        # Get decrypted list of params received on URL
        keyList = decrypt_msg(keyList, secret).split('|')
        # Splits each param to separate name and value and adds it to the param collection
        for value in keyList:
            parm = value.split('=')
            parmList[parm[0]] = parm[1]

    return parmList

def getParmValue(parmList, parmName, defValue):
    # Get parameter from parameter list
    parmValue = parmList.get(parmName)
    # If not found, returnd default value
    if parmValue == None and defValue != None:
        parmValue = defValue
    
    return parmValue

def getUrlEncoded(url, secret):
    # Get secret key
    if (secret == None or secret == ''):
        secret = settings.SECURE_KEY

    # Return url encrypted
    return ('?key=' + encrypt_msg(url, secret))
    #return ('?key=' + url)
