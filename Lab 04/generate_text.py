#!/usr/bin/env python3
import text_stats
import os
import sys
import random
import math

wholeBooks = ""
givenWord = ""
Number_Words = 0
NewTxtList = []


# select one random word depending on the weights
def selectText(words, weight):
    msg = ''
    selectWord = random.choices(words,weights = weight, k = 1)#Number_Words)
    #msg = ' '.join(selectWord)
    #return msg
    return str(selectWord[0])
# genetate list of words
# Simple Algo
# First given_word is get as an input like "king"
# calculating the frequency from getOccurrence in text_stats.py
# get the next random word from selectText using weights.
# now choice that nextWord as a given_word and repeat the process until you generate the list of forexample 500 words i.e also an input from the user.
def generateText(mapped_words,given_word,remainingWords):
    if remainingWords <= 0:
        return NewTxtList
    # calcualte the freq of all the followed words
    frequency_Key = text_stats.getOccurrence(mapped_words[given_word][1])
    totalSum = mapBooked[givenWord][0]
    # Normalized the the freq of all the followed words in the range of [0-1]
    normalized_frequency_Key_sorted = {key:float(val)/totalSum for key, val in frequency_Key.items()}
    normalized_frequency_Key_sorted = text_stats.sortResult_dic_simple(normalized_frequency_Key_sorted)
    words =  [a_tuple[0] for a_tuple in normalized_frequency_Key_sorted]
    weight = [a_tuple[1] for a_tuple in normalized_frequency_Key_sorted]
    #fetch any random word from the list 
    nextWord = selectText(words,weight)
    NewTxtList.append(nextWord)
    #repeat the same process again but now the given_word is the newly generated random word
    generateText(mapped_words,nextWord,remainingWords-1)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit()

    givenWord  = sys.argv[2]
    Number_Words = int(sys.argv[3])   

    if os.path.isfile(sys.argv[1]):
        wholeBooks = text_stats.read_file(sys.argv[1])
        bookWords =  text_stats.tokenize(wholeBooks)
        mapBooked = text_stats.map_words(bookWords)
        mapBooked_sorted = text_stats.sortResult_dic(mapBooked)
        NewTxtList = []
        generateText(mapBooked,givenWord,Number_Words)
        generated = ' '.join(NewTxtList)
        print(generated)


