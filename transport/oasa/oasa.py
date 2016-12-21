from oasa_data import  *
from transport.utils import *
from flask import session


def stopsData():

    for stop in stops:
        res = []
        #print stop
        for dt in getWSJsonResponse(OASA_WS_STOP_INFO % stop['id']):
            try:
                dt['nm'] = routes[int(dt['route_code'])]
                res.append(dt)
            except KeyError:
                pass
        stop['data'] = res

    buses = {}
    for route in routes.keys():
        res = []
        for bus in getWSJsonResponse(OASA_WS_BUS_LOCATION % route):
            res.append((float(bus['CS_LAT']), float(bus['CS_LNG']),bus['VEH_NO']))
        buses[route] = res

    for stop in stops:
        res = []
        for route in stop['routes']:
            for bus in buses[route]:
                #print route,lines
                dist = round(distance_on_unit_sphere(bus[0], bus[1], stop['stop_lat'], stop['stop_lng']), 2)
                session_key =  str(route)+ "_" + bus[2]
                prev_dist = ""
                diff = 0
                if session.has_key(session_key):
                    prev_dist = session[session_key]
                    diff = dist - prev_dist
                session[session_key] = dist
                res.append({'route':routes[route], 'veh_code':bus[2], 'dist':dist, 'prev_dist': prev_dist, 'diff': diff})
        stop['buses'] = res

    return stops

#OrderedDict(sorted(from_airport.items(), key=lambda t: t[0]))

#print stopsData()