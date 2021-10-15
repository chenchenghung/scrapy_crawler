# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    main_group=scrapy.Field()
    title=scrapy.Field()
    regions=scrapy.Field()
    types=scrapy.Field()
    douban_rating=scrapy.Field()
    id=scrapy.Field()
    release_date=scrapy.Field()
    detail_first_page=scrapy.Field()
    rating_by_writer=scrapy.Field()
    comment=scrapy.Field()

