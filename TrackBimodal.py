'''
Created on Oct 1, 2013

@author: Alan

Takes as input the {0}_track.txt file generated by an OpinionPropagation.py experiment.
Prints out a list of final opinion distributions that are bimodal (along with identifying 
information for their experiment parameters)  
'''
#import fileinput
import re
import sys
import math

INPUT_DIR = "C:\\Users\\Alan\\workspace\\OpinionPropagation\\opinion_prop\\"
INPUT_EXPR = sys.argv[1]
INPUT_SUFFIX = "_track.txt"
INPUT_FILE = INPUT_DIR + INPUT_EXPR + INPUT_SUFFIX

filein = open(INPUT_FILE,'r')

curr_exprline = None
last_words = None

THRESHOLD = 20 # a local maxima must have value at least this much

def isBimodal(hist):
    '''
    Checks if a given histogram (list of integers) is a bimodal distribution
    '''
    localMaxes = getLocalMaxima(hist,threshold=THRESHOLD)
    if len(localMaxes) <= 1:
        return False
    
    for i in localMaxes:
        for j in localMaxes:
            if i == j:
                continue
            else:
                if containsValley(hist,i,j):
                    return True
    return False


def getLocalMaxima(hist,threshold=0):
    '''
    Returns the indices of the local maxima
    '''
    ret = []
    for i in range(len(hist)):
        if i == 0:
            if hist[1] < hist[0] and hist[i]>=threshold:
                ret.append(i)
        elif i == len(hist)-1:
            if hist[-1] > hist[-2] and hist[i]>=threshold:
                ret.append(i)
        else:
            if hist[i] >= hist[i-1] and hist[i] > hist[i+1] and hist[i]>=threshold:
                ret.append(i)
    return ret

def containsValley(hist,i,j):
    '''
    Returns true only if there is a bucket between i and j that has value at most half of the 
    smaller of the two
    '''
    bar = math.floor(min(hist[i],hist[j])/2)
    for m in range(i+1,j):
        if hist[m] <= bar:
            return True
    return False
        
count=0
for line in filein:
    if curr_exprline == None:
        curr_exprline = line
    elif re.match("^m",line):
        ####
        last_words = last_words[0:20]
        last_words = list(map(int,last_words))
        if isBimodal(last_words):
            print(curr_exprline," -> ",list(last_words))
        else:
            count = count+1
        ####
        
        curr_exprline = line
    elif re.match("^[^\W]+\W+[^\W]+\W+",line):
        last_words = re.split("\W+", line)
    else:
        print ("NO MATCH : {0}".format(line))

####
last_words = last_words[0:20]
last_words = list(map(int,last_words))
if isBimodal(last_words):
    print(curr_exprline," -> ",list(last_words))
####

print(count," unimodals read")
