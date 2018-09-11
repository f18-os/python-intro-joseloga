#! /usr/bin/env python3

import os, sys, time, re

inputs=""
while inputs != "quit":
    inputs= input("insert Command:")
    if inputs == "quit":
        sys.exit(0) 
    pid = os.getpid()               # get and remember pid
#    os.write(1, ("About to fork (pid=%d)\n" % pid).encode())
    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:                   # child
#        os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
#                     (os.getpid(), pid)).encode())
        args = inputs.split(' ')
    
        if '>' in args:
            outputText= args[args.index('>')+1:]
            args= args[0:args.index('>')]
            
            print(outputText)
#            print("> detected")
            os.close(1)                 # redirect child's stdout
            sys.stdin = open(outputText[0], "w")
            fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)
            os.set_inheritable(fd, True)
            os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())
            
        if '<' in args:
            outputText= args[args.index('<')+1:]
            args= args[0:args.index('<')]
            args.append(outputText[0])
#            print(args)

        for dir in re.split(":", os.environ['PATH']): # try each directory in path
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly 

        os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
        sys.exit(1)                 # terminate with error
        
    else:                           # parent (forked ok)
#        os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
#                     (pid, rc)).encode())
        childPidCode = os.wait()
#        os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
#                     childPidCode).encode())
#   wc shell.py > new.txt