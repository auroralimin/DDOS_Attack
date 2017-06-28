import socket
import struct
import sys

class Body(object):
    body = ""

class Reply(object):
    reply = ""

def configMulticastSock():
    mCastGrpAddr = '224.1.1.1'
    mCastPort = 5007
    serverAddr = ('', mCastPort)

    # Tell the operating system to add the socket to the multicast group
    # on all interfaces.
    group = socket.inet_aton(mCastGrpAddr)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)

    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Bind to the server address
    sock.bind(serverAddr)
    return sock

def rcvMsg(sock, aliveEvent, msgEvent, readEvent): 
    print '[MSG_RECEIVER] rcvMsg thread started\n'
    # Receive/respond loop
    while aliveEvent.is_set():
        print '[MSG_RECEIVER] Waiting to receive message...\n'
        Body.body, masterAddr = sock.recvfrom(1024)
        
        msgEvent.set()
        readEvent.wait()
        readEvent.clear()

        print '[MSG_RECEIVER] Received %s bytes from %s\n' %\
            (len(Body.body), masterAddr)

        print '[MSG_RECEIVER] Sending reply to', masterAddr, '\n'
        sock.sendto(Reply.reply, masterAddr)
        Reply.reply = ""
    print '[MSG_RECEIVER] rcvMsg thread ended\n'

def getBody():
    return Body.body

def setReply(reply):
    Reply.reply = reply

