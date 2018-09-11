import rpyc
from constant import *

class Client:
    global conn   # Connect to the server
    conn = rpyc.connect(SERVER, PORT)  # Connect to the server

    def __init__(self,port):
        self.port=port

    def indexing(self,FILELIST) :
        filelist=conn.root.exposed_Register(self.port,FILELIST)
        print filelist

    def findFile(self,FILENAME):
        PORTLIST=conn.root.exposed_search(FILENAME)
        return PORTLIST


