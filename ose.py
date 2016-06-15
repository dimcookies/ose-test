# -*- coding: utf-8 -*-
from flask import Flask, render_template, session
import json
import urllib2
from collections import OrderedDict
import time
import math

app = Flask(__name__)
app.config['DEBUG'] = True

app.secret_key = 'br6YwkwSk5JSjo62MheXjPT9PPOjWjlbA9rG9aLJC1bmIr3WV5JarPHPwFVp3'

# map of stations, values: Description, next station, previous station
st = {
    u"ΠΑΕΡ": ["Aerodromio", u"ΠΚΡΩ", u"ΠΚΡΩ", 12],
    u"ΠΚΡΩ": ["Koropi", u"ΠΠΑΙ", u"ΠΑΕΡ", 11],
    u"ΠΠΑΙ": ["Paiania_katza", u"ΠΠΑΛ", u"ΠΚΡΩ", 10],
    u"ΠΠΑΛ": ["Pallini", u"ΠΔΟΥ", u"ΠΠΑΙ", 9],
    u"ΠΔΟΥ": ["Doukisis", u"ΠΠΕΝ", u"ΠΠΑΛ", 8],
    u"ΠΠΕΝ": ["Pentelis", u"ΠΚΗΦ", u"ΠΔΟΥ", 7],
    u"ΠΚΗΦ": ["Kifisias", u"ΠΝΕΡ", u"ΠΠΕΝ", 6],
    u"ΠΝΕΡ": ["Neratziotisa", u"ΠΗΡΑ", u"ΠΚΗΦ", 5],
    u"ΠΗΡΑ": ["Irakleio", u"ΠΜΕΤ", u"ΠΝΕΡ", 4],
    u"ΠΜΕΤ": ["Metamorfosi", u"ΠΣΚΑ", u"ΠΗΡΑ", 3],
    u"ΠΣΚΑ": ["Ska", u"ΠΑΝΛ", u"ΠΜΕΤ", 2],
    u"ΠΑΝΛ": ["Ano_liosia", u"ΠΑΣΠ", u"ΠΣΚΑ", 1],
    u"ΠΑΣΠ": ["Aspropirgos", u"ΠΜΑΓ", u"ΠΑΝΛ", 0],
    u"ΠΜΑΓ": ["Magoula", u"ΠΝΕΠ", u"ΠΑΣΠ", 0],
    u"ΠΝΕΠ": ["Nea_peramos", u"ΠΜΕΓ", u"ΠΜΑΓ", 0],
    u"ΠΜΕΓ": ["Megara", u"ΠΚΙΝ", u"ΠΝΕΠ", 0],
    u"ΠΚΙΝ": ["Kineta", u"ΠΑΘΕ", u"ΠΜΕΓ", 0],
    u"ΠΑΘΕ": ["Ag_theodoroi", u"ΠΚΟΡ", u"ΠΚΙΝ", 0],
    u"ΠΚΟΡ": ["Korinthos", u"ΠΖΕΥ", u"ΠΑΘΕ", 0],
    u"ΠΖΕΥ": ["Zevgolatio", u"ΠΚΙΑ", u"ΠΚΟΡ", 0],
    u"ΠΚΙΑ": ["Kiato", u"ΠΖΕΥ", u"ΠΖΕΥ", 0]
}

st_coords = {u'\u03a0\u039a\u03a1\u03a9': (37.9128816667, 23.8957616),
             u'\u03a0\u0396\u0395\u03a5': (37.9258416667, 22.8060633),
             u'\u03a0\u039a\u0397\u03a6': (38.0418933333, 23.80414),
             u'\u03a3\u039a\u0391\u03a7': (38.06860667, 23.73783667),
             u'\u03a0\u039d\u0395\u03a1': (38.04474, 23.7938333), u'\u0391\u03a5\u039b\u0399': (38.40464333, 23.603455),
             u'\u03a0\u0397\u03a1\u0391': (38.0569733333, 23.772015),
             u'\u039b\u0399\u03a4\u039f': (40.1251816667, 22.5498966667),
             u'\u03a0\u0392\u0391\u03a3': (38.04010333, 23.72767),
             u'\u0391\u03a7\u0391\u03a1': (38.080255, 23.74397167),
             u'\u039b\u0395\u03a0\u03a4': (40.0585933333, 22.56559), u'\u03a0\u03a0\u0395\u039d': (38.03303, 23.82242),
             u'\u03a0\u0394\u039f\u03a5': (38.02446, 23.8341566),
             u'\u03a0\u0395\u0399\u03a1': (37.94900667, 23.64413167),
             u'\u03a0\u03a0\u0391\u039b': (38.0054066667, 23.869755),
             u'\u039a\u039f\u03a1\u039f': (40.3170916667, 22.5784433333),
             u'\u03a0\u03a0\u0391\u0399': (37.9833916667, 23.8698133),
             u'\u03a1\u0391\u03a8\u0391': (39.8994433333, 22.614535),
             u'\u03a0\u039a\u0399\u0391': (38.01347, 22.735045),
             u'\u0394\u0395\u039a\u0395': (38.09975833, 23.78016833),
             u'\u03a0\u0391\u03a3\u03a0': (38.0807983333, 23.604755),
             u'\u03a0\u0391\u039d\u039b': (38.0707316667, 23.7103233),
             u'\u03a0\u039a\u039f\u03a1': (37.9210566667, 22.9328616),
             u'\u03a0\u0391\u0395\u03a1': (37.937005, 23.9451283),
             u'\u0391\u0394\u0395\u039d': (40.674405, 22.6029083333),
             u'\u03a0\u0391\u039b\u03a6': (39.3124716667, 22.2439716667),
             u'\u03a7\u0391\u039b\u039a': (38.46252, 23.58667833), u'\u03a0\u039a\u0399\u039d': (37.965635, 23.2014233),
             u'\u03a0\u0391\u039d\u0393': (38.02215167, 23.71857333),
             u'\u039b\u0391\u03a1\u0399': (39.6301016667, 22.4250616667),
             u'\u03a0\u0391\u0399\u03a1': (37.96234333, 23.66905333),
             u'\u03a0\u039d\u0395\u03a0': (38.0133616667, 23.4147183),
             u'\u03a0\u039c\u0395\u03a4': (38.0601466667, 23.755695),
             u'\u03a0\u03a4\u0391\u03a5': (37.96902333, 23.694015), u'\u039a\u0391\u039b\u0391': (39.70306, 21.62511),
             u'\u039d\u03a0\u039f\u03a1': (39.9760133333, 22.6383733333),
             u'\u03a0\u039b\u03a5\u039a': (38.05460667, 23.732815),
             u'\u03a0\u039b\u03a4\u03a5': (40.63724, 22.5306566667), u'\u03a0\u039b\u0395\u03a5': (37.95577, 23.65442),
             u'\u039f\u0399\u039d\u03a6': (38.30737833, 23.63357333),
             u'\u0391\u0398\u0397\u039d': (37.992535, 23.72071833),
             u'\u039a\u0391\u03a4\u0395': (40.2686683333, 22.5315883333),
             u'\u0391\u0399\u0393\u039d': (40.4983483333, 22.55212),
             u'\u0391\u0398\u03a9\u039c': (38.28189333, 23.66706333),
             u'\u0391\u03a6\u0399\u0394': (38.187955, 23.844555), u'\u03a7\u03a301': (38.35529833, 23.607045),
             u'\u0391\u03a5\u039b\u03a9': (38.25054167, 23.69554667),
             u'\u039f\u0399\u039d\u039f': (38.32211, 23.60955667),
             u'\u03a0\u03a3\u039a\u0391': (38.0660316667, 23.7363216),
             u'\u0391\u03a3\u03a4\u0395': (38.14028833, 23.859125),
             u'\u03a0\u0391\u0398\u0395': (37.9333983333, 23.137485),
             u'\u03a3\u03a6\u0395\u039d': (38.23545167, 23.78402667),
             u'\u03a0\u039c\u0395\u0393': (37.99094, 23.361145),
             u'\u03a0\u03a1\u039f\u03a5': (37.97402167, 23.70442333),
             u'\u039a\u0391\u039b\u03a0': (38.389675, 23.59284833),
             u'\u03a3\u0399\u039d\u0394': (40.67413, 22.8059216667),
             u'\u03a0\u039c\u0391\u0393': (38.0740033333, 23.5298633),
             u'\u03a3\u03a5\u039d\u0395': (38.33785833, 23.60959333),
             u'\u0398\u0395\u03a3\u03a3': (40.64516, 22.929425)}


@app.route('/')
def trainPosition():
    to_airport = {}
    from_airport = {}
    current_sec = int(time.time())
    for i in getWSResponse():
        # get values from record
        id = i["id"]
        trip_id = i["tripId"]
        start = i["tripStartEn"]
        end = i["tripEndEn"]
        end2 = i["endStationNameEn"]
        station = i["closestStationId"]
        speed = i["speed"]
        lat = float(i["lat"])
        lon = float(i["lon"])
        distance = distance_from_station(lat, lon, station)
        # create record
        rc = {'start': start, 'end': end, 'end2': end2, 'station': getStation(station), 'speed': speed, 'id': id,
              'trip_id': trip_id, 'distance': distance}
        # default direction from airport
        direction = "d"
        session_id = id + "_" + direction
        # airport to liosia, kiato
        if (start in ['AIRPORT'] and (end in ['A. LIOSSIA', 'KIATO'] or end2 in ['A. LIOSSIA', 'KIATO'])) or (
                start in ['A. LIOSSIA'] and (end in ['KIATO'] or end2 in ['KIATO'])):
            rc['next_station'] = getNextStation(station, speed, 1)
            rc['prev_station'] = getNextStation(station, speed, 2)
            from_airport[id] = rc
            from_airport[id].update(checkPrev(session_id, current_sec))
        # kiato,liosia to airport
        elif start in ['A. LIOSSIA', 'KIATO'] and end in ['AIRPORT'] or end2 in ['AIRPORT']:
            rc['next_station'] = getNextStation(station, speed, 2)
            rc['prev_station'] = getNextStation(station, speed, 1)
            to_airport[id] = rc
            # update direction
            direction = "r"
            session_id = id + "_" + direction
            to_airport[id].update(checkPrev(session_id, current_sec))
        # update session if has changed
        if (not session.has_key(session_id)) or session.get(session_id)[0] != st.get(station, [station, '', ''])[
            0] or distance != session.get(session_id)[2]:
            session[session_id] = [st.get(station, [station, '', ''])[0], current_sec, distance]
    # orde dictionaries based on id
    return render_template('index.html', stations=stationsToDisplay(),
                           stationsFrom=trainsToDisplay(from_airport.items()),
                           stationsTo=trainsToDisplay(to_airport.items()),
                           from_airport=OrderedDict(sorted(from_airport.items(), key=lambda t: t[0])),
                           to_airport=OrderedDict(sorted(to_airport.items(), key=lambda t: t[0])))


'''
Retreive certain stations to show on page ordered
{id:station_name}
'''


def stationsToDisplay():
    return dict(filter(lambda x: x[0] != 0, map(lambda x: (st[x][3], st[x][0]), st)))

'''
Retreice stations with trains as current station, value
{id:distance}
'''


def trainsToDisplay(trains):
    stations = stationsToDisplay()
    for station in stations:
        station_name = stations[station]
        stations[station] = ""
        for train in trains:
            train = train[1]
            if train['station'] == station_name:
                stations[station] = stations[station] + str(train['trip_id']) + " (" +str(train['distance']) + " km) "

    return stations

''' Retreives response from web service and parse it as json '''


def getWSResponse():
    try:
        response = urllib2.urlopen('http://www.trainose.gr/traingps/ws.php?op=1')
        html = response.read()
        return json.loads(html)
    except Exception, e:
        return []
    


''' Station name from map '''


def getStation(station):
    return st.get(station, [station, '', ''])[0]


'''
	Next / Prev station from map 
	idx : 1 is next, 2 is previous
'''


def getNextStation(station, speed, idx):
    # if train is stopped do not show next and previous station
    if float(speed.replace(",", ".")) > 0 and st.has_key(station):  # should exist in map to show prev/next
        return getStation(st[station][idx])
    return ""


''' Check if session has stored previous station info '''


def checkPrev(id, current_sec):
    if session.has_key(id):
        record = {}
        record['last_station'] = session[id][0]
        record['last_station_time_diff'] = convertSecs(int(current_sec - int(session[id][1])))
        record['last_station_distance'] = session[id][2]
        return record
    return {}


''' Seconds to minutes '''


def convertSecs(sec):
    min_part = str(sec / 60)
    sec_part = str(sec % 60).zfill(2)
    return min_part + ":" + sec_part + " mins"


'''
returns distance between current position and a certain station
returns -1 if station not found
'''


def distance_from_station(lat1, long1, stationId):
    if not st.has_key(stationId):
        return -1
    return round(distance_on_unit_sphere(lat1, long1, st_coords[stationId][0], st_coords[stationId][1]), 2)


'''
 taken from http://www.johndcook.com/blog/python_longitude_latitude/

 calculates distance between a set of lat/long points
 Output in kilometers
'''


def distance_on_unit_sphere(lat1, long1, lat2, long2):
    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi / 180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1) * degrees_to_radians
    phi2 = (90.0 - lat2) * degrees_to_radians

    # theta = longitude
    theta1 = long1 * degrees_to_radians
    theta2 = long2 * degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) +
           math.cos(phi1) * math.cos(phi2))
    arc = math.acos(cos)

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    earth_radius_km = 6371
    return arc * earth_radius_km


if __name__ == '__main__':
    app.run(debug=True)
