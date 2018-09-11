# server.py
import socket                   # Import socket module
import threading
from threading import Thread

class ClientThread(Thread):
    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print "[+] New thread started for " + ip + ":" + str(port)

    def run(self):
        while True:
            threadLock.acquire()
            data = conn.recv(1024)
            print('Server received', repr(data))
            filename = 'mytext.txt'
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



port = 60000                    # Reserve a port for your service.
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)             # Create a socket object
host = socket.gethostname()     # Get local machine name
s.bind((host, port))            # Bind to the port
threadLock = threading.Lock()
threads = []

while True:
    s.listen(5)     # Now wait for client connection.
    print 'Server listening....'
    (conn, (ip, port)) = s.accept()  # Establish connection with client.
    print 'Got connection from', (ip, port)
    newthread = ClientThread(ip, port)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()





