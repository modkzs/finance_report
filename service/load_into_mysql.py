# -*- coding: utf-8 -*-
import pymysql.cursors

connection = pymysql.connect(host='10.60.0.54',
                             user='hyx',
                             password='hyx',
                             db='finance',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
SQL = "INSERT INTO news_influence (news, target, influence) VALUES (%s, %s, %s)"
info = {}
with connection.cursor() as cursor:
    with open('result') as f:
        for l in f:
            source, influence, obj_id, target = l.strip().split('\t')
            cursor.execute(SQL, (source + "." + obj_id, target, float(influence)))
            info[target] = info.get(target, 0) + float(influence)

    SQL = "INSERT INTO target_desc (name, belongs_target, performance, predict_perf) VALUES (%s, %s, %s, %s)"
    for (k, v) in info.items():
        cursor.execute(SQL, (k, "", 0, v))

    connection.commit()

connection.close()
