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