OASA_WS_STOP_INFO = "http://telematics.oasa.gr/api/?act=getStopArrivals&p1=%s"
OASA_WS_BUS_LOCATION = "http://telematics.oasa.gr/api/?act=getBusLocation&p1=%s"

stops = [
    {'name':"Filadelfia",'id':350037, 'routes':[2219,2042], "stop_lat":38.0400748,"stop_lng":23.7405624},
    {'name':"Gefira",'id':310033, 'routes':[2043], "stop_lat":38.0600155,"stop_lng":23.752822},
    {'name':"Metamorfosi",'id':10437, 'routes':[2219], "stop_lat":38.06021,"stop_lng":23.7562958}
]

routes = {
    2219: '619',
    2042: 'B9 Anodos',
    2043: 'B9 Kathodos'
}

lines = {2242:1023, 2243:1023, 2219:1063}