import sys
import os
import json
import pyes, pprint
import codecs

import math

from datetime import datetime, timedelta
from os import listdir
from StringIO import StringIO





def save_file(filename, json_data):
	print "salvando '%s'..." % filename
	with open(filename, "w") as the_file:
		the_file.write(json.dumps(json_data, encoding="utf-8")) #iso-8859-1"))
	print "file saved"


#iso-8859-1





linhas = {}
stop_times = {}
frequencies = {}
shapes = {}





def getTime(val):

	tm1 = map(int, val.split(':')) 
	return timedelta(hours=tm1[0], minutes=tm1[1], seconds=tm1[2])



def get_routes(): #routes.txt
	arquivo = "../amostra/SPTrans GTFS/routes.txt"
	with codecs.open(arquivo, 'r', encoding='UTF-8') as raw:	
		#with open(decoded_file, 'r') as raw:
		for a in raw.readlines()[1:]:
			b = a.replace('\r\n', '').split(',')

			#"route_id","agency_id","route_short_name","route_long_name","route_type","route_color","route_text_color"
			#"1016-10","1","1016-10","Cemiterio Do Horto - Center Norte",3,"",""

			id = b[0].replace("\"", "")
			name = b[3].replace("\"", "")

			if not linhas.has_key(id):
				linhas[id] = {
					"id": id,
					"name": name,
					"sentidos": {},
				}




def get_trips(): #trips.txt
	arquivo = "../amostra/SPTrans GTFS/trips.txt"
	with codecs.open(arquivo, 'r', encoding='UTF-8') as raw:	
		#with open(decoded_file, 'r') as raw:
		for a in raw.readlines()[1:]:
			b = a.replace('\r\n', '').split(',')
			#"route_id","service_id","trip_id","trip_headsign","direction_id","shape_id"
			#"1016-10","USD","1016-10-0","Center Norte",0,42746

			id = b[0].replace("\"", "")
			working = b[1].replace("\"", "")
			name = b[3].replace("\"", "")
			sentido = b[4]
			shape_id = int(b[5])

			if linhas.has_key(id):

				item = linhas[id]
				item["sentidos"][sentido] = {
					"name": name,				#//GTFS:trips - headsign
					"shape_id": shape_id,		#//GTFS:trips - id do shape
					"shapes": None,				#//GTFS:shapes array
					"travel_time": 0,			#//calculo: GTFS:stop_times - tempo de percurso em segundos
					"travel_discance": 0, 		#//calculo: GTFS:shapes - distancia do percurso em metros
					"travels": [0] * 24,  		#//calculo: GTFS:frequencies 00-23h: 3600/headway_secs
					"total_travels": 0,			#//calculo: GTFS:frequencies 00-23h: SUM(3600/headway_secs)
					"working": working			#//GTFS:trips: USD (Util, Sabado, Domingo)
				}



def get_travel_times(): #stop_times.txt
	arquivo = "../amostra/SPTrans GTFS/stop_times.txt"
	with codecs.open(arquivo, 'r', encoding='UTF-8') as raw:	
		#with open(decoded_file, 'r') as raw:
		for a in raw.readlines()[1:]:
			b = a.replace('\r\n', '').split(',')
			#print b

			#"trip_id","arrival_time","departure_time","stop_id","stop_sequence"
			#[u'"978J-10-0"', u'"06:11:54"', u'"06:11:54"', u'410003639', u'8']

			id_completo = b[0].replace("\"", "")
			id = id_completo[0:-2]
			sentido = id_completo[-1:]
			arrival_time = b[1].replace("\"", "")
			departure_time = b[2].replace("\"", "")
			stop_id = b[3]
			stop_sequence = b[4]


			arrival_timestamp = getTime(arrival_time)
			departure_timestamp = getTime(departure_time)


			if not stop_times.has_key(id):
				stop_times[id] = {}

			item = stop_times[id]
			if not item.has_key(sentido):
				item[sentido] = {
					"start": timedelta(),
					"stop": timedelta(),
					"last_sequence": 0,
					"duration": 0
				}

			if (stop_sequence == 1):
				item[sentido]["start"] = arrival_timestamp

			if (stop_sequence > item[sentido]["last_sequence"]):
				item[sentido]["last_sequence"] = stop_sequence
				item[sentido]["stop"] = departure_timestamp

		# calculando o tempo da viagem (por sentido)
		for id in stop_times:
			if linhas.has_key(id):
				linha = linhas[id]
				item = stop_times[id]
				for sentido in item:
					travel_time = item[sentido]["stop"] - item[sentido]["start"]
					linha["sentidos"][sentido]["travel_time"] = travel_time.total_seconds()
					#print "%s: %s - %s." % (id, sentido, str(item[sentido]["duration"] ))



def get_frequencies(): #frequencies.txt"
	arquivo = "../amostra/SPTrans GTFS/frequencies.txt"
	with codecs.open(arquivo, 'r', encoding='UTF-8') as raw:	
		#with open(decoded_file, 'r') as raw:
		for a in raw.readlines()[1:]:
			b = a.replace('\r\n', '').split(',')
			#print b

			#"trip_id","start_time","end_time","headway_secs"
			#"1016-10-0","00:00:00","00:59:00",1800

			id_completo = b[0].replace("\"", "")
			id = id_completo[0:-2]
			sentido = id_completo[-1:]

			start_time = b[1].replace("\"", "")
			end_time = b[2].replace("\"", "")
			headway_secs = int(b[3])
			travels = 3600/headway_secs

			start_timestamp = int(getTime(start_time).total_seconds() // 3600)

			if linhas.has_key(id):
				linha = linhas[id]
				if linha["sentidos"].has_key(sentido):
					item = linha["sentidos"][sentido]
					item["total_travels"] += travels
					item["travels"][start_timestamp] = travels



def get_shapes(): #shapes.txt
	arquivo = "../amostra/SPTrans GTFS/shapes.txt"
	with codecs.open(arquivo, 'r', encoding='UTF-8') as raw:	
		#with open(decoded_file, 'r') as raw:
		for a in raw.readlines()[1:]:
			b = a.replace('\r\n', '').split(',')

			#print b
			#"shape_id","shape_pt_lat","shape_pt_lon","shape_pt_sequence","shape_dist_traveled"
			#42746,-23.446799,-46.611059,1,0
			#42746,-23.446665,-46.612229,4,120.57015

			shape_id = int(b[0])
			shape_pt_lat = float(b[1])
			shape_pt_lon = float(b[2])
			shape_pt_sequence = int(b[3])
			#shape_dist_traveled = float(b[4])

			if not shapes.has_key(shape_id):
				shapes[shape_id] = {
					"total_distance_traveled": 0,
					"last_shape": 0,
					"shapes": []
				}

			shape = shapes[shape_id]

			#shape["total_distance_traveled"] += shape_dist_traveled
			shape["last_shape"] = shape_pt_sequence

			shape["shapes"].append({
				"lat": shape_pt_lat,
				"lng": shape_pt_lon,
				"sequence": shape_pt_sequence,
				"distance_traveled": 0
			})


		for id in linhas:
			linha = linhas[id]
			for sentido in linha["sentidos"]:
				item = linha["sentidos"][sentido]
				if item["shape_id"] in shapes:
					linha["sentidos"][sentido]["shapes"] = shapes[item["shape_id"]]

		#for shape_id in shapes:
		#	print "%s %s %s" % (shape_id, shapes[shape_id]["total_distance_traveled"], len(shapes[shape_id]["shapes"]))







get_routes()
get_trips()
get_travel_times()
get_frequencies()

save_file("../web/data/linhas.json", linhas)
get_shapes()

#print float('120.57015')


for id in linhas:
	save_file("../web/data/linhas/%s.json" % id, linhas[id])


print "*** FIM ***"





def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc