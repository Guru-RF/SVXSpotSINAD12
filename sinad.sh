#!/bin/bash

while true; do
	touch input.wav
	rm input.wav 

	arecord -d 5 -f S16_LE -r 44100 -c 1 input.wav
	python sinad12.py
	rm input.wav 
done
