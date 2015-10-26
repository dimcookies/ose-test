# -*- coding: utf-8 -*-
from flask import Flask,render_template,session
import json
import urllib2
from collections import OrderedDict
import time

app = Flask(__name__)
app.config['DEBUG'] = True

app.secret_key = 'br6YwkwSk5JSjo62MheXjPT9PPOjWjlbA9rG9aLJC1bmIr3WV5JarPHPwFVp3'

#map of stations, values: Description, next station, previous station
st= {
u"ΠΑΕΡ":["Aerodromio",u"ΠΚΡΩ",u"ΠΚΡΩ"],
u"ΠΚΡΩ":["Koropi",u"ΠΠΑΙ",u"ΠΑΕΡ"],
u"ΠΠΑΙ":["Paiania_katza",u"ΠΠΑΛ",u"ΠΚΡΩ"],
u"ΠΠΑΛ":["Pallini",u"ΠΔΟΥ",u"ΠΠΑΙ"],
u"ΠΔΟΥ":["Doukisis",u"ΠΠΕΝ",u"ΠΠΑΛ"],
u"ΠΠΕΝ":["Pentelis",u"ΠΚΗΦ",u"ΠΔΟΥ"],
u"ΠΚΗΦ":["Kifisias",u"ΠΝΕΡ",u"ΠΠΕΝ"],
u"ΠΝΕΡ":["Neratziotisa",u"ΠΗΡΑ",u"ΠΚΗΦ"],
u"ΠΗΡΑ":["Irakleio",u"ΠΜΕΤ",u"ΠΝΕΡ"],
u"ΠΜΕΤ":["Metamorfosi",u"ΠΣΚΑ",u"ΠΗΡΑ"],
u"ΠΣΚΑ":["Ska",u"ΠΑΝΛ",u"ΠΜΕΤ"],
u"ΠΑΝΛ":["Ano_liosia",u"ΠΑΣΠ",u"ΠΣΚΑ"],
u"ΠΑΣΠ":["Aspropirgos",u"ΠΜΑΓ",u"ΠΑΝΛ"],
u"ΠΜΑΓ":["Magoula",u"ΠΝΕΠ",u"ΠΑΣΠ"],
u"ΠΝΕΠ":["Nea_peramos",u"ΠΜΕΓ",u"ΠΜΑΓ"],
u"ΠΜΕΓ":["Megara",u"ΠΚΙΝ",u"ΠΝΕΠ"],
u"ΠΚΙΝ":["Kineta",u"ΠΑΘΕ",u"ΠΜΕΓ"],
u"ΠΑΘΕ":["Ag_theodoroi",u"ΠΚΟΡ",u"ΠΚΙΝ"],
u"ΠΚΟΡ":["Korinthos",u"ΠΖΕΥ",u"ΠΑΘΕ"],
u"ΠΖΕΥ":["Zevgolatio",u"ΠΚΙΑ",u"ΠΚΟΡ"],
u"ΠΚΙΑ":["Kiato",u"ΠΖΕΥ",u"ΠΖΕΥ"]
}

@app.route('/')
def hello():
	to_airport = {}
	from_airport = {}
	current_sec = int(time.time())
	response = urllib2.urlopen('http://www.trainose.gr/traingps/ws.php?op=1')
	html = response.read()
	parsed_json = json.loads(html)
	for i in parsed_json:
		#get values from record
		id = i["id"]
		trip_id = i["tripId"]
		start = i["tripStartEn"]
		end = i["tripEndEn"]
		end2 = i["endStationNameEn"]
		station = i["closestStationId"]
		speed = i["speed"]
		#create record
		rc = {'start':start , 'end':end, 'end2':end2, 'station':getStation(station), 'speed':speed, 'id':id, 'trip_id':trip_id}
		#default direction from airport
		direction = "d"
		session_id = id + "_" + direction
		#airport to liosia, kiato		
		if (start in ['AIRPORT'] and (end in ['A. LIOSSIA', 'KIATO'] or end2 in ['A. LIOSSIA', 'KIATO'])) or (start in ['A. LIOSSIA'] and (end in ['KIATO'] or end2 in ['KIATO'])):
			rc['next_station'] = getNextStation(station, speed, 1)
			rc['prev_station'] = getNextStation(station, speed, 2)
			from_airport[id] = rc
			from_airport[id].update(checkPrev(session_id, current_sec))
		#kiato,liosia to airport
		elif start in ['A. LIOSSIA', 'KIATO'] and end in ['AIRPORT'] or end2 in ['AIRPORT']:	
			rc['next_station'] = getNextStation(station, speed, 2)
			rc['prev_station'] = getNextStation(station, speed, 1)
			to_airport[id] = rc
			#update direction
			direction = "r"
			session_id = id + "_" + direction
			to_airport[id].update(checkPrev(session_id, current_sec))
		#update session if has changed
		if (not session.has_key(session_id)) or session.get(session_id)[0] != st.get(station,[station,'',''])[0]:
			session[session_id] = [st.get(station,[station,'',''])[0], current_sec]
	#orde dictionaries based on id
	return render_template('index.html', from_airport=OrderedDict(sorted(from_airport.items(), key=lambda t: t[0])), to_airport=OrderedDict(sorted(to_airport.items(), key=lambda t: t[0])))

''' Station name from map '''
def getStation(station):
	return st.get(station, station)[0]

''' 
	Next / Prev station from map 
	idx : 1 is next, 2 is previous
'''
def getNextStation(station, speed, idx):
	#if train is stopped do not show next and previous station
	if float(speed.replace(",",".")) > 0 and st.has_key(station): #should exist in map to show prev/next
		return getStation(st[station][idx])
	return ""		

''' Check if session has stored previous station info '''
def checkPrev(id, current_sec):
	if session.has_key(id):
		record = {}
		record['last_station'] = session[id][0]
		record['last_station_time_diff'] = convertSecs(int(current_sec - int(session[id][1])))
		return record
	return {}

''' Seconds to minutes '''
def convertSecs(sec):
	if sec < 61:
		return str(sec) + " sec"
	return str(sec/60.0)[:4] + " min"

if __name__ == '__main__':	
	app.run(debug=True)

