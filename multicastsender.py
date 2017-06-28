import socket
import struct
import sys

mCastGrpAddr = '224.1.1.1'
mCastPort = 5007
mCastGroup = (mCastGrpAddr, mCastPort)

def configMulticastSock():
    # Create the datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Set socket time to live 
    # Setting 1 keeps the packet in the local network segment.
    ttl = struct.pack('b', 1)

    # Set options
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    # Set a timeout so the socket does not block indefinitely when trying
    # to receive data.
    sock.settimeout(1)
    return sock

def sendMsgToSlaves(body, sock):  
    # Send data to the multicast group
    print >>sys.stderr, '    Sending "%s" to slaves' % body
    sent = sock.sendto(body, mCastGroup)

    # Look for responses from all recipients
    print >>sys.stderr, '    Responses from slaves: '
    while True:
        try:
            response, slaveAddr = sock.recvfrom(1024)
        except socket.timeout:
            print >>sys.stderr, '    Timed out, no more responses'
            break
        else:
            print >>sys.stderr, '    Received "%s" from slave %s' %\
                (response, slaveAddr)

