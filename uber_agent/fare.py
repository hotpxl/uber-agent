import requests
import json
import distance


# curl -H 'Authorization: Token uBVRF7hOPOfAdo6BNQcUb5M8OVZEhNAc7g2Y6J3v' \
#      -H 'Accept-Language: en_US' \
#      -H 'Content-Type: application/json' \
#      'https://api.uber.com/v1.2/estimates/price?start_latitude=37.7752315&start_longitude=-122.418075&end_latitude=37.7752415&end_longitude=-122.518075'

# uBVRF7hOPOfAdo6BNQcUb5M8OVZEhNAc7g2Y6J3v

def get_fare(index1, index2):

    start_latitude = 37.7752315
    start_longitude= -122.418075
    end_latitude=37.7752415
    end_longitude=-122.518075

    url  =  'https://api.uber.com/v1.2/estimates/price?start_latitude={}&start_longitude={}&end_latitude={}&end_longitude={}'.format(start_latitude, start_longitude, end_latitude, end_longitude)
    headers = {'Authorization': 'Token uBVRF7hOPOfAdo6BNQcUb5M8OVZEhNAc7g2Y6J3v',
               'Accept-Language': 'en_US',
               'Content-Type': 'application/json'}

    r = requests.get(url, headers=headers)
    #print (r.text)

    data = json.loads(r.text)
    entries = data["prices"]
    uberX = entries[7]
    high_estimate = uberX["high_estimate"]
    low_estimate = uberX["low_estimate"]
    average_fare = (high_estimate+low_estimate)/2

    print (average_fare)



