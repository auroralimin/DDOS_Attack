import socket
import struct
import sys

#TODO: thread a ser implementada em cada servo
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

# Receive/respond loop
while True:
    print >>sys.stderr, '\nwaiting to receive message'
    body, masterAddr = sock.recvfrom(1024)
    
    print >>sys.stderr, 'received %s bytes from %s' % (len(body), masterAddr)
    print >>sys.stderr, body

    print >>sys.stderr, 'sending acknowledgement to', masterAddr
    sock.sendto('ack', masterAddr)

