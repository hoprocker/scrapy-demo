from scrapy.spider import BaseSpider
from scrapy import log
from scrapy.selector import Selector
from realtortest.items import ListingItem

class ListingSpider(BaseSpider):
    name = "realtor"
    start_urls = ["http://www.realtor.com/realestateandhomes-search/Sonora_CA/sby-6?pgsz=50",]

    def parse(self, resp):
        log.msg("response recieved from %s" % (resp.url))
        
        sel = Selector(resp)
        for listing_sel in sel.xpath("//div[@class='listing-group']//div[@class='listing-wrap']"):
            item = ListingItem()
            for f in item.fields:
                xpath_sel = "listing-%s" % (f.replace("_", "-"))
                val = listing_sel.xpath("//span[@class='%s']/text()" % xpath_sel)[0].extract().strip()
                log.msg("item: %s --> %s" % (xpath_sel, val))
                item[f] = val
            yield item

