# -*- coding: utf-8 -*-
import time
from collections import OrderedDict

from flask import session

from ose_data import st, st_coords, OSE_WS_URL

from transport.utils import distance_on_unit_sphere, convertSecs, getWSJsonResponse

'''TODO refactor: abstract session, refactor to class + methods'''
def trainPosition():
    to_airport = {}
    from_airport = {}
    current_sec = int(time.time())
    for i in getWSJsonResponse(OSE_WS_URL):
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
        rc = {'start': start, 'end': end, 'end2': end2, 'station': getStation(station), 'speed': speed, 'id': id, 'trip_id': trip_id, 'distance': distance}
        # default direction from airport
        direction = "d"
        session_id = id + "_" + direction
        # airport to liosia, kiato
        if (start in ['AIRPORT'] and (end in ['A. LIOSSIA', 'KIATO'] or end2 in ['A. LIOSSIA', 'KIATO'])) or (start in ['A. LIOSSIA'] and (end in ['KIATO'] or end2 in ['KIATO'])):
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
        if (not session.has_key(session_id)) or session.get(session_id)[0] != st.get(station, [station, '', ''])[0] or distance != session.get(session_id)[2]:
            session[session_id] = [st.get(station, [station, '', ''])[0], current_sec, distance]
    # sort dictionaries based on id
    return {'stations':stationsToDisplay(),
                           'stationsFrom':trainsToDisplay(from_airport.items()),
                           'stationsTo':trainsToDisplay(to_airport.items()),
                           'from_airport':OrderedDict(sorted(from_airport.items(), key=lambda t: t[0])),
                           'to_airport':OrderedDict(sorted(to_airport.items(), key=lambda t: t[0]))}


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
                stations[station] = (str(train['trip_id']) + " (" +str(train['distance']) + " km) ", float(train['speed'].replace(",",".")))
                break

    return stations


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


''' Check if session has stored previous station info TODO refactor: abstract session'''


def checkPrev(id, current_sec):
    if session.has_key(id):
        record = {}
        record['last_station'] = session[id][0]
        record['last_station_time_diff'] = convertSecs(int(current_sec - int(session[id][1])))
        record['last_station_distance'] = session[id][2]
        return record
    return {}

'''
returns distance between current position and a certain station
returns -1 if station not found
'''


def distance_from_station(lat1, long1, stationId):
    if not st.has_key(stationId):
        return -1
    return round(distance_on_unit_sphere(lat1, long1, st_coords[stationId][0], st_coords[stationId][1]), 2)

