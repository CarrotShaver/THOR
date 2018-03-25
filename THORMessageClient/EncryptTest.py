import os
from Crypto.Cipher import AES # Used to create AES encrypted message
from Crypto.Hash import SHA256 # Used to convert a message into a 16 bit hash
from Crypto import Random # Used to make sure the IV is a random value each time it is used

def encrypt(key, messagetxt):
    chunksize = 64*1024
    outputtxt = "enc-"+messagetxt
    messagesize = str(os.path.getsize(messagetxt)).zfill(16)
    IV = Random.new().read(16)

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(messagetxt, "rb") as inmessage:
        with open(outputtxt, "wb") as outmessage:
            outmessage.write(messagesize.encode("utf-8"))
            outmessage.write(IV)

            while True:
                chunk = inmessage.read(chunksize)

                # Padding of message if not in 16 byte chunks
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b" " * (16 - (len(chunk) %16))

                outmessage.write(encryptor.encrypt(chunk))

def decrypt(key, messagetxt):
    chunksize = 64*1024
    outputtxt = messagetxt[11:]

    with open(messagetxt, "rb") as inmessage:
        messagesize = int(inmessage.read(16))
        IV = inmessage.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open("decryptedmsg", "wb") as outmessage:
            while True:
                chunk = inmessage.read(chunksize)
                
                if len(chunk) == 0:
                    break

                outmessage.write(decryptor.decrypt(chunk))

            outmessage.truncate(messagesize) # Removes padding from encryption

def getKey(password):
    hasher = SHA256.new(password.encode("utf-8"))
    return hasher.digest()

def Main():
    choice = input("Would you like to (E)ncrypt or (D)ecrypt?: ")

    if choice == "E":
        filename = input("File to encrypt: ")
        password = input("Password ")
        encrypt(getKey(password), filename)
        print("Done.")

    elif choice == "D":
        filename = input("File to decrypt: ")
        password = input("Password: ")
        decrypt(getKey(password), filename)
        print("Done.")

    else:
        print("No option selected, closing...")

if __name__=="__main__":
    Main()