#!/usr/bin/env python3
import sys
import os
import string
from itertools import islice
from itertools import groupby
import operator

output_file = False
wholeBooks = ""
out_file = ""
out_AsFile = False

def read_file(path):
    with open(path) as file:
        textData = file.read()
        return textData

def tokenize(book):
    if book is not None:
        words = book.lower().split()
        words = [x for x in words if x] #list(filter(bool,words))
        return words
    else:
        return None

def clean_text(word,printable):
    word = word.replace(",","")
    word =  word.replace(".","")
    word =  word.replace(" ","")
    word =  word.replace("?","")
    word =  word.replace(";","")
    word =  word.replace("!","")
    word =  word.replace("[","")
    word =  word.replace("]","")
    word = list(filter(lambda x: x in printable, word))
    word = ''.join(word)
    return word

def map_words(words):
    hashTable = {}
    printable = set(string.printable)
    if words is not  None:
        for  index , word in enumerate(words):
            temp = word.replace(",","")
            temp =  temp.replace(".","")
            temp =  temp.replace(" ","")
            temp =  temp.replace("?","")
            temp =  temp.replace(";","")
            temp =  temp.replace("!","")
            temp =  temp.replace("[","")
            temp =  temp.replace("]","")
            temp = list(filter(lambda x: x in printable, temp))
            temp = ''.join(temp)
            temp =  ''.join(e for e in temp if e.isalnum())
            if not temp  or temp == " " or temp == "" or len(temp) < 1:
                continue
            try:
                int(temp)
                continue
            except ValueError:
                pass
            nextWord = ""
            if len(words)-1 > index:   
                nextWord = clean_text(words[index+1],printable)
                #print(nextWord)   
            
            if temp in hashTable:
                Frequency, followWord = hashTable[temp]
                #print("before adding anything {} in {}".format(followWord,temp))
                Frequency = Frequency +1
                if  nextWord or nextWord != "" :
                    #print(nextWord)
                    followWord.append(nextWord)
                    #print("adding new value in {} for word {}".format(followWord,temp))
                hashTable[temp] = (Frequency,followWord)
            else:
                if nextWord is not None:
                    hashTable[temp] = (1,[nextWord])
                else:
                    hashTable[temp] = (1,list())
        return hashTable
    else:
        return None    

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return (iterable[:n])

def take_dic(n, iterable):
    "Return first n items of the iterable as a list"
    return dict(iterable.items()[:n])

def printOccurance(followedWord_list):
    hashTable = {}
    for word in followedWord_list:
        if word  in hashTable:
            hashTable[word]  =hashTable[word]  + 1
        else:
             hashTable[word] = 1
    return hashTable


def  print_mappedWords(mappedWords,followedWord):
    print ("{:<8} \t {:<20} \t {} \n".format('Words','Frequency',"Followed Vocab"))

    for (k, v) in mappedWords:
        print( "{:<8} \t {} \t {} \n".format(k, v[0],v[1][0:10]))

    print('----------------------------------\n')
    print('Followed Word Frequency "my" \n')
    print ("{:<8} \t {:<20}\n".format('Words','Frequency'))
    [ print( "{:<8} \t {:<25} \n".format(k, v)) for (k, v) in  followedWord]


def write_mappedWords(filename,mappedWords,followedWord):
    with open(filename,"w")  as file:
        file.write ("{:<8} \t {:<20} \t {} \n".format('Words','Frequency',"Followed Vocab"))

        for (k, v) in mappedWords:
           file.write( "{:<8} \t {} \t {} \n".format(k, v[0],v[1][0:10]))

        file.write('----------------------------------\n')
        file.write('Followed Word Frequency  " my" \n')
        file.write ("{:<8} \t {:<20}\n".format('Words','Frequency'))
        [ file.write( "{:<8} \t {:<25} \n".format(k, v)) for (k, v) in  followedWord]
        
def sortResult_dic(dic_words):
    sorted_Tuple= sorted(dic_words.items(),key=lambda item: item[1][0],reverse=True)
    return sorted_Tuple

def sortResult_dic_simple(dic_words):
    sorted_Tuple= sorted(dic_words.items(),key=lambda item: item[1],reverse=True)
    return sorted_Tuple

if __name__ == "__main__":
    if len(sys.argv) > 3:
        output_file = True

    if len(sys.argv) >= 3 :
        out_file  = sys.argv[2]
        out_AsFile = True

    if os.path.isfile(sys.argv[1]):
        wholeBooks = read_file(sys.argv[1])
        bookWords =  tokenize(wholeBooks)
        mapBooked = map_words(bookWords)
        mapBooked_sorted = sortResult_dic(mapBooked)
        frequency_Key = printOccurance(mapBooked["my"][1])
        frequency_Key_sorted = sortResult_dic_simple(frequency_Key) 
        if out_AsFile:
            write_mappedWords(out_file,take(5,mapBooked_sorted),take(5,frequency_Key_sorted))
            
        else:
            print_mappedWords(take(5,mapBooked_sorted),take(5,frequency_Key_sorted))

        #print("File length {count}".format(count = len(wholeBooks)))
    else:
        print("The file doesn't exit!")
