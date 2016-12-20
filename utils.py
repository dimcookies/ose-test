import json
import math
import urllib2

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


''' Seconds to minutes '''


def convertSecs(sec):
    min_part = str(sec / 60)
    sec_part = str(sec % 60).zfill(2)
    return min_part + ":" + sec_part + " mins"

''' Retreives response from web service and parse it as json '''

def getWSJsonResponse(url):
    try:
        response = urllib2.urlopen(url)
        html = response.read()
        return json.loads(html)
    except Exception, e:
        return []