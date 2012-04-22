#!/usr/bin/env python
import os, eZ430

from Xlib import X, display, ext
import time
import math

#setup X11
d = display.Display()
s = d.screen()
root = s.root

MAXX = d.screen().width_in_pixels
MAXY = d.screen().height_in_pixels
x=MAXX/2
y=MAXY/2

def twos_comp(val, bits=8):
    """compute the 2's compliment of int value val"""
    if( (val&(1<<(bits-1))) != 0 ):
        val = val - (1<<bits)
    return val

def find_button(key):
	if key == 17:
		return 1
	elif key == 33:
		return 2
	elif key == 49:
		return 3
	else:
		return 0

curr_button = 0

watch = eZ430.watch()
print "Opening eZ430 on",watch.dev
while 1:
	data = watch.read(7)
	read_y=twos_comp(ord(data[0]))
	read_x=twos_comp(ord(data[1]))
	
	pressed = find_button(ord(data[6]))
	if curr_button != pressed:
		#print 'Got button {} (previous {})'.format(pressed, curr_button)
		if curr_button > 0:
			ext.xtest.fake_input(d, X.ButtonRelease, curr_button)
		if pressed > 0:
			ext.xtest.fake_input(d, X.ButtonPress, pressed)
		curr_button = pressed
	
	read_str = ', '.join([ str(ord(x)) for x in data ])
	#print 'Read: {}'.format(read_str)
	
	pointer = root.query_pointer()
	
	x = pointer.root_x + ( (read_x ** 3 ) / 2550 )
	y = pointer.root_y + ( (read_y ** 3 ) / 2550 )
	
	#print 'New Values x: {}\ty: {}'.format(x, y)
	
	root.warp_pointer(x, y)
	d.sync()
	time.sleep(1/40)
