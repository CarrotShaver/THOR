from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto import Random
import random, string

class rsa():
    pub = ""
    encrypted_key = ""
    secret_code = ""
    key = None

    def rsa_gen(self):
        secret_size = 128
        self.secret_code = "".join(random.choices(
            string.ascii_uppercase + string.digits + string.ascii_lowercase, 
            k=secret_size)
            )
        
        self.key = RSA.generate(1024)
        self.encrypted_key = self.key.exportKey(
            passphrase = self.secret_code,
            pkcs = 8,
            protection = "scryptAndAES128-CBC"
        )
        self.pub = RSA.import_key(self.encrypted_key, passphrase = self.secret_code)
        file_out = open("rsakey.pem", "w+")
        
    def encrypt(self, message):
        hashed = SHA.new(message)
        cipher = PKCS1_v1_5.new(self.pub)
        ciphertext = cipher.encrypt(message+hashed.digest())
        return ciphertext

    def decrypt(self, ciphertext):
        dsize = SHA.digest_size
        sentinel = Random.new().read(15+dsize)
        cipher = PKCS1_v1_5.new(self.encrypted_key)
        message = cipher.decrypt( ciphertext, sentinel )

        digest = SHA.new(message[:-dsize]).digest()
        if digest==message[-dize:]:
            print("Message Decryption Successful")
            return message
        else:
            print("Message Decryption Unsuccessful")


if __name__=="__main__":
    rsa = rsa()
    rsa.rsa_gen()
    print (rsa.secret_code)
    print( (rsa.pub.publickey().exportKey()).decode("utf-8"))
    print( (rsa.encrypted_key).decode("utf-8") )

    message = (input("Encrypt Message: "))
    message = message.encode("utf-8")
    cipher = rsa.encrypt(message)
    print(cipher)
    input("Decrypting...")
    print(rsa.decrypt(cipher))