# coding: utf-8
import tushare as ts

df = ts.get_hist_data('000875')

# df.to_csv('../data/000875.csv')
# df.to_csv('../data/000875.csv',columns=[] )

news = ts.get_latest_news(top=5,show_content=True)

news.to_csv('../data/news.csv',columns=['classify','title','time','content'])