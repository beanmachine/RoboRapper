import urllib
import urllib2
import random
import requests
import math
import string
import re
import time
import sys
import pyttsx
import subprocess
import copy
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

song = [
"Eastside, we got one",
"Uhh, got a hundred on the dash, young",
"Hot where i'm from, the newscasters don't come",
"Turned himself in, i had to find that dumb",
"Ain't nothing but another calculated schemes",
"Indeed, the flow raw just the same as my levi jeans",
"We all dream one day we be kings and queens",
"But all she ever want me to do is unzip her jeans",
"So when I diss you wouldn't want to answer this",
"He's in it for the sportrunnin circles round his",
"So she went across the street, gave him a kiss",
"That's flyer than a wrestler, you don't want to mess with",
"When my people are down so they can screw us around",
"Wrap around 'til they hit the ground and they hear a sound",
"Told me mary was a go so we passed her round and round",
"And me and them rappers we don't share no common ground",
"Said you wasn't civilized and stole your name",
"Everything was picture perfect till you moved the frame",
"My pistols represent mebust until my rounds emptyback for the street fame",
"These girls all aboard, this young money trainhaving since fame shit'll never be the same",
"Cause some time has passed seem you all forget",
"You know if you was harder than me then you'd be lead",
"- or i'mma fuckin' put this gun in your fuckin' head",
"The king of comedy heard everythin' that you said",
"I love you",
"Wolf gang, triple six crew",
"I call em up, they might fall through",
"But i love my babies too",
"When my people are down so they can screw us around",
"Wrap around 'til they hit the ground and they hear a sound",
"Told me mary was a go so we passed her round and round",
"And me and them rappers we don't share no common ground",
"Okay, I'm going to attempt to drown myself",
"Bitch, don't mess this up for yourself",
"Yeah, that there is a fight in itself",
"So, just tell me something about yourself",
"The crazy thing about it",
"And california on that jerk shit",
"Then the gun shot, but i wasn't hit",
"Young money motherfucker we the shit",
"My nerves hurt and lately I'm on edge",
"Your friends say, why we not together yet",
"Kinda pop tart, when i bite into them red",
"Y'all test like professors, you can get ahead",
"When my people are down so they can screw us around",
"Wrap around 'til they hit the ground and they hear a sound",
"Told me mary was a go so we passed her round and round",
"And me and them rappers we don't share no common ground",
"That I just severed a main vein",
"Straight shots don't toast champagne",
"Imma make it rain",
"Love turns into pain",
"A premature birth that was four minutes late",
"Yeah, i think i'mma cop me that new estate",
"When i saw that 28 to put me in and out of state",
"And we gonnna toast up for the niggas that hate",
"Cause I'm so high, talkin I'm so fly",
"I'm touching skies, no puffing lie",
"You know i want a piece of that pie",
"One choke of this you a note from mariah high",
"When my people are down so they can screw us around",
"Wrap around 'til they hit the ground and they hear a sound",
"Told me mary was a go so we passed her round and round",
"And me and them rappers we don't share no common ground",
]



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
         )

stichCmd = ['cat']
for i in xrange(len(song)):
   stichCmd.append('outwav/_' + str(i) + '.mp3')

target = open('outwav/final.mp3', 'w')
subprocess.call(stichCmd, stdout=target)
target.close()
#    engine.setProperty('voice', engine.getProperty('voices')[15].id)
#    engine.setProperty('rate', int(linesPerMinute*wordLen))
#    engine.say(song[i])
#    print song[i], engine.getProperty('voices')[15].id

#engine.runAndWait()
