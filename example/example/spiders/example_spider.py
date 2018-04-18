# -*- coding: utf-8 -*-
import scrapy
import datetime


class ExampleSpider(scrapy.Spider):
    name = "example"

    custom_settings = {
        'ITEM_PIPELINES': {
            'example.pipelines.ExamplePipeline': 300,
        }
    }

    def start_requests(self):
        yield scrapy.Request(url="http://news.10jqka.com.cn/today_list/", callback=self.get_enter)

    def get_enter(self, response):
        for url in response.xpath('//ul[@class="list"]//li/a/@href').extract():
            yield scrapy.Request(url=url, callback=self.craw_news_page)

    def craw_news_page(self, response):
        for url in response.xpath('//span[@class="arc-title"]/a/@href').extract():
            yield scrapy.Request(url=url, callback=self.craw_news)

        for url in response.xpath('//a[@class="next"]/@href').extract():
            yield scrapy.Request(url=url, callback=self.craw_news_page)

    def craw_news(self, response):
        text = "".join(response.xpath('//div[@class="main-text atc-content"]//p/text()').extract())
        influence = "".join(response.xpath('//div[@class="info-fr fr"]/span/text()').extract())
        title = "".join(response.xpath('//title/text()').extract())
        time = datetime.datetime.strptime("".join(response.xpath('//span[@id="pubtime_baidu"]/text()').extract()),
                                          "%Y-%m-%d %H:%M:%S")
        url = response.url

        yield {'text': text, 'influence': influence, 'title': title, 'time': time, 'url': url}
