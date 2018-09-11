from collections import defaultdict
import rpyc
from constant import *
from rpyc.utils.server import ThreadedServer

class DBList(rpyc.Service):
  index=defaultdict(list)    #list of files

  # contain Register function to indext peer port and files the peer has
  # Register(port ,fileName) return void

  def exposed_Register(self,port,fileName):
      values = self.index[str(port)]
      size=len(values)
      lenght=len(fileName)
      for i in range(0,lenght): #loop to enter all files
          Flag = False
          for j in range(0,size):  #loop to check if file exist before
              if values[j]==fileName[i]:
                  Flag=True
                  break
          if Flag==False:
              self.index[str(port)].append(fileName[i])
      return self.index

  # contain search function to search for the port of the peers which have specific file
  # search (fileName) return list of peers ports that contain the file
  def exposed_search(self,fileName):
      portlist = []  # list of ports
      for key, value in self.index.items():
          count =len(value)
          for i in range(0,count):
              if value[i]==fileName:
                  portlist.append(key)
                  break
      return portlist





if __name__ == "__main__":
    # use threads to allow more than one peer to access in the same time
    server = ThreadedServer(DBList,hostname = SERVER, port = PORT)
    server.start()
#be aware of the thread synchronizing issues to avoid inconsistency or deadlock in your system.