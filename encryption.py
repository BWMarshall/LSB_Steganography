from cryptography.fernet import Fernet


def encrypt(data):
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data, key

def decrypt(data,key):
    f = Fernet(key)
    decrypted_data = f.decrypt(data)
    return decrypted_data.decode()


text = "hello World"

shh,key = encrypt(text)

print(shh)

data = decrypt(shh,key)

print(data)
print(key)