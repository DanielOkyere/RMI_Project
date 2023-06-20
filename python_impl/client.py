#! /usr/bin/env python3
""" Client Side code """

import Pyro4



fileServer = Pyro4.Proxy("PYRONAME:FileServer")



# Demonstrates the First Part Question 1
filename = "example.txt"
file_data = fileServer.getFile(filename)

with open(filename, 'a+') as file:
    content = file.read()
    print(content)
    file.write("\n Client has added some new text \n")

print("File recieved and saved: ", filename)

# Question 2


RSA_clone = Pyro4.Proxy('PYRONAME:RSA_clone')
print('-----------Server Generates a key-----------\n')

passphrase = input('Input Sever passphrase\n')
RSA_clone.gen_key('server_keys.pem', passphrase)
RSA_clone.read_key('server_keys.pem', passphrase)

print('---------Reciever Now has to generate a private Key--------\n')
reciever_passcode = input('Please Enter reciever passcode\n')
RSA_clone.gen_key('reciever.pem', reciever_passcode)
RSA_clone.read_key('reciever.pem', reciever_passcode)

print('-----------We would encrypt the data here now------------- \n')
input_data = input('Please input message to encrypt\n')
RSA_clone.encrypt_data('encrypt_data.txt', reciever_passcode, input_data)


# print('-----But would use server public key to decrypt------\n')
# RSA_clone.





# print('-------------------Decrypted data-----------------------')
# RSA_clone.decrypt_data('encrypt_data.txt', )
