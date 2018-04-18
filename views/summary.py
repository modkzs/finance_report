# -*- coding: utf-8 -*-
from bson import ObjectId
from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request

summary = Blueprint("summary", __name__)

performance = {0: '小幅震荡', 1: '小幅上扬', 2: '大幅上涨', 3 : '小幅下跌', 4:'大幅下挫'}


@summary.record
def record_params(setup_state):
    app = setup_state.app
    summary.config = app.config


@summary.route("/<stock_name>", methods=['POST', 'GET'])
def get_summary(stock_name):
    summary_sql = "SELECT * FROM `target_desc` WHERE `name`=%s"
    news_sql = "SELECT * FROM `news_influence` WHERE `target`=%s"

    with summary.config['MYSQL'].cursor() as cursor:
        cursor.execute(summary_sql, (stock_name, ))
        result = cursor.fetchall()

        if len(result) == 0:
            return

        day_show = result[0]['performance']
        predict_pref = result[0]['predict_perf']

        cursor.execute(news_sql, (stock_name,))
        result = cursor.fetchall()

        datas = [r['news'].split('.') for r in result]
        news = {}
        for d in datas:
            tmp = news.get(d[1], [])
            tmp.append(ObjectId(d[2]))
            news[d[1]] = tmp

    result = []
    for (k, v) in news.items():
        result.extend([p['title'] for p in summary.config['MONGO'][k].find({"_id": {"$in": v}})])

    return render_template('report.html', stock_name=stock_name, perf=performance[day_show],
                           predict_pred=performance[predict_pref], news=result)
