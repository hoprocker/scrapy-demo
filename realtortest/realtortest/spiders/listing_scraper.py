from scrapy.spider import BaseSpider

class ListingSpider(BaseSpider):
    name = "realtor.com"
    start_urls = ["http://www.realtor.com/realestateandhomes-search/Sonora_CA/sby-6?pgsz=50",]

    def parse(self, resp):
        pass

