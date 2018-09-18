#! /usr/bin/env python3

import os, sys, time, re

inputs=""
library=["cd","ls"]
PS1 = 	os.getcwd()
r, w = os.pipe() 
#print(os.environ.get('PS1'))

while inputs != "quit":
    try:
        print("┌─[lacutie@shell]─[~",os.getcwd(),"]")       
        inputs= input("└──╼ $")
    except EOFError:
        print("")
        break 
        
    if inputs == "quit" :
        sys.exit(0) 
        
    pid = os.getpid()               # get and remember pid
    args = inputs.split(" ")
    if not args[0]: # Check if list is empty
        print("====================")
        args.pop(0)
#    print(* args , sep=" -")

    
    if inputs in library:
        if inputs=="cd":
            os.chdir("/home/lacutie/Documents/")
        if inputs=="ls":
#            print("ls mode")
            files=os.listdir(os.getcwd())
            print (* files, sep="   ",)

   
    else:
        rc = os.fork()


        if rc < 0:
            os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)

        elif rc == 0:                   # child
    #        os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
    #                     (os.getpid(), pid)).encode())


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

            if '|' in args:
                rightPipe= args[args.index('|')+1:]
                leftPipe= args[0:args.index('|')]
                args=rightPipe
                
#                print(* args, sep=" ")      
                print("pipe mode")
                np= os.fork()
                
                
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

                    for dir in re.split(":", os.environ['PATH']): # try each directory in path
                        program = "%s/%s" % (dir, leftPipe[0])
                        try:
                            os.execve(program, leftPipe, os.environ) # try to exec program
                        except FileNotFoundError:             # ...expected
                            pass                              # ...fail quietly 
                    os.write(2, ("Child:    Error: Could not exec %s\n" % leftPipe [0]).encode())
                    sys.exit(1)           
                else:           # second parent 
                    print(* rightPipe, sep="->")  
                    childPidCode2 = os.wait()
                    os.close(0)                 # redirect child's stdout
                    sys.stdin = open("aux", "r")
                    fd = sys.stdin.fileno() # os.open("p4-output.txt", os.O_CREAT)
                    os.set_inheritable(fd, True)
                    for dir in re.split(":", os.environ['PATH']): # try each directory in path
                        program = "%s/%s" % (dir, rightPipe[0])
                        try:
                            os.execve(program, rightPipe, os.environ) # try to exec program
                        except FileNotFoundError:             # ...expected
                            pass                              # ...fail quietly 
                    os.write(2, ("Child:    Error: Could not exec %s\n" % args [0]).encode())
                    sys.exit(1)           
                   
                    
#                    
             
#            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print(* args, sep="->")  
            for dir in re.split(":", os.environ['PATH']): # try each directory in path
                program = "%s/%s" % (dir, args[0])
                try:
                    os.execve(program, args, os.environ) # try to exec program

                except FileNotFoundError:             # ...expected
                    pass                              # ...fail quietly 

            os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
            sys.exit(1)                 # terminate with error

        else:                           # parent (forked ok)
            childPidCode = os.wait()
            os.remove("aux")
#            os.close(w)
#            print(childPidCode)
#           bc#449t5r+it
