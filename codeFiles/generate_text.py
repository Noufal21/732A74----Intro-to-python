#!/usr/bin/env python3
import text_stats
import os
import sys
import random
import math

wholeBooks = ""
givenWord = ""
Number_Words = 0




def generateText(words, weight):
    msg = ''
    selectWord = random.choices(words,weights = weight, k = Number_Words)
    msg = ' '.join(selectWord)
    return msg




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
        frequency_Key = text_stats.printOccurance(mapBooked[givenWord][1])
        frequency_Key_sorted = text_stats.sortResult_dic_simple(frequency_Key)
        print(Number_Words)
        totalSum = mapBooked[givenWord][0]
        #print(mapBooked)
        normalized_frequency_Key_sorted = {key:float(val)/totalSum for key, val in frequency_Key.items()}
        normalized_frequency_Key_sorted = text_stats.sortResult_dic_simple(normalized_frequency_Key_sorted)
        words =  [a_tuple[0] for a_tuple in normalized_frequency_Key_sorted]
        weight = [a_tuple[1] for a_tuple in normalized_frequency_Key_sorted]
        generated = generateText(words,weight)
        print(generated)


