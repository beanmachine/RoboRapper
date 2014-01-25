import urllib
from inspect import getmembers, isfunction
import urllib2
import random
import requests
import math
import string
import re
import time
import sys
import pyttsx
import copy
import types
from pprint import pprint

table = string.maketrans("","")
url = 'http://rappad.co/rap/freestyle'
lines = []
song = []
chorus = []

def countSyl(word):
    #filters word
    word = re.sub("[\.\t\,\:;\(\)\.]", "", word, 0, 0)
 
    if len(word) == 0:
        return 0
    if word == 'righteus':
        return 2
    if word == 'holes':
        return 1
    if word == 'trying':
        return 2
    if len(word) <= 3:
        return 1
    word = word.replace('(?:[^laeiouy]es|ed|[^laeiouy]e)$', '')
    word = word.replace('^y','')
    vowels = re.findall('[aeiouy]{1,2}', word)
    if len(vowels) > 0:
        return len(vowels)
    else:
        return 1

def genLine(song, count):
    if count == 0:
        return True

    prev = song[len(song) -1]
    syl = countSyl(prev)
    words = prev.split(' ')
    word = words[len(words)-1]

    params = urllib.urlencode({
       'syllables': syl,
       'lastWord': word
    })

    response = requests.post(url, data=params) 
    if response.status_code == 200:
        print response
        js = response.json()
        line = js['line']
        song.append(line)
        return genLine(song, count - 1)
    else: #response failed
        time.sleep(3)
        while(len(song) % 4 != 0):
            del(song[-1])

        return False 

with open('raplines.txt', 'r') as f:
    for line in f:
        lines.append(line)

def genSong(lines, song, count, chorus):
    if count == 0:
        return

    if chorus != [] and (count == 13 or count == 9 or count == 5 or count == 1 ):
        for line in chorus:
            song.append(line)
        count -= 1
    else:
        i = int(math.floor(random.random() * len(lines)))
        line = lines[i].rstrip()
        words = line.split(' ')
        lastWord = words[len(words)-1]
        del(lines[i])
        song.append(line)
        count -= 1
        result = genLine(song, 3)
        if (result == False):
            count += 1

    genSong(lines, song, count, chorus)

genSong(lines, chorus, 1, [])
genSong(lines, song, 16, chorus)

for line in song:
    line = line + ".. "
    filter(lambda x: x in string.printable, line)

for i in range(0, len(song)):
    print song[i]
    if (i+1)%4 == 0:
        print ""

engine = pyttsx.init('espeak', True)

secondsPerLine = 6.0 
linesPerMinute = 96.0/secondsPerLine

#print engine.getProperty('voice')
 
for i in range(0, len(song)):
    wordLen =len(song[i].split(' '))
#    print wordLen
#    engine.setProperty('voice', engine.getProperty('voices')[i % len(engine.getProperty('voices'))].id)
    engine.setProperty('voice', engine.getProperty('voices')[15].id)
    engine.setProperty('rate', int(linesPerMinute*wordLen))
    engine.say(song[i])
#    print song[i], engine.getProperty('voices')[15].id


engine.runAndWait()
