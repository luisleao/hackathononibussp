import sys
import os
import json
import pyes, pprint
import codecs


from datetime import datetime
from os import listdir
from StringIO import StringIO



listas = {}


file_trips = "../amostra/SPTrans GTFS/trips.txt"

with codecs.open(file_trips, 'r', encoding='iso-8859-1') as raw:	
	#with open(decoded_file, 'r') as raw:
	for a in raw.readlines()[1:]:
		b = a.replace('\r\n', '').split(',')
		print b

		id = b[0]
		if not listas.has_key(id):
			listas[id] = {
				"id": id,
				
			}

		item = listas[id]



print "*** FIM ***"


