from random import randint
import re

def getRandomInt(size):
    return randint(0, size - 1)

def getRandomTuple(items):
    pos = getRandomInt( len( items ) )
    return items[pos]

def getSplit(text, delimiter_pattern=(',|\\b(or)')):
    return re.split(delimiter_pattern, text)
