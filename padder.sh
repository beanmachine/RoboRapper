#!/bin/bash
ffmpeg -i concat:"silence.mp3|$1" -codec copy $2 
