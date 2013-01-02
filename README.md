WeMo
====

`wemo.py` contains a simple Python class for the [Belkin WeMo](http://www.amazon.com/gp/product/B0089WFPRO/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&tag=snosrap02-20&linkCode=as2&camp=1789&creative=9325&creativeASIN=B0089WFPRO) device.  It uses Miranda for UPnP.

Files
=====
* `wemo.py` - The main class, supports turning the outlet on/off as well as changing the device's name.  Running `python wemo.py` lists WeMos on the network along with their `binaryState` (on/off).
* `miranda.py` - A slightly modified version of the [miranda](http://code.google.com/p/miranda-upnp/) client.

Sample Usage
============

	$ python
	>>> from wemo import *
	>>> 
	>>> wemos = search()
	>>> for wemo in wemos:
	...     print wemo.binaryState, "\t", wemo.friendlyName
	... 
	True 	Master Bedroom
	False 	Kitchen
	True 	Staircase
	>>> 
	>>> w = wemos[0]
	>>> w.binaryState = False
	>>> w.binaryState = True
	>>> w.binaryState = not w.binaryState
	>>> 

