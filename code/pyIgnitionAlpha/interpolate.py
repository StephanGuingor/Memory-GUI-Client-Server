### EXESOFT PYIGNITION ###
# Copyright David Barker 2010
# 
# Utility module for interpolating between keyframed values

import math


def LinearInterpolate(val1, val2, t):
	diff = val2 - val1
	dist = float(diff) * t
	
	return val1 + dist

def CosineInterpolate(val1, val2, t):
	amplitude = float(val2 - val1)
	midpoint = float(val1 + val2) / 2.0
	
	return (amplitude * math.cos(math.pi * (1.0 - t))) + midpoint


def LinearInterpolateKeyframes(curframe, key1, key2, val1, val2):
	if key1 == key2:
		return val2
	
	factor = float(curframe - key1) / float(key2 - key1)
	
	return LinearInterpolate(val1, val2, factor)

def CosineInterpolateKeyframes(curframe, key1, key2, val1, val2):
	if key1 == key2:
		return val2
	
	factor = float(curframe - key1) / float(key2 - key1)
	
	return CosineInterpolate(val1, val2, factor)