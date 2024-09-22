from cryptography.fernet import Fernet


def decrypt(value):
    with open('/etc/key') as file_in:
        key = file_in.read()

    fernet = Fernet(bytes(key.encode('utf-8')))
    return fernet.decrypt(bytes(value.encode('utf-8'))).decode('utf-8')


def encrypt(value):
    with open('/etc/key') as file_in:
        key = file_in.read()

    fernet = Fernet(bytes(key.encode('utf-8')))
    return fernet.encrypt(bytes(value.encode('utf-8'))).decode('utf-8')
