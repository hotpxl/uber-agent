import json, math

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
        print self.dict
    # def getCoordinatesByZoneId(self, zoneId):
    # def getAddressByZoneId(self, zoneId):
    #
    def getDistance(self, zoneId1, zoneId2):
        c1 = self.dict[zoneId1]
        c2 = self.dict[zoneId2]
        return math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2)



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

        print d
        print len(d)

a = ZoneCoordinates()
print a.getDistance(1,300)