from flask import Flask, redirect, url_for
from pymongo import MongoClient
import pymysql.cursors
from views.summary import summary


app = Flask(__name__)
app.config['MONGO'] = MongoClient(host='10.60.0.50')['finance']
app.config['MYSQL'] = pymysql.connect(host='10.60.0.54', user='hyx', password='hyx',
                                      db='finance', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

app.register_blueprint(summary, url_prefix="/summary")


@app.route('/')
def root():
    return redirect(url_for('summary.get_summary', stock_name="上证综指"))


def create_app():
    return app


application = create_app()

if __name__ == '__main__':
    application.run(host="0.0.0.0", port=10001)
    app.config['MONGO'].close()
    app.config['MYSQL'].close()

