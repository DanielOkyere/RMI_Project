#! /usr/bin/env python3

"""Server side code"""
import Pyro4


@Pyro4.expose
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


Pyro4.Daemon.serveSimple({
    FileServer: 'FileServer',
}, host="0.0.0.0", port=5000, ns=False, verbose=True)
