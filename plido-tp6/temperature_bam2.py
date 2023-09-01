from pymongo import MongoClient
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

client = MongoClient()
db = client["meteo-data"]
measure = db.measure

sensor_location = "Room 23"

found_item = measure.find_one ({"Location" : sensor_location })
if found_item is None:
    raise ValueError ("{} not found".format(sensor_location))
else:
    sensor_id = found_item["_id"]

currentDate = datetime.datetime.utcnow()
oneDayAgo = currentDate - datetime.timedelta(seconds=3600*24)

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


for r in res:
    x = np.array(r["x"])
    y = np.array(r["y"])

e = mdates.datestr2num(x)

y_min = np.min(y) # take the min and max to display curves the same way
y_max = np.max(y)

fig = plt.figure()
grid = plt.GridSpec(3, 7, hspace=0.2, wspace=0.2) # display grid 3x7

curve = fig.add_subplot(grid[0, 0:-1]) # first line, keep last grid empty
curve.set_ylim([y_min, y_max])
curve.plot_date(e, y, linestyle="solid")
curve.fmt_xdata = mdates.DateFormatter('%m-%d %H:%M:%S')

single_boxplot = curve = fig.add_subplot(grid[0, -1]) # boxplot in the last grid 
single_boxplot.boxplot(y, showmeans=True)

b = np.array_split(y, 6) # cut one hourinto 10 min arrays

for idx in range(0, 6):
    curve = fig.add_subplot(grid[2, idx])
    curve.set_ylim([y_min, y_max])
    curve.axes.get_xaxis().set_visible(False)
    curve.axes.get_yaxis().set_visible(False)
    color = "b" # by default curve color is blue
    if idx > 0:
        if np.quantile(b[idx-1],.75)<np.quantile(b[idx],.25):
            print ("tendance a la hausse entre ", idx-1, "et", idx)
            color="r" # color is red
        elif  np.quantile(b[idx],.75)<np.quantile(b[idx-1],.25):
            print ("tendance a la baisse entre ", idx-1, "et", idx)
            color="g" # color is green
    
    curve.plot(np.arange(0, len(b[idx])), b[idx],color=color)

multibox = fig.add_subplot(grid[2, -1])
multibox.axes.get_yaxis().set_visible(False)    
multibox.boxplot(b, showmeans=True) # array may not have the same size => dtype
    
plt.show()


