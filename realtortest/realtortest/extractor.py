from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy import log
from scrapy.link import Link
import re

class PagerExtractor(SgmlLinkExtractor):
    __slots__ = ["pages_followed"]
    pages_followed = []

    def extract_links(self, resp):
        base_http = re.search("^([a-z]+://[\/]?[^\/]*)/", resp.url).groups()
        if base_http:
            base_http = base_http[0]

        if len(self.pages_followed) < 1:
            ## first time, add this page to list
            first_page = re.match("^[a-z]+://[\/]?[^\/]*(/.*)$", resp.url).groups()
            if first_page:
                log.msg("adding %s to followed" % first_page[0])
                self.pages_followed.append(first_page[0])
        sel = Selector(resp)
        links = sel.xpath("//ol[contains(@class,'pagination pagination-pos-b')]/li/a[contains(@class,'paginate')]/@href").extract()

        ## remove links we've followed already
        [links.pop(links.index(l)) for l in self.pages_followed if l in links]

        ## now add the rest
        log.msg("adding %s to followed" % (links,))
        self.pages_followed.extend(links) 
        return map(lambda x: Link("%s%s" % (base_http,x)), links)
