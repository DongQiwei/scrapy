# -*- coding: utf-8 -*-
import scrapy
import logging
from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    # 这里是爬虫名字
    name = 'douban_spider'
    # 允许的域名
    allowed_domains = ['movie.douban.com']
    # 入口url,扔到调度器里去
    start_urls = ['https://movie.douban.com/top250']

    # 默认解析方法
    def parse(self, response):
        self.log(f"start to parse url:{response.url}", level=logging.WARNING)
        # 循环电影的条目
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for i_item in movie_list:
            # item文件导进来
            douban_item = DoubanItem()
            # 写详细的xpath,进行数据解析
            serial_number = i_item.xpath('.//div[@class="item"]//em/text()').extract_first()
            movie_name = i_item.xpath(
                ".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            content = i_item.xpath(".//div[@class='info']/div[@class='bd']/p[1]/text()").extract()
            # 多行数据处理

            for i_content in content:
                content_s = "".join(i_content.split())
                introduce = content_s
            star = i_item.xpath('.//span[@class="rating_num"]/text()').extract_first()
            evaluate = i_item.xpath('.//div[@class="star"]/span[4]/text()').extract_first()
            describe = i_item.xpath('.//p[@class="quote"]/span/text()').extract_first()
            image_url = i_item.xpath('.//div[@class="item"]/div[@class="pic"]/a/img/@src').extract_first()

            self.log(f"image_url:{image_url}, name:{movie_name}", level=logging.WARNING)
            item = DoubanItem(serial_number=serial_number, movie_name=movie_name, introduce=introduce,
                              star=star, evaluate=evaluate, describe=describe, image_url=[image_url])
            # 需要将数据yield到pipelines里面去

            yield item

        # 解析下一页,取得后页的xpath
        next_link = response.xpath('//span[@class="next"]/link/@href').extract()
        if next_link:
            next_link = next_link[0]
            self.log(f"scrapy next_link:{next_link}", level=logging.WARNING)
            yield scrapy.Request("https://movie.douban.com/top250" + next_link, callback=self.parse)
