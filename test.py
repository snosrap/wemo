from wemo import *

wemos = search()
for wemo in wemos:
	print wemo.binaryState, wemo.friendlyName
