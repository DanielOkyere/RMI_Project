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
    file.write("Client has added some text")

print("File recieved and saved: ", filename)

# Question 2
message = 'Welcome'
print('Unencrypted text: ' + message)

RSA_clone = Pyro4.Proxy('PYRONAME:RSA_clone')
encrypted = RSA_clone.encrypt('user_encrypt', message)

print('Message Encrypted Using RSA is : ' + str(encrypted))

print('\n lets decrypt it \n')

decrypted = RSA_clone.decrypt('user_encrypt', message)

print('Voila! is decrypted: ' + str(decrypted))