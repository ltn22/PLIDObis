from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

client = MongoClient()
db = client["meteo-data"]
measure = db.measure

list_of_locations = measure.find({"@context": "http://user.ackl.io/schema/Sensor"})

sensor_location = "Room 23"

found_item = measure.find_one ({"Location" : sensor_location })
if found_item == None:
    raise ValueError ("{} not found".format(sensor_location))
else:
    sensor_id = found_item["_id"]

print (sensor_id)

currentDate = datetime.datetime.utcnow()
oneDayAgo = currentDate - datetime.timedelta(seconds=3600*24)

print (oneDayAgo)
print (oneDayAgo.isoformat())
        
res = measure.aggregate([
    {"$match":  { "$and" : [
                       {"SensorCharacteristics": sensor_id},
                       {"Date": {"$gte" : oneDayAgo.isoformat()}}
                           ]
                 }
    },

    {"$group" : {
        "_id": None,
        "count": {"$sum": 1},
        "x": {"$push": "$Date"},
        "y": {"$push": "$Temperature"}
        }
     }
])

print (res)

for r in res:
    print (r)
    x = np.array(r["x"])
    y = np.array(r["y"])

    print (len(x))

    print (len(y))

e = mdates.datestr2num(x)


fig, ax = plt.subplots(1, 3)
ax[0].plot_date(e, y, linestyle="solid")
ax[1].boxplot(y)

middle = len(y)//2
y1 = y[:middle]
y1 = y[middle:] 
ax[2].boxplot(y1, y2)


plt.title("Sensor values in the last hour")
ax[0].fmt_xdata = mdates.DateFormatter('%m-%d %H:%M:%S')
fig.autofmt_xdate()

plt.show()

