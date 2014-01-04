# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from db import datastore

class RealtortestPipeline(object):
    def process_item(self, item, spider):
        datastore.store(item)
