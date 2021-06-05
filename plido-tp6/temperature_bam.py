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


fig, ax = plt.subplots(1, 5)
ax[0].plot_date(e, y, linestyle="solid")
ax[1].boxplot(y)

b = [r["y"]]

for idx in range(2, 5):
    print ("*"*10, idx)
    b_2 = []
    for a in b:
        middle = len(a)//2
        r1 = a[:middle]
        r2 = a[middle:] 
        print (r1, r2)
        b_2.append(r1)
        b_2.append(r2)
        print (b_2)

    ax[idx].boxplot(np.array(b_2, dtype=object))
    b = b_2



plt.title("Sensor values in the last hour")
ax[0].fmt_xdata = mdates.DateFormatter('%m-%d %H:%M:%S')
fig.autofmt_xdate()

plt.show()

