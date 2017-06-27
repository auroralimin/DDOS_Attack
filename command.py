print "===== Welcome to DDOS Attacker====="
print "Please command your attack or try --help for more information"

while 1:
    line = raw_input("> ")
    line = line.lower()
    words = line.split(' ')

    if len(words) < 1:
        print "Invalid command. For more information, try --help"
        continue

    if words[0] == 'syn-flood':
        print "syn-flood"
    elif words[0] == 'http-post':
        print "http-post"
    elif words[0] == '--help':
        print "Please inform <attack type> <flags>"
        print "\nValid attack types:"
        print "    syn-flood"
        print "    http-post"
        print "\n Valid flags:"
        print "    -start"
        print "    -stop"
        print "    -time <[int] attack period in ms>"
        continue
    else:
        print "Invalid command. For more information, try --help"
        continue

    if len(words) < 2:
        print "Please inform flags. For more information, try --help"
        continue
    if words[1] == '-start':
        print "-start"
    elif words[1] == '-stop':
        print "-stop"
    elif (words[1] == '-time') & (len(words) > 2):
        try:
            print "-time %s" % (int(words[2]))
        except ValueError:
            print "Invalid time value. For more information, try --help"
            continue
    else:
        print "Invalid flag. For more information, try --help"

