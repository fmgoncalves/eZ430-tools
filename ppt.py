#!/usr/bin/env python
import os, eZ430

from Xlib import X, display, ext, XK
import time

verbose = 1
watch = eZ430.watch()


if verbose: print "Opening eZ430 on",watch.dev

d = display.Display()
print 

def find_key(key):
	if key == 18:
		return d.keysym_to_keycode(XK.string_to_keysym('Left'))
	elif key == 50:
		return d.keysym_to_keycode(XK.string_to_keysym('Right'))
	elif key == 34:
		return d.keysym_to_keycode(XK.string_to_keysym('Home'))
	else:
		return 0

curr_key = 0

while 1:
	data = watch.read(7)
	pressed = find_key(ord(data[6]))
	if pressed != curr_key:
		watch.debounce()
		watch.debounce()
		if curr_key > 0:
			ext.xtest.fake_input(d, X.KeyRelease, curr_key)
		if pressed > 0:
			ext.xtest.fake_input(d, X.KeyPress, pressed)
		curr_key = pressed
	d.sync()
	time.sleep(1/20)
