import json, math, requests

class ZoneCoordinates():
    def __init__(self, fileName="washington_DC_censustracts.json"):
        self.dict = {}
        with open(fileName) as json_data:
            data = json.load(json_data)
            # print(data)
            entries = data["features"]

            # Each entry:
            # {"type": "Feature",
            #  "geometry": {"type": "MultiPolygon",
            #               "coordinates": [[[[-77.048009, 38.841266], [-77.051623, 38.987145]]]]},
            #  "properties": {"MOVEMENT_ID": "2",
            #                 "DISPLAY_NAME": "1400 Juniper Street Northwest, Northwest
            # Washington, Washington"}}

            for entry in entries:
                coords = entry["geometry"]["coordinates"][0][0]
                zoneId = int(entry["properties"]["MOVEMENT_ID"])
                avgCoord = (sum(c[1] for c in coords) / len(coords), sum(c[0] for c in coords) / len(coords))
                self.dict[zoneId] = avgCoord

            json_data.close()
        #print self.dict
    # def getCoordinatesByZoneId(self, zoneId):
    # def getAddressByZoneId(self, zoneId):
    #
    def getDistance(self, zoneId1, zoneId2):
        c1 = self.dict[zoneId1]
        c2 = self.dict[zoneId2]
        return math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2)

    def get_fare(self, index1, index2):

        start_latitude = self.dict[index1][0]
        start_longitude= self.dict[index1][1]
        end_latitude= self.dict[index2][0]
        end_longitude= self.dict[index2][1]

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

        return average_fare

    def fare_matrix(self):

        matrix = []
        for i in range(1,11):
            ls = []
            for j in range(1,11):
                fare = self.get_fare(i,j)
                print (fare)
                ls.append(fare)
            matrix.append(ls)
        return matrix





def loadZoneCoordinates(fileName="washington_DC_censustracts.json"):
    with open(fileName) as json_data:
        data = json.load(json_data)
        # print(data)
        entries = data["features"]

        # Each entry:
        # {"type": "Feature",
        #  "geometry": {"type": "MultiPolygon",
        #               "coordinates": [[[[-77.048009, 38.841266], [-77.051623, 38.987145]]]]},
        #  "properties": {"MOVEMENT_ID": "2",
        #                 "DISPLAY_NAME": "1400 Juniper Street Northwest, Northwest Washington, Washington"}}

        d = {}
        for entry in entries:
            coords = entry["geometry"]["coordinates"][0][0]
            zoneId = int(entry["properties"]["MOVEMENT_ID"])
            avgCoord = (sum(c[0] for c in coords) / len(coords), sum(c[1] for c in coords) / len(coords))
            d[zoneId] = avgCoord

        # print d
        # print len(d)

a = ZoneCoordinates()
#print (a.getDistance(1,300))
print (a.fare_matrix())
