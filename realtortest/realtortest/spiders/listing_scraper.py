from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import log
from scrapy.http import Request
from scrapy.selector import Selector
from realtortest.items import ListingItem, ListingItemLoader
from realtortest.extractor import PagerExtractor
import re

class ListingSpider(CrawlSpider):
    name = "realtor"
    start_urls = ["http://www.realtor.com/realestateandhomes-search/Sonora_CA",]

    rules = (Rule(link_extractor=PagerExtractor(), callback="parse_page"),)

    def parse_page(self, resp):
        base_http = re.search("^([a-z]+://[\/]?[^\/]*)/", resp.url).groups()
        if base_http:
            base_http = base_http[0]
        log.msg("response recieved from %s" % (resp.url))
        
        ## first parse this page
        sel = Selector(resp)
        for listing_sel in sel.xpath("//*[contains(@class,'listing-summary-wrapper group')]"):
            item = ListingItem()
            loader = ListingItemLoader(item=item, selector=listing_sel)
            for f in item.fields:
                ## our fields are named to match up with the page structure
                xpath_sel = "listing-%s" % (f.replace("_", "-"))
                loader.add_xpath(f, "ul//*[contains(@class, '%s')]" % xpath_sel)
            yield loader.load_item()  ## return items

        ## now extract links to the rest of the listing
        for link in sel.xpath("//ol[@class='pagination pagination-pos-b']/li/a[@class='paginate ']/@href").extract():
            log.msg("returning %s%s to follow" % (base_http,link))
            yield Request("%s%s" % (base_http,link))
