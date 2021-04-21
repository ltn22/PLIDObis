from pymongo import MongoClient

client = MongoClient()
db = client["meteo-data"]
measure = db.measure

list_of_locations = measure.find({"@context": "http://user.ackl.io/schema/Sensor"})
print (list_of_locations)

sensor_location = "kitchen"

found_item = measure.find_one ({"Location" : sensor_location })
if found_item == None:
    raise ValueError ("{} not found".format(sensor_location))
else:
    sensor_id = found_item["_id"]

print (sensor_id)
        
res = measure.aggregate([{"$match" : {"SensorCharacteristics" : sensor_id }}])

print (res)

for r in res:
    print (r)