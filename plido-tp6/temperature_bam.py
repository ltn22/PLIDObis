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

fig = plt.figure(figsize=(9, 4))
grid = plt.GridSpec(2, 6, hspace=0.2, wspace=0.2)

curve = fig.add_subplot(grid[0, 0:-1])
curve.plot_date(e, y, linestyle="solid")
curve.fmt_xdata = mdates.DateFormatter('%m-%d %H:%M:%S')

single_boxplot = curve = fig.add_subplot(grid[0, -1])
single_boxplot.boxplot(y)

b = [r["y"]]

for idx in range(1, 2):
    print ("*"*10, idx)
    b_2 = []
    for a in b: # split the array in two
        middle = len(a)//2
        r1 = a[:middle]
        r2 = a[middle:] 
        print (r1, r2)
        b_2.append(r1)
        b_2.append(r2)
        print (b_2)

    nb_curves = len(b_2)
    block = 8//nb_curves
    pos = 0
    for a in b_2:
        curve = fig.add_subplot(grid[idx,pos:block])
        curve.plot(np.arange(0, len(a)), a)
        pos += block


    #plt.boxplot(np.array(b_2, dtype=object))
    b = b_2



#plt.title("Sensor values in the last hour")

plt.show()

# pyplot.figure(1)
# pyplot.subplot(1, 2, 1)
# pyplot.scatter(range(5), [x ** 2 for x in range(5)], color = 'blue')
# pyplot.subplot(2, 2, 2)
# pyplot.plot(range(5), color = 'red')
# pyplot.subplot(2, 2, 4)
# pyplot.bar(range(5), range(5), color = 'green')