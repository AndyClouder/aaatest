# -*- coding: utf-8 -*-
import os
import scrapy

class PItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()


class RentiSpider(scrapy.Spider):
    name = "renti"
    allowed_domains = ["www.duotoo.com/rentiyishu"]
    start_urls = ( 'http://www.duotoo.com/rentiyishu/25091.html',)

    def parse(self, response):
        exp = '//div[@class="pages"]//li//a[text()="下一页"]/@href'
        _next = response.xpath(exp).extract_first()
        next_page = os.path.join(os.path.dirname(response.url), _next)
        yield scrapy.FormRequest(next_page, callback=self.parse)
        for p in response.xpath('//div[@class="ArticlePicBox Aid43 "]//li//a/@href').extract():
            yield scrapy.FormRequest(p, callback=self.parse_item)
    def parse_item(self, response):
        item=PItem()
        urls = response.xpath("//div[@class='ArticleBox']//a//img/@src").extract()
        item['image_urls'] = urls
        return item