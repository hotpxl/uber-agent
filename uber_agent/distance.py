import json
import math
import requests
import multiprocessing.dummy

# times
times = [[695.1904000000001, 770.73, 1017.77, 1312.24, 695.1904000000001, 1472.96, 695.1904000000001, 129.99, 115.0, 244.64], [961.81, 695.1904000000001, 522.48, 1073.94, 695.1904000000001, 1524.46, 695.1904000000001, 983.21, 1020.13, 799.52], [1041.9, 459.82, 695.1904000000001, 604.37, 695.1904000000001, 1123.34, 2161.67, 1178.62, 1248.64, 1280.43], [1317.65, 881.57, 490.71, 695.1904000000001, 1784.3, 613.75, 1852.73, 1425.4, 1538.77, 1472.58], [695.1904000000001, 695.1904000000001, 695.1904000000001, 1371.66, 695.1904000000001, 1429.8, 695.1904000000001, 695.1904000000001, 695.1904000000001, 695.1904000000001], [1518.75, 1449.72, 1049.26, 597.03, 980.51, 695.1904000000001, 1235.76, 1640.29, 1590.41, 1825.91], [695.1904000000001, 695.1904000000001, 1976.87, 1658.43, 678.28, 1304.11, 695.1904000000001, 695.1904000000001, 695.1904000000001, 695.1904000000001], [159.04, 872.27, 1115.49, 1401.99, 695.1904000000001, 1551.41, 695.1904000000001, 695.1904000000001, 83.23, 87.03], [141.66, 930.38, 1193.22, 1483.12, 695.1904000000001, 1417.57, 695.1904000000001, 122.93, 695.1904000000001, 251.84], [331.15, 731.46, 1258.16, 1628.78, 695.1904000000001, 1706.79, 695.1904000000001, 90.91, 228.69, 695.1904000000001]]

# fares
fares = [[16.0, 34.5, 30.5, 33.5, 24.0, 30.5, 21.5, 23.5, 31.5, 28.5], [35.0, 17.0, 22.0, 20.5, 28.5, 18.5, 25.0, 23.5, 15.0, 26.5], [33.5, 20.5, 18.5, 21.5, 21.5, 21.0, 25.0, 28.0, 28.5, 22.5], [37.0, 20.5, 19.5, 18.5, 29.5, 17.5, 29.0, 23.0, 16.0, 25.0], [29.5, 27.0, 19.5, 23.5, 18.5, 26.5, 23.0, 29.0, 28.5, 17.5], [28.5, 16.5, 24.0, 14.0, 26.0, 17.0, 28.0, 20.5, 19.0, 22.5], [25.0, 29.5, 28.0, 28.5, 21.5, 24.0, 17.0, 16.5, 24.0, 24.5], [24.0, 32.0, 31.5, 30.5, 27.0, 27.0, 22.5, 17.0, 23.0, 21.5], [31.5, 17.0, 26.0, 16.0, 28.5, 19.5, 24.0, 20.5, 20.5, 24.0], [28.5, 30.5, 25.0, 31.5, 17.0, 23.0, 22.0, 19.5, 27.0, 18.5]]

class ZoneCoordinates():
    def __init__(self, fileName="../data/washington_DC_censustracts.json"):
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
        # print (self.dict)
    # def getCoordinatesByZoneId(self, zoneId):
    # def getAddressByZoneId(self, zoneId):
    #
    def getDistance(self, zoneId1, zoneId2):
        c1 = self.dict[zoneId1]
        c2 = self.dict[zoneId2]
        return math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2)

    def distMatrix(self, n):
        matrix = []
        for i in range(1, n+1):
            l = []
            for j in range(1, n+1):
                l.append(self.getDistance(i, j))
            matrix.append(l)
        return matrix

    def get_fare(self, i):
        index1, index2 = i

        start_latitude = self.dict[index1][0]
        start_longitude= self.dict[index1][1]
        end_latitude= self.dict[index2][0]
        end_longitude= self.dict[index2][1]

        url  =  'https://api.uber.com/v1.2/estimates/price?start_latitude={}&start_longitude={}&end_latitude={}&end_longitude={}'.format(start_latitude, start_longitude, end_latitude, end_longitude)
        headers = {'Authorization': 'Token 3c0nc9MQBT_Ati3Smkb8Dmn7272uf_jyrq_r27OX',
                   'Accept-Language': 'en_US',
                   'Content-Type': 'application/json'}

        r = requests.get(url, headers=headers)
        #print (r.text)

        data = json.loads(r.text)
        if 'prices' in data:
            entries = data["prices"]
            uberX = entries[7]
            high_estimate = uberX["high_estimate"]
            low_estimate = uberX["low_estimate"]
            average_fare = (high_estimate+low_estimate)/2
        else:
            average_fare = None

        return i, average_fare

    def fare_matrix(self):
        pool = multiprocessing.dummy.Pool(32)
        entries = []
        for i in range(1, 41):
            for j in range(1, 41):
                entries.append((i, j))
        matrix = [[0] * 40 for _ in range(40)]
        for (i, j), fare in pool.imap_unordered(self.get_fare, entries):
            print(i, j, fare)
            matrix[i-1][j-1] = fare
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
matrix = a.fare_matrix()
import pickle
with open('fare.p', 'wb') as f:
    pickle.dump(matrix, f)
