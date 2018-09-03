import os         # checking if file exists
import sys        # command line arguments
import csv
from collections import Counter
    
#read text from files
def readFile():
    
    textFile=  sys.argv[1]
    readFile=  open(textFile,"r")
    outputFile=  open("OutputFile.txt","w+")
    asList = []
    dictionary= []
        
    #checking if the text file exist
    if not os.path.exists(textFile):
        print ("text file input %s doesn't exist! Exiting" % textFname)
        exit()
    
    print("reading File....")
    if readFile.mode == "r":
            asList = readFile.read().split()
      
            print("Filtering words...")
            for word in asList:
                word = editWord(word)
                if '-' in word:
                    x=word.split('-')
                    for item in x:
                        item=editWord(item)
                        dictionary.append(item)
#                        print(item)    
                elif "'" in word:
                    x=word.split("'")
                    for item in x:
                        item=editWord(item)
                        dictionary.append(item)
#                        print(item)            
                else:
#                    print("d")    
                    dictionary.append(word)
                
                    
#            print(dictionary, sep='\n')
            
            dictionary= sorted(dictionary)
            dictionary.pop(0)
            counter= Counter(dictionary)
#            for key, value in counter.items():
#                print(key,value)
            
            print("writing to output file...")
            wr= csv.writer(outputFile,delimiter=" ")
            wr.writerows( counter.items())
            

def editWord(word ):
    word = word.lower()
#    word = word.replace(' ', '')
    word = word.replace(',', '')
    word = word.replace('.', '')
    word = word.replace(';', '')
    word = word.replace(':', '')
    if word.isspace():
        print (word,"is only spaces")
    
    return word


def main():
    readFile();
    

main();            