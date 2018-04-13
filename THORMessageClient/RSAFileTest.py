from Crypto.PublicKey import RSA 
import random, string # Used for creating randomized strings for codes
from Crypto.Random import get_random_bytes # Used for AES hashing
from Crypto.Cipher import AES, PKCS1_OAEP

class rsa():
    code = None
    key = None
    encrypted_key = None
    public_key = None

    def code_gen(self, size):
        self.code = "".join(random.choices(
            string.ascii_letters + string.digits,
            k = size
        ))
        # Create code_gen file based on IP here

    def key_gen(self):
        self.code = self.code_gen(128)
        self.key = RSA.generate(2048)
        self.encrypted_key = self.key.exportKey(
            format = "PEM",
            passphrase = self.code,
            pkcs = 8,
            protection="scryptAndAES128-CBC"
        )
        
        private_out = open("rsa_key.pem", "wb") # Create private key file
        private_out.write(self.encrypted_key) # Write private key to file

        public_out = open("rsa_pub.pem", "wb") # Create public key file
        public_out.write(self.key.publickey().exportKey(format="PEM"))

    def get_key(self, filename): # server
        self.encrypted_key = open(filename, "rb").read()
        self.key = RSA.import_key(
            self.encrypted_key,
            passphrase = self.code
        )
        return self.key
        # Change to return a key object instead of setting global key variable
    
    def get_public(self, filename):
        public_key = RSA.import_key(open(filename).read()) # Creates public_key object
        return public_key # Returns the object, *use file.write(public.exportKey())

        # key = self.get_key(filename)
        # return key.publickey().exportKey(format="PEM")

    def encrypt(self, receiverfile, messagefile): # client-side
        # Creates encrypted filename
        encrypted_filename = open("encrypted_data.bin", "wb") 
        # Reads in receiver key and creates public key object
        target_public_key = RSA.import_key(open(receiverfile).read()) 
        # Creates a session key hash for the receiver
        session_key = get_random_bytes(16)
        # Begin encrypting with public key
        cipher_rsa = PKCS1_OAEP.new(target_public_key)
        encrypted_filename.write(cipher_rsa.encrypt(session_key))
        # Encrypt data with AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        # Read in the message to send
        ciphertext, tag = cipher_aes.encrypt_and_digest(open(messagefile, "rb").read())
        [ encrypted_filename.write(x) for x in (cipher_aes.nonce, tag, ciphertext)]

    def decrypt(self, encryptedfile, keyfile):
        decrypt_filename = open(encryptedfile, "rb")
        private_key = self.get_key(keyfile)

        enc_session_key, nonce, tag, ciphertext = \
            [ decrypt_filename.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

        # Decrypt session key with public RSA key
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)

        # Decrypt data with AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        decrypted_data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        return decrypted_data.decode("utf-8")

if __name__=="__main__":
    rsa = rsa()
    rsa.key_gen()
    rsa.get_key("rsa_key.pem")
    receiver = open("receiver.pem", "wb")
    receiver.write((rsa.get_public("rsa_pub.pem")).exportKey(format="PEM"))
    receiver.close()
    rsa.encrypt("receiver.pem", "testing.bin")
    print(rsa.decrypt("encrypted_data.bin", "rsa_key.pem"))
    
