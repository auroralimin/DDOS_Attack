
def check_flags(words):
    if len(words) < 2:
        print "Please inform flags. For more information, try --help"
    elif words[1] == '-start':
        if words[0] == 'syn-flood':
            print "syn-flood -start"
        elif words[1] == 'http-post':
            print "http-post -start"
    elif words[1] == '-stop':
        if words[0] == 'syn-flood':
            print "syn-flood -stop"
        elif words[1] == 'http-post':
            print "http-post -stop"
    elif (words[1] == '-time') & (len(words) > 2):
        try:
            if words[0] == 'syn-flood':
                print "syn-flood -time %s" % (int(words[2]))
            elif words[1] == 'http-post':
                print "http-post -time %s" % (int(words[2]))
        except ValueError:
            print "Invalid time value. For more information, try --help"
    else:
        print "Invalid flag. For more information, try --help"

def init_screen():

    print ("===== Welcome to DDOS Attacker=====")
    print ("Please command your attack or try --help for more information")

    while 1:

        line = raw_input(">>> ")
        line = line.lower()
        words = line.split(' ')

        if len(words) < 1:
            print "Invalid command. For more information, try --help"
            continue

        if words[0] == 'syn-flood':
            check_flags(words)
        elif words[0] == 'http-post':
            check_flags(words)
        elif words[0] == '--help':
            print "Please inform <attack type> <flags>"
            print "\n Valid attack types:"
            print "    syn-flood"
            print "    http-post"
            print "\n Valid flags:"
            print "    -start"
            print "    -stop"
            print "    -time <[int] attack period in ms>"
            print "\n Exit"
            print "    exit()"
            continue
        elif words[0] == 'exit()':
            break
        else:
            print "Invalid command. For more information, try --help"
            continue


if __name__ == '__main__':
    init_screen()