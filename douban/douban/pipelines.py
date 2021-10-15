# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

client= MongoClient(host="127.0.0.1",port=27017)
collection= client['douban']['dbmovie']

class DoubanPipeline:
    def process_item(self, item, spider):
        collection.insert(dict(item))

        return item


class MongoPipeline(object):
    # collection名字，自己任取

    # def __init__(self, mongo_uri, mongo_db, mongo_port):
    #     self.mongo_uri = mongo_uri
    #     self.mongo_db = mongo_db
    #     self.mongo_port = mongo_port
    #     self.client = None
    #     self.db = None

    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         mongo_uri=crawler.settings.get('MONGO_URI'),
    #         mongo_db=crawler.settings.get('MONGO_DATABASE'),
    #         mongo_port=crawler.settings.get('MONGODB_PORT')
    #     )

    # def open_spider(self, spider):
    #     self.client = pymongo.MongoClient(self.mongo_uri)
    #     self.db = self.client[self.mongo_db]

    # def process_item(self, item, spider):
    #     self.db[self.collection_name].insert(dict(item))
    #     return item

    def close_spider(self, spider):
        self.client.close()