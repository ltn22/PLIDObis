from pymongo import MongoClient

client = MongoClient()
db = client["meteo-data"]
measures = db.data

sensor_location = "Room 23"

found_item = measures.find_one ({"Location" : sensor_location })
if found_item == None:
    raise ValueError ("{} not found".format(sensor_location))
else:
    sensor_id = found_item["_id"]
    
print (sensor_id)
        
res = measures.aggregate([{"$match" : {"SensorCharacteristics" : sensor_id }}])

print (res)

for r in res:
    print (r)