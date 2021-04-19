from pymongo import MongoClient

client = MongoClient()
db = client["meteo-data"]
measures = db.data

pokemon = "Flingouste"

found_item = measures.find_one ({"Name" : pokemon })
if found_item == None:
    raise ValueError ("{} not found".format(pokemon))
else:
    sensor_id = found_item["_id"]
    
print (sensor_id)
        
res = measures.aggregate([{"$match" : {"SensorCharacteristics" : sensor_id }}])

print (res)

for r in res:
    print (r)