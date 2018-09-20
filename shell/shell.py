#! /usr/bin/env python3

import os, sys, time, re

inputs=""
library=["cd"]

def parent():
    childPidCode = os.wait()
    if os.path.isfile("aux"):
        os.remove("aux")

def callProgram(args):
    for dir in re.split(":", os.environ['PATH']): # try each directory in path
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ) # try to exec program
        except FileNotFoundError:             # ...expected
            pass                              # ...fail quietly
    os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
    sys.exit(1)

def child(args):
    if '>' in args:
        outputText= args[args.index('>')+1:]
        args= args[0:args.index('>')]
        print(outputText)
        os.close(1)                 # redirect child's stdout
        sys.stdin = open(outputText[0], "w")
        fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)
        os.set_inheritable(fd, True)
        os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())

    if '<' in args:
        outputText= args[args.index('<')+1:]
        args= args[0:args.index('<')]
        args.append(outputText[0])

    if '|' in args:
                rightPipe= args[args.index('|')+1:]
                leftPipe= args[0:args.index('|')]
                args=rightPipe
                print(* args, sep=" ")
                print("pipe mode")
                np= os.fork()
                os.close()

                if np <0:
                    os.write(2, ("fork failed, returning %d\n" % rc).encode())
                    sys.exit(1)

                if np == 0:  # new child
                    os.close(1)                 # redirect child's stdout
                    sys.stdout = open("aux", "w")
                    fd = sys.stdout.fileno() # os.open("p4-output.txt", os.O_CREAT)
                    os.set_inheritable(fd, True)
                    print("====================================")
                    print(*leftPipe, sep=" ")

                    callProgram(leftPipe)
                else:           # second parent
                    print(* rightPipe, sep="->")
                    childPidCode2 = os.wait()
                    os.close(0)                 # redirect child's stdout
                    sys.stdin = open("aux", "r")
                    fd = sys.stdin.fileno() # os.open("p4-output.txt", os.O_CREAT)
                    os.set_inheritable(fd, True)
                    callProgram(rightPipe)
    callProgram(args)

while inputs != "quit":

    try:
        os.environ["PS1"]= "[lacutie@Shell]─["+os.getcwd()+"] $"
        inputs= input(os.environ["PS1"])
    except EOFError:
        print("")
        break

    if inputs == "quit" :
        sys.exit(0)

    pid = os.getpid()               # get and remember pid
    args = inputs.split(" ")
    if not args[0]:                 # Check if list is empty
        # print("====================")
        args.pop(0)

    if args[0] in library:
        if "cd" in args:
            os.chdir("/home/")


    else:
        rc = os.fork()
        if rc < 0:
            os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)                                                           # parent error

        elif rc == 0:                   # child
            child(args)
        else:                           # parent (forked ok)
            parent()
