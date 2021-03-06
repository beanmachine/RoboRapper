import os
import urllib
from inspect import getmembers, isfunction
import urllib2
import random
import requests
import json
import math
import string
import re
import time
import sys
import subprocess
import random 
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

genSong(lines, song, 3, [])

#genSong(lines, chorus, 1, [])
#genSong(lines, song, 16, chorus)

for line in song:
    line = line + ".. "
    filter(lambda x: x in string.printable, line)

"""
for i in range(0, len(song)):
    print song[i]
    if (i+1)%4 == 0:
        print ""
"""
#engine = pyttsx.init('espeak', True)

secondsPerLine = 6.0 
linesPerMinute = 96.0/secondsPerLine

#print engine.getProperty('voice')
with open(os.devnull, "w") as fnull:
    for i in range(0, len(song)):
        wordLen =len(song[i].split(' '))


        subprocess.call(['espeak',
                '"'+song[i] + '" ',
                '-p 10 ',
                '-venglish-us',
                '-s ' + str(int(linesPerMinute*wordLen)) + ' ',
                '-woutwav/_' + str(i) + '.wav'
                ])

        subprocess.call(['lame',
                '-h',
                'outwav/_' + str(i) + '.wav',
                'outwav/_' + str(i) + '.mp3'],
                stdout = fnull,
                stderr = fnull
                )

stichCmd = ['cat']
for i in xrange(len(song)):
   stichCmd.append('outwav/_' + str(i) + '.mp3')

rhash = random.getrandbits(128)
fname ='inter_'+str(rhash)+'.mp3'
fname2 = 'final_' + str(random.getrandbits(128))+'.mp3'
target = open(fname, 'w')
subprocess.call(stichCmd, stdout=target)
target.close()
print ['./padder.sh', ' '+fname, ' '+fname2]
subprocess.call(['./padder.sh', 
                 fname,
                 fname2]);

#subprocess.call(["rm", "outwav/*"])

print json.dumps({'fname':fname2,
            'lines':song})
#    print wordLen
#    engine.setProperty('voice', engine.getProperty('voices')[i % len(engine.getProperty('voices'))].id)
#    engine.setProperty('voice', engine.getProperty('voices')[15].id)
#    engine.setProperty('rate', int(linesPerMinute*wordLen))
#    engine.say(song[i])
#    print song[i], engine.getProperty('voices')[15].id


#engine.runAndWait()
