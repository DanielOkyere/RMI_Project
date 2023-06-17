#! /usr/bin/env python3
""" Client Side code """

import Pyro4


uri = "PYRO:FileServer@0.0.0.0:5000"
fileServer = Pyro4.Proxy(uri)

filename = "example.txt"
file_data = fileServer.getFile(filename)

with open(filename, 'w') as file:
    file.write(file_data)

print("File recieved and saved: ", filename)
