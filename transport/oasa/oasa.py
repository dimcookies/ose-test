from oasa_data import  *
from transport.utils import *

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
            res.append((float(bus['CS_LAT']), float(bus['CS_LNG'])))
        buses[route] = res

    for stop in stops:
        res = []
        for route in stop['routes']:
            for bus in buses[route]:
                #print route,lines
                res.append({'route':routes[route], 'dist':round(distance_on_unit_sphere(bus[0], bus[1], stop['stop_lat'], stop['stop_lng']) ,2)})
        stop['buses'] = res

    return stops

#OrderedDict(sorted(from_airport.items(), key=lambda t: t[0]))

#print stopsData()