# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from .spiders.labirint import LabirintSpider
from .spiders.book24 import Book24Spider


class BooksProjectPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.books
        self.db[LabirintSpider.name].drop()
        self.db[Book24Spider.name].drop()


    def process_item(self, item, spider):
        collection = self.db[spider.name]
        collection.update_one(item, {'$set': item}, upsert=True) 
        return item
