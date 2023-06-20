#! /usr/bin/env python3

"""Server side code"""
import Pyro4
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP, AES



@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class FileServer(object):
    """Class File Server
       Defines the methods and attributes for the class Server
    """
    def getFile(self, filename):
        """GetFile - Fetches the file from the server using the open API"""
        try:
            with open(filename, 'r') as file:
                return file.read()
        except IOError:
            raise ValueError('File not found: ' + filename)


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class RSA_clone(object):
    """RSA Class for encrypting and decrypting on server"""
    
    def gen_key(self, filename, passphrase):
        """Encrypts message by adding a digital signature
        Args:
            message: the message to be encrypted
        Returns: the public key 
        """
        key = RSA.generate(2048)
        pub_key = key.export_key(passphrase=passphrase,
                                       pkcs=8,
                                       protection="scryptAndAES128-CBC")
        file_out = open(filename, "wb")
        file_out.write(pub_key)
        file_out.close()
        


    def read_key(self, filename, passphrase):
        """Reads the Public RSA Key the message
        Args:
            filename (str): file name where RSA public key is store
            passphrase (str): secret passphrase to get public key
        Returns: public key"""
        encoded_key = open(filename, "rb").read()
        key = RSA.import_key(encoded_key, passphrase=passphrase)
        print(key.publickey().export_key())
        
    
    def encrypt_data(self, filename, passphrase,  data):
        """Encrypts the data
        Args: 
            filename(str): filename for RSA public key
            passphrase(str): Secret passphrase 
            data (str): data to be encrypted using RSA
        Returns: Encrypted Data"""
        
        file_out = open(filename, "wb")
        encoded_file = open("./reciever.pem", 'rb').read()
        recipient_key = RSA.import_key(encoded_file, passphrase)
        session_key = get_random_bytes(16)
        print('type of session key is ' + str(type(session_key)))
        
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        enc_session_key = cipher_rsa.encrypt(session_key)
        
        # cipher_aes = AES.new(session_key, AES.MODE_EAX, session_key)
        # cipher_text, tag = cipher_aes.encrypt_and_digest(data)
        [ file_out.write(x) for x in (
            enc_session_key, 
            # cipher_aes.nonce, 
            # tag, 
            # cipher_text
            )]
        file_out.close()
        
    
    def decrypt_data(self, filename, privatekey):
        """Decrypt data from the stored value
        Args:
            filename(str): filename for the data
            privatekey(str): privatekey for the data
        Returns: Decrypted Data
        """
        file_in = open(filename, "rb")
        private_key = RSA.import_key(open(privatekey).read())
        
        enc_session_key, nonce, tag, ciphertext = \
            [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]
        
        file_in.close()
        
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key = cipher_rsa.decrypt(enc_session_key)
        
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)
        print(data.decode('utf-8'))

def main():
    Pyro4.Daemon.serveSimple({
        FileServer: 'FileServer',
        RSA_clone: 'RSA_clone'
    }, host="127.0.0.1", port=5000, ns=True, verbose=True)


if __name__ == "__main__":
    main()