import scrapy
import json
from ..items import DoubanItem
import re
from copy import deepcopy

class DbmovieSpider(scrapy.Spider):
    name = 'dbmovie'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/chart']

    def parse(self, response):
        cate_list= response.xpath('//div[@class="types"]/span')
        for cate in cate_list:
            item=DoubanItem()
            item['main_group']= cate.xpath('./a/text()').extract_first()
            get_type=cate.xpath('./a/@href').extract_first()
            get_type=re.search("type=.*?(\d+).*?",get_type)
            type_num=get_type.group(1)
            for p in range(0,300,20):
                json_api_page='https://movie.douban.com/j/chart/top_list?type={}&interval_id=100%3A90&action=&start={}&limit=20'.format(type_num,p)
                yield scrapy.Request(
                    json_api_page
                    ,callback=self.parse_json
                    ,meta= {'item':deepcopy(item)}
                )

    def parse_json(self,response):
        item=response.meta['item']
        json_api=json.loads(response.body_as_unicode())
        for i in range(len(json_api)):
            item['title']=json_api[i]['title']
            item['regions']=json_api[i]['regions']
            item['types']=json_api[i]['types']
            item['douban_rating']=json_api[i]['rating'][0]
            item['id']=json_api[i]['id']
            item['release_date']=json_api[i]['release_date']
            item['detail_first_page']='https://movie.douban.com/subject/{}/comments'.format(item['id'])

            yield scrapy.Request(
                item['detail_first_page']
                ,callback=self.detail_page
                ,meta= {'item':deepcopy(item)}
            )

    def detail_page(self,response):
        item=response.meta['item']
        comments=response.xpath('//div[@class="mod-bd"]/div')[:-1]
        for comment in comments:
            item['comment']=comment.xpath('.//p/span/text()').extract_first()
            rating_by_writer=comment.xpath('./div[2]//span[2]/@class').extract()[-1]
            res=re.search("star.*?(\d+).*?",rating_by_writer)
            item['rating_by_writer']=int(res.group(1))/10
            print(item)
            yield item
        next_page_part=comments[-1].xpath('//a[text()="后页 >"]/@href').extract_first()
        page_num=re.search("start=.*?(\d+).*?",next_page_sign)
        page_num=page_num.group(1)
        if int(page_num) <= 200:
            next_url=item['detail_first_page']+next_page_part

            yield scrapy.Request(
                next_url
                ,callback=self.detail_page()
                ,meta= {'item':deepcopy(item)}
            )
