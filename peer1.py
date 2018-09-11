import socket
import threading
from threading import Thread
import rpyc
from constant import *
from peer import Client

def DownloadasServer():
  class ClientThread(Thread):
    def __init__(self, ip, port):
      Thread.__init__(self)
      self.ip = ip
      self.port = port
      print "[+] New thread started for " + ip + ":" + str(port)
    def run(self):
      while True:
        threadLock.acquire()
        data = conn.recv(1024)   #server recived fileName from client
        filename=data
        print('Server received', repr(data))
        # filename = 'mytext.txt'
        f = open(filename, 'rb')
        l = f.read(1024)
        while (l):
          conn.send(l)
          print('Sent ', repr(l))
          l = f.read(1024)
        f.close()
        conn.close()
        print('Done sending')
        threadLock.release()
        break
        # conn.send('Thank you for connecting')

  #port = 60000  # Reserve a port for your service.
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
  host = socket.gethostname()  # Get local machine name
  s.bind((host, peer1Port))  # Bind to the port
  threadLock = threading.Lock()
  threads = []

  while True:
    s.listen(5)  # Now wait for client connection.
    print 'Server listening....'
    (conn, (ip, port)) = s.accept()  # Establish connection with client.
    print 'Got connection from', (ip, port)
    newthread = ClientThread(ip, port)
    newthread.start()
    threads.append(newthread)

  for t in threads:
    t.join()

#client to download specific file from other peer
def DownloadasClient(filename, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
        host = socket.gethostname()  # Get local machine name
        s.connect((host, int(port)))
        s.send(filename)   #client send fileName to the server
        with open('recieved'+filename, 'wb') as f:
            print 'file opened'
            while True:
                print('receiving data...')
                data = s.recv(1024)
                #print('data=%s', (data))
                if not data:
                    break
                # write data to a file
                f.write(data)
        f.close()
        filelist.append('recieved_'+filename)
        print('Successfully get the file')
        s.close()
        print('connection closed')

#constants
peer1Port = 4567
filelist = ['Artificial.txt', 'managment.txt', 'mytext.txt']
PORTLIST = []

if __name__ == "__main__":
  peer1=Client(peer1Port)  #object from client
  while True :   #choose operation
    choice = raw_input("press 1 to load your files on server,press 2 to search file ,press 3 to download file,press 4 to send file,press 5 to exist ")
    if choice=='1':
      peer1.indexing(filelist)
    elif choice=='2':
      while True:
        filename = raw_input("Enter file Name ")
        if not filename:
          pass
        else:
          PORTLIST=peer1.findFile(filename)
          print PORTLIST
          break
    elif choice=='3':
        while True:
            Flag=False
            filename = raw_input("Enter file Name ")
            PORTLIST = peer1.findFile(filename)
            #print PORTLIST
            if not PORTLIST:
                print "File doesn't exist in the network"
                pass
            else:
                serverPeer = '54492'  # peer2
                #serverPeer = '54493'  # peer3
                length = len(PORTLIST)
                for i in range(0, length):
                    if serverPeer == PORTLIST[i]:
                        Flag=True
                if Flag==True:
                        DownloadasClient(filename, PORTLIST[i])
                else:
                        print "server peer doesn't have the file"
            break
    elif choice=='4':
      DownloadasServer()
      break
    elif choice=='5':
      print "bye ^^"
      break
    else:
      print "Enter only one digit number from 1 to 4 to choose "



