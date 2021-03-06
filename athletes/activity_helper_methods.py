## Author:  Katie Hanss
## Class:   Senior Thesis
## Description: This file contains methods that help 
## manipulate activities.
from .conversions import meters_to_miles, meters_to_feet, meters_per_sec_to_min_per_mile, meters_per_sec_to_miles_per_sec
from geopy.distance import vincenty


## ------------------------------------------------------------ ##
## input:    an fitparse_activity generated by fitparse
## outputs:  a dictionary where keys are fields ('distance', 
##           'timestamp' etc.) and values are a list 
## ------------------------------------------------------------ ##
def get_dict_of_fields(fitparse_activity):

    ## get unique fields in the fitparse_activity
    fields = {field for record in fitparse_activity.get_records_as_dicts('record') for field in record.keys()}

    ## make a dictionary of fields
    activity_dict = dict()
    for field in fields:
        activity_dict[field] = []

    ## fill in dictionary with appropriate fields
    for record in fitparse_activity.get_records_as_dicts('record'):
        for field in fields:

            ## if field in this record append
            if field in record:

                if field == "distance":
                    activity_dict[field].append(meters_to_miles(record[field]))

                elif field == "altitude":
                    activity_dict[field].append(meters_to_feet(record[field]))

                elif field == "speed":
                    activity_dict[field].append(record[field])

                else:
                    activity_dict[field].append(record[field])

            ## else append None
            else:
                activity_dict[field].append(None)

    return activity_dict

def get_dict_from_gpx(gpx):

    latitude = []
    longitude = []
    speed = []
    time = []
    altitude = []
    hr = []
    cad = []
    rpe = []
    distance = [0]
    for track in gpx.tracks:
        for segment in track.segments:
            for point_no in range(0, len(segment.points)):

                point = segment.points[point_no]
                
                ## get latitude
                try:
                    latitude.append(point.latitude)
                except:
                    latitude.append(None)
                    
                ## get longitude
                try:
                    longitude.append(point.longitude)
                except:
                    longitude.append(None)
                    

                ## get HR
                try:
                    hr_key = [x for x in point.extensions.keys() if "hr" in x][0]
                    hr.append(int(point.extensions[hr_key]))
                except:
                    hr.append(None)

                ## get cadence
                try:
                    cad_key = [x for x in point.extensions.keys() if "cad" in x][0]
                    cad.append(int(point.extensions[cad_key]))
                except:
                    cad.append(None)  

                ## get RPE
                try:
                    rpe_key = [x for x in point.extensions.keys() if "rpe" in x][0]
                    rpe.append(point.extensions[rpe_key])
                except:
                    rpe.append(None)


                ## get time
                try:
                    time.append(point.time)
                except:
                    time.append(None)

                ## get altitude
                try:
                    altitude.append(point.elevation)
                except:
                    altitude.append(None)

                ## get speed
                # modified from http://stackoverflow.com/questions/20308253
                if point.speed != None:
                    speed.append(point.speed)
                elif point_no > 0:
                    speed.append(point.speed_between(segment.points[point_no - 1]))
                else:
                    speed.append(None)

                ## get DISTANCE
                if point_no > 0:
                    try:
                        current_loc = (point.latitude, point.longitude)
                        previous_loc = (segment.points[point_no - 1].latitude, segment.points[point_no - 1].longitude)
                        delta_distance = vincenty(current_loc, previous_loc).miles
                    except:
                        delta_distance = 0

                    distance.append(distance[point_no - 1] + delta_distance)
                    
    return {'timestamp':time, 'position_lat':latitude, 'position_long':longitude,
            'distance':distance, 'altitude':altitude, 'speed': speed, 'heart_rate': hr,
           'cadence': cad, 'rpe':rpe}