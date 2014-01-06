from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import log
from scrapy.http import Request
from scrapy.selector import Selector
from realtortest.items import ListingItem
from realtortest.extractor import PagerExtractor
import re

class ListingSpider(CrawlSpider):
    name = "realtor"
    start_urls = ["http://www.realtor.com/realestateandhomes-search/Sonora_CA",]

    rules = (Rule(link_extractor=PagerExtractor(), callback="parse_page"),)

    def parse_page(self, resp):
        base_http = re.search("^(http[s]?://[^\/]*)/.*", resp.url).groups()
        if base_http:
            base_http = base_http[0]
        log.msg("response recieved from %s" % (resp.url))
        
        sel = Selector(resp)
        for listing_sel in sel.xpath("//*[@class='listing-summary-wrapper group']"):
            item = ListingItem()
            for f in item.fields:
                xpath_sel = "listing-%s" % (f.replace("_", "-"))
                fld = listing_sel.xpath("ul//*[@class='%s']/text()" % xpath_sel)
                if len(fld) > 0:
                    val = fld[0].extract().strip()
                    log.msg("item: %s --> %s" % (xpath_sel, val))
                    item[f] = val
            yield item

        for link in sel.xpath("//ol[@class='pagination pagination-pos-b']/li/a[@class='paginate ']/@href").extract():
            log.msg("returning %s%s to follow" % (base_http,link))
            yield Request("%s%s" % (base_http,link))
