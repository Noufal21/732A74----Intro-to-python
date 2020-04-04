#!/usr/bin/env python3
import sys
import os
import string
from itertools import islice
from itertools import groupby
import operator
from collections import Counter
import string

output_file = False
wholeBooks = ""
out_file = ""
out_AsFile = False
WordCount = 0
UniqueWord = 0

def read_file(path):
    with open(path) as file:
        textData = file.read()
        return textData

def tokenize(book):
    # tokenize the books like covert the string to the list and all the words are in lower case
    if book is not None:
        words = book.lower().split()
        words = [x for x in words if x] #list(filter(bool,words))
        return words
    else:
        return None

# Clean the text and remove all types of special character 
# printable is the list of all the character which is in simple ASCII.
def clean_text(word,printable):
    word = word.replace(",","")
    word =  word.replace(".","")
    word =  word.replace(" ","")
    word =  word.replace("?","")
    word =  word.replace(";","")
    word =  word.replace("!","")
    word =  word.replace("[","")
    word =  word.replace("]","")
    word =  word.replace("'","")
    word =  word.replace('"',"")
    word =  word.replace("-","")
    word =  word.replace("_","")
    word =  word.replace(":","")
    word = list(filter(lambda x: x in printable, word))
    word = ''.join(word)
    return word

#get the next occupance word after cleaning it.
def get_nextWord(words, index,printable):
    nextWord = words[index + 1]
    nextWord = clean_text(nextWord,printable)
    # this is kind of definition of the word it must be greater than or equal 2 character. if not get the next word form the txt file 
    if not nextWord  or nextWord == " " or nextWord == "" or len(nextWord) < 2:
        return get_nextWord(words,index+1,printable)
    # check whether it is integer or not. trying to remove the page number or chapter number.
    try:
        int(nextWord)
        return get_nextWord(words,index+1,printable)
    except ValueError:
        pass
    return nextWord

#calculate the alphabets[a-z] in the file and their frequency 
def calculateAlpha(bookWords):
    alphaHashTable = dict.fromkeys(string.ascii_lowercase, 0)
    for word in bookWords:
        for char in word:
            if char in alphaHashTable:
                alphaHashTable[char] = alphaHashTable[char] + 1
    return alphaHashTable


# this is the main function which create the basic data structure. As the whole code is functional based . I dont think it is a good idea to 
#initialize one big data base for the whole thing. It is better to convert this in OOP and then assigning the whole big database make sense.
def map_words(words):
    global WordCount
    hashTable = {}
    printable = set(string.printable)
    if words is not  None:
        for  index , word in enumerate(words):
            # cleaning the whole file.
            temp = word.replace(",","")
            temp =  temp.replace(".","")
            temp =  temp.replace(" ","")
            temp =  temp.replace("?","")
            temp =  temp.replace(";","")
            temp =  temp.replace("!","")
            temp =  temp.replace("[","")
            temp =  temp.replace("]","")
            temp =  temp.replace("'","")
            temp =  temp.replace('"',"")
            temp =  temp.replace('_',"")
            temp =  temp.replace('-',"")
            temp =  temp.replace(':',"")
            temp = list(filter(lambda x: x in printable, temp))
            temp = ''.join(temp)
            temp =  ''.join(e for e in temp if e.isalnum())
            if not temp  or temp == " " or temp == "" or len(temp) < 2:
                continue
            try:
                int(temp)
                continue
            except ValueError:
                pass
            # calculating the total number of words in the file
            WordCount = WordCount + 1

            # fetching the next followed word
            nextWord = ""
            if len(words)-1 > index:   
                #nextWord = clean_text(words[index+1],printable)
                nextWord = get_nextWord(words,index,printable)
                #print(nextWord)   
            
            # update the hashTable (dic) the structure of this dictionary is {key:word,value: (frequency,[followedWords]})}
            #{key:word,value: (frequency,[followedWords])} in other words dic<string,tuple<int,list>>
            # the reason I am making one big list is that I have write the minimun code for generate txt or to print anything.
            # I parse the whole file at once and I think this is a assumption to parse the whole file at once and you can do anything with it afterwards.
            if temp in hashTable:
                Frequency, followWord = hashTable[temp]
                #print("before adding anything {} in {}".format(followWord,temp))
                Frequency = Frequency +1
                # next word is present
                if  nextWord or nextWord != "" :
                    # make a tuple and add it
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

# calculate the frequency of the followed word just lke the mapped function but here there is no need to clean it 
# bcoz I already clean the followed word in the mapped function. (The perks of parsing the whole file at once)
def getOccurrence(followedWord_list):
    hashTable = {}
    for word in followedWord_list:
        if word  in hashTable:
            hashTable[word]  =hashTable[word]  + 1
        else:
             hashTable[word] = 1
    return hashTable

# simple Print function on console
def  print_mappedWords(mappedWords,followedWord,alphaDic_sorted):
    print(f"Total Number of words in the file : {WordCount}.\n")
    print(f"Total Number of unique words : {UniqueWord}.\n")
    print("{:<8}  \n".format('TOP 5 Words'))

    for (k, v) in mappedWords:
        print("{:<8} \n".format(k))
        frequency_Key = getOccurrence(v[1])
        followedWord = sortResult_dic_simple(frequency_Key)
        print('----------------------------------\n')
        print('Followed Word Frequency "my" \n')
        print ("{:<8} \t {:<20}\n".format('Words','Frequency'))
        [ print( "{:<8} \t {:<25} \n".format(k, v)) for (k, v) in  followedWord[0:5]]
        print("------------------------------------------\n")
    
    print("------------------------------\n")
    print("Alphabet Frequency\n")
    print("{:<8} \t {:<8} \n".format("Key" , "Frequency"))
    for (k,v) in alphaDic_sorted:
        print("{:<8} \t {:<8} \n".format(k, v))


    

# simple Print function on file
def write_mappedWords(filename,mappedWords,followedWord,alphaDic_sorted):
    with open(filename,"w")  as file:
        file.write(f"Total Number of words in the file : {WordCount} \n")
        file.write(f"Total Number of unique words : {UniqueWord} \n")
        file.write ("{:<8}  \n".format('TOP 5 Words'))

        for (k, v) in mappedWords:
            file.write("{:<8} \n".format(k))
            frequency_Key = getOccurrence(v[1])
            followedWord = sortResult_dic_simple(frequency_Key)
            file.write('----------------------------------\n')
            file.write(f'Followed Word Frequency  " {k} " \n')
            file.write ("{:<8} \t {:<20}\n".format('Words','Frequency'))
            [file.write( "{:<8} \t {:<25} \n".format(k, v)) for (k, v) in  followedWord[0:5]]
            file.write("------------------------------------------\n")
        
        file.write("------------------------------\n")
        file.write("Alphabet Frequency\n")
        file.write("{:<8} \t {:<8} \n".format("Key" , "Frequency"))
        for (k,v) in alphaDic_sorted:
            file.write("{:<8} \t {:<8} \n".format(k, v))

        
# sort this {key:word,value: (frequency,[followedWords])} in other words dic<string,tuple<int,list>>
# depending of the frequency
def sortResult_dic(dic_words):
    sorted_Tuple= sorted(dic_words.items(),key=lambda item: item[1][0],reverse=True)
    return sorted_Tuple
# sort this {key:word,value: frequency} in other words dic<string,int>
# depending of the frequency
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
        UniqueWord = len(mapBooked)
        mapBooked_sorted = sortResult_dic(mapBooked)
        alphaDic = calculateAlpha(bookWords)
        alphaDic_sorted = sortResult_dic_simple(alphaDic)
        if out_AsFile:
            write_mappedWords(out_file,take(5,mapBooked_sorted),mapBooked,alphaDic_sorted)
            
        else:
            print_mappedWords(take(5,mapBooked_sorted),mapBooked,alphaDic_sorted)

        #print("File length {count}".format(count = len(wholeBooks)))
    else:
        print("The file doesn't exit!")
