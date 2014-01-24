import mp3play

filename = r'bplease2.mp3'
clip = mp3play.load(filename)

clip.play()

import time
time.sleep(min(30, clip.seconds()))
clip.stop()
