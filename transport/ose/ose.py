# -*- coding: utf-8 -*-
import time
from collections import OrderedDict

from flask import session

from ose_data import st, st_coords, OSE_WS_URL, JsonObject,all_stations_dct,new_stations

from transport.utils import distance_on_unit_sphere, convertSecs, getWSJsonResponse

'''TODO refactor: abstract session, refactor to class + methods'''


def trainPosition():
    to_airport = []
    from_airport = []
    other = []
    map_from = {}
    map_to = {}
    for i in new_stations:
        map_from[i] = []
        map_to[i] = []
    current_sec = int(time.time())
    trains_dct = getWSJsonResponse(OSE_WS_URL)
    for train_dct in filter(lambda train: train['tripStartEn'] == 'AIRPORT', trains_dct):
        from_airport.append(createTrain(train_dct, map_from))
    for train_dct in filter(lambda train: train['tripEndEn'] == 'AIRPORT', trains_dct):
        to_airport.append(createTrain(train_dct, map_to))
    for train_dct in filter(lambda train: train['tripEndEn'] != 'AIRPORT' and train['tripStartEn'] != 'AIRPORT', trains_dct):
        other.append(createTrain(train_dct, {}))

    # sort dictionaries based on id
    return {'stations': new_stations,
            'map_from': map_from,
            'map_to': map_to,
            'from_airport': from_airport,
            'to_airport': to_airport,
            'other':other, 'map_from':map_from, 'map_to':map_to}

def createTrain(train_dct, map_dct):
    train_dct['distance'] = distance_from_station(float(train_dct['lat']), float(train_dct['lon']),
                                                      train_dct["closestStationId"])
    try:
        train_dct['closestStation'] = all_stations_dct[train_dct["closestStationId"]].stationNameEn
    except:
        train_dct['closestStation'] = train_dct["closestStationId"]
    map_dct.setdefault(train_dct["closestStationId"],[]).append(train_dct['tripId'] + ' ')
    return JsonObject(**train_dct)

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
                stations[station] = (str(train['trip_id']) + " (" + str(train['distance']) + " km) ",
                                     float(train['speed'].replace(",", ".")))
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
