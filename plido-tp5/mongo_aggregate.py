from pymongo import MongoClient

client = MongoClient()
db = client["meteo-data"]
measure = db.measure

sensor_location = "Room A123"

found_item = measure.find_one ({"Location" : sensor_location })
if found_item is None:
    raise ValueError ("{} not found".format(sensor_location))
else:
    sensor_id = found_item["_id"]

print (sensor_id)
        
res = measure.aggregate([{"$match" : {"SensorCharacteristics" : sensor_id }}])

print (res)

for r in res:
    print (r)