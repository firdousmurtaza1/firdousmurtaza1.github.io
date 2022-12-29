from cryptography import fernet

def generate_key():
    return fernet.Fernet.generate_key()



def encrypt_string(message,fernet_key):
    f = fernet.Fernet(fernet_key)
    return f.encrypt(message.encode()).decode('utf-8')


def decrypt_string(message, fernet_key):
    f = fernet.Fernet(fernet_key)
    return f.decrypt(message.encode()).decode('utf-8')