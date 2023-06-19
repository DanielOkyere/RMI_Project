#! /usr/bin/env python3

"""Server side code"""
import Pyro4
from Crypto.PublicKey import RSA



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
    
    def encrypt(self, filename, message):
        """Encrypts message by adding a digital signature
        Args:
            message: the message to be encrypted
        Returns: the public key 
        """
        key = RSA.generate(2048)
        encrypted_key = key.export_key(passphrase=message,
                                       pkcs=8,
                                       protection="scryptAndAES128-CBC")
        file_out = open(filename, "wb")
        file_out.write(encrypted_key)
        file_out.close()
        #print(key.publickey().export_key())
        return key.publickey().export_key()


    def decrypt(self, filename, passphrase):
        """Decrypts the message"""
        encoded_key = open(filename, "rb").read()
        key = RSA.import_key(encoded_key, passphrase=passphrase)
        #print(key.publickey().export_key())
        
        return key.publickey().export_key()
        
def main():
    Pyro4.Daemon.serveSimple({
        FileServer: 'FileServer',
        RSA_clone: 'RSA_clone'
    }, host="127.0.0.1", port=5000, ns=True, verbose=True)


if __name__ == "__main__":
    main()