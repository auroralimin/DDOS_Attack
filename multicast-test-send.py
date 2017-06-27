import socket
import struct
import sys

mCastGrpAddr = '224.1.1.1'
mCastPort = 5007
mCastGroup = (mCastGrpAddr, mCastPort)

def configMulticastSock():
    # Set socket time to live 
    # Setting 1 keeps the packet in the local network segment.
    ttl = struct.pack('b', 1)

    # Set options
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    # Set a timeout so the socket does not block indefinitely when trying
    # to receive data.
    sock.settimeout(1)

def sendMsgToSlaves(body):  
    # Send data to the multicast group
    print >>sys.stderr, 'sending "%s"' % body
    sent = sock.sendto(body, mCastGroup)

    # Look for responses from all recipients
    while True:
        print >>sys.stderr, 'Responses from slaves: '
        try:
            response, slaveAddr = sock.recvfrom(1024)
        except socket.timeout:
            print >>sys.stderr, 'timed out, no more responses'
            break
        else:
            print >>sys.stderr, 'received "%s" from slave %s' % (response, slaveAddr)

if __name__ == '__main__':
    # Create the datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Config socket for multicast
    configMulticastSock()
    try:
        sendMsgToSlaves("BODY COM OS COMANDOS E TAL")
    finally:
        print >>sys.stderr, 'closing socket'
        sock.close()