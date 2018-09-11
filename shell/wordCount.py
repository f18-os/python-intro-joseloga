import os         # checking if file exists
import sys        # command line arguments
import csv        # write dictionary to txt file
import re 
from collections import Counter

textFile=  sys.argv[1]
readFile=  open(textFile,"r")
outputFile=  open("OutputFile.txt","w+")

#read text from files and creates a list with all the words
def collectWords():
 
    asList = []
    bsList = []

    #checking if the text file exist
    if not os.path.exists(textFile):
        print ("text file input %s doesn't exist! Exiting" % textFname)
        exit()
    
#    print("reading File....")
    if readFile.mode == "r":
        asList = re.sub('\W+', ' ',readFile.read()).split()
        readFile.close()
        print("Filtering words...")
        for word in asList:
            word = editWord(word)
            insertWord(word, bsList)
            
        bsList= sorted(bsList)

        return bsList
            
            
#read words and deletes special characters
def editWord(word ):
    word = word.lower()
#    print(word)
    
    return word


#count how many times a word appears
def countWords(dictionary):
    counter= Counter(dictionary)
    return counter


#insert words to a list
def insertWord(word, dictionary):
    
    word=word.strip()
    if '-' in word:
        x=word.split('-')
        for item in x:
            item=editWord(item)
            dictionary.append(item)
            print(item)    
    elif "'" in word:
        x=word.split("'")
        for item in x:
            item=editWord(item)
            dictionary.append(item)
#                        print(item)            
    else:
#                    print("d")    
        dictionary.append(word)
    
    
    
#
#copy a dictionary to a txt file
def writeToFile(dictionary):
    print("writing to output file...")
    wr= csv.writer(outputFile,delimiter=" ")
    wr.writerows( dictionary.items())
    

#print list
def printList(dictionary):
#    for item in dictionary:
#        print(item, sep="\n")
    for key, value in dictionary.items():
        print(key,value)



def main():
    wordList =  collectWords();
#    printList(wordList);
    dictionary = countWords(wordList)
#    printList(dictionary);
    writeToFile(dictionary)
    
    
main();            