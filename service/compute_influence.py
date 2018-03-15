# -*- coding: utf-8 -*-
from pymongo import MongoClient
import datetime
import random

client = MongoClient('10.60.0.50', 27017)
db = client.finance
iter = db.example.find({
    "time": {"$gte": datetime.datetime.strptime("2018-03-08 00:00:00", "%Y-%m-%d %H:%M:%S"),
             "$lt": datetime.datetime.strptime("2018-03-09 00:00:00", "%Y-%m-%d %H:%M:%S")}
})

with open('data', 'w') as w:
    for p in iter:
        info = 1 if p['influence'] == "利好" else -1 if p['influence'] == "利空" else 0
        w.write("finance.example," + str(random.uniform(0, 1) * info) + "," + str(p['_id']) + ',' + "深证成指\n")
        w.write("finance.example," + str(random.uniform(0, 1) * info) + "," + str(p['_id']) + ',' + "上证综指\n")
